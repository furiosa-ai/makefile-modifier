import sys
import argparse
from .modifier import modify_makefile

def main():
    parser = argparse.ArgumentParser(description="Modify Makefile rules")
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Add dependency
    parser_add_dep = subparsers.add_parser('add_dependency', help='Add a dependency to a rule')
    parser_add_dep.add_argument('makefile', help='Path to the Makefile')
    parser_add_dep.add_argument('rule_name', help='Name of the rule')
    parser_add_dep.add_argument('new_dependency', help='New dependency to add')

    # Add line
    parser_add_line = subparsers.add_parser('add_line', help='Add a line to a rule')
    parser_add_line.add_argument('makefile', help='Path to the Makefile')
    parser_add_line.add_argument('rule_name', help='Name of the rule')
    parser_add_line.add_argument('new_line', help='New line to add')

    # Add rule
    parser_add_rule = subparsers.add_parser('add_rule', help='Add a new rule')
    parser_add_rule.add_argument('makefile', help='Path to the Makefile')
    parser_add_rule.add_argument('rule_name', help='Name of the new rule')
    parser_add_rule.add_argument('dependencies', help='Dependencies of the new rule')
    parser_add_rule.add_argument('commands', nargs='+', help='Commands for the new rule')

    # Copy rules
    parser_copy_rules = subparsers.add_parser('copy_rules', help='Copy rules from one Makefile to another')
    parser_copy_rules.add_argument('makefile', help='Path to the target Makefile')
    parser_copy_rules.add_argument('source_makefile', help='Path to the source Makefile')
    parser_copy_rules.add_argument('rules', nargs='+', help='Rules to copy')

    args = parser.parse_args()

    if args.action is None:
        parser.print_help()
        sys.exit(1)

    success = modify_makefile(args)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()