# Makefile Modifier

A command-line tool to modify Makefile rules.

## Installation

```bash
pip install git+https://github.com/furiosa-ai/makefile-modifier.git
```

## Usage

```bash
makefile-modifier <command> [<args>]
```

Available commands:
- `add_dependency`: Add a dependency to a rule
- `add_line`: Add a line to a rule
- `add_rule`: Add a new rule
- `copy_rules`: Copy rules from one Makefile to another

For more information on each command, use:

```bash
makefile-modifier <command> --help
```

## Examples

Add a dependency:
```bash
makefile-modifier add_dependency path/to/Makefile rule_name new_dependency
```

Add a line to a rule:
```bash
makefile-modifier add_line path/to/Makefile rule_name "new command"
```

Add a new rule:
```bash
makefile-modifier add_rule path/to/Makefile new_rule_name "dep1 dep2" "command1" "command2"
```

Copy rules:
```bash
makefile-modifier copy_rules path/to/target/Makefile path/to/source/Makefile rule1 rule2
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.