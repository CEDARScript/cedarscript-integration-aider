# CEDARScript Integration: Aider

[![PyPI version](https://badge.fury.io/py/cedarscript-editor.svg)](https://pypi.org/project/cedarscript-editor/)
[![Python Versions](https://img.shields.io/pypi/pyversions/cedarscript-editor.svg)](https://pypi.org/project/cedarscript-editor/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`CEDARScript Integration: Aider` allows `Aider` to use CEDARScript as an edit format.


## What is CEDARScript?

[CEDARScript](https://github.com/CEDARScript/cedarscript-grammar#readme) (_Concise Examination, Development, And Refactoring Script_)
is a domain-specific language that aims to improve how AI coding assistants interact with codebases and communicate their code modification intentions.
It provides a standardized way to express complex code modification and analysis operations, making it easier for
AI-assisted development tools to understand and execute these tasks.

## Features

- Given a `CEDARScript` script and a base direcotry, executes the script commands on files inside the base directory;
- Return results in `XML` format for easier parsing and processing by LLM systems

## Installation

You can install `CEDARScript` Editor using pip:

```
pip install cedarscript_editor
```

## Usage

Here's a quick example of how to use `CEDARScript` Editor:

```python
from cedarscript_editor import CEDARScriptEdior

parser = CEDARScriptEdior()
code = """
CREATE FILE "example.py"
UPDATE FILE "example.py"
    INSERT AT END OF FILE
        CONTENT
            print("Hello, World!")
        END CONTENT
END UPDATE
"""

commands, errors = parser.parse_script(code)

if errors:
    for error in errors:
        print(f"Error: {error}")
else:
    for command in commands:
        print(f"Parsed command: {command}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
