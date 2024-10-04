from pyparsing import Word, alphanums, Suppress, OneOrMore, restOfLine, LineEnd, ParseException

def parse_makefile(makefile_path):
    rule = Word(alphanums + "_-") + Suppress(":") + restOfLine + LineEnd()
    
    with open(makefile_path, 'r') as file:
        content = file.read()
    
    parsed_content = []
    for line in content.splitlines():
        try:
            parsed = rule.parseString(line)
            parsed_content.append(('rule', parsed[0], parsed[1].strip()))
        except ParseException:
            parsed_content.append(('line', line))
    
    return parsed_content

def write_makefile(makefile_path, content):
    with open(makefile_path, 'w') as file:
        for item in content:
            if item[0] == 'rule':
                file.write(f"{item[1]}: {item[2]}\n")
            else:
                file.write(f"{item[1]}\n")

def add_dependency_to_rule(parsed_content, rule_name, new_dependency):
    for i, item in enumerate(parsed_content):
        if item[0] == 'rule' and item[1] == rule_name:
            dependencies = item[2].split()
            if new_dependency not in dependencies:
                dependencies.append(new_dependency)
                parsed_content[i] = ('rule', rule_name, ' '.join(dependencies))
            return True
    return False

def add_line_to_rule(parsed_content, rule_name, new_line):
    for i, item in enumerate(parsed_content):
        if item[0] == 'rule' and item[1] == rule_name:
            j = i + 1
            while j < len(parsed_content) and parsed_content[j][0] == 'line' and parsed_content[j][1].strip().startswith('\t'):
                j += 1
            parsed_content.insert(j, ('line', f"\t{new_line}"))
            return True
    return False

def add_new_rule(parsed_content, rule_name, dependencies, commands):
    parsed_content.append(('rule', rule_name, ' '.join(dependencies)))
    for command in commands:
        parsed_content.append(('line', f"\t{command}"))
    return True

def copy_make_rules(source_parsed_content, target_parsed_content, rules_to_copy):
    copied_rules = []
    for rule in rules_to_copy:
        rule_content = []
        copy_flag = False
        for item in source_parsed_content:
            if item[0] == 'rule' and item[1] == rule:
                rule_content.append(item)
                copy_flag = True
            elif copy_flag:
                if item[0] == 'rule':
                    break
                rule_content.append(item)
        
        if rule_content:
            target_parsed_content.extend(rule_content)
            copied_rules.append(rule)
        else:
            print(f"Warning: Rule '{rule}' not found in source Makefile")
    
    return copied_rules

def modify_makefile(args):
    parsed_content = parse_makefile(args.makefile)
    
    if args.action == 'add_dependency':
        if add_dependency_to_rule(parsed_content, args.rule_name, args.new_dependency):
            print(f"Successfully added dependency '{args.new_dependency}' to rule '{args.rule_name}'")
        else:
            print(f"Error: Rule '{args.rule_name}' not found")
            return False
    elif args.action == 'add_line':
        if add_line_to_rule(parsed_content, args.rule_name, args.new_line):
            print(f"Successfully added line '{args.new_line}' to rule '{args.rule_name}'")
        else:
            print(f"Error: Rule '{args.rule_name}' not found")
            return False
    elif args.action == 'add_rule':
        if add_new_rule(parsed_content, args.rule_name, args.dependencies.split(), args.commands):
            print(f"Successfully added new rule '{args.rule_name}'")
        else:
            print(f"Error: Failed to add new rule '{args.rule_name}'")
            return False
    elif args.action == 'copy_rules':
        source_parsed_content = parse_makefile(args.source_makefile)
        copied_rules = copy_make_rules(source_parsed_content, parsed_content, args.rules)
        if copied_rules:
            print(f"Successfully copied rules: {', '.join(copied_rules)}")
        else:
            print("Error: No rules were copied")
            return False
    
    write_makefile(args.makefile, parsed_content)
    return True