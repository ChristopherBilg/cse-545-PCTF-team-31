# cse-545-PCTF-team-31

CSE 545: Software Security - PCTF - Team 31

## Examples to Run

- `python3 runner.py -h`
- `python3 runner.py -l`
- `python3 runner.py -m example`
- `python3 runner.py -m example -a 1 2 3`

## Environment

TShark v3.2.3 or higher
WireShark v3.2.3 or higher
Python v3.8.5 or higher

- argparse v1.4.0 or higher
- pathlib v1.0.1 or higher
- pyshark v0.4.2.11 or higher

## Development

1. Create a new module in the "modules/" directory using kebab-case, IE: `modules/kebab-case-module.py`
2. Add the following shebang line at the top of the file: `#!/usr/bin/env python3`
3. Define the following four functions:
   1. module_name: return the module name, in kebab-case
   2. module_help: return helpful information about the module
   3. module_usage: return an example usage string of the module, IE: `kebab-case-module <arg1> <arg2>`
   4. main: the function that will run the business logic of the module
4. At the bottom of the module file add the following code block:

```python
if __name__ == "__main__":
  main()
```

**NOTE 1: Python3 cares about indentation, so 2 spaces can be the indentation that this project uses. It doesn't _really_ matter.**

**NOTE 2: Take a look at the modules/example.py file for further clarification.**
