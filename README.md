# Cloacal

A tool for formatting character sheets in CLO format and converting from TOML.

## Installation

```bash
pip install cloacal
```

## Usage

### Format a CLO file:

```bash
cloacal format -f character.clo
```

Or pipe input:

```bash
cat character.clo | cloacal format
```

### Convert TOML to CLO:

```bash
cloacal toml -f character.toml
```

Example TOML input:
```toml
name = "Carlisle"
age = 99
species = "seagull"
ilk = "bird"

description = """
Id ipsum elit tempor non incididunt laborum 
anim dolore eu fugiat.
"""

memories = [
    "Consectetur ut qui Lorem ad.",
    "Veniam mollit nostrud velit laborum."
]
```

## Options

- `--width N`: Set maximum line width (default: 44)
