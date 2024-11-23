from collections import OrderedDict

import tomllib

from .format import format_clo


def toml_to_clo(toml_input: str, max_line_length: int = 44) -> str:
    """
    Converts a TOML string to a formatted Cloacal string.

    Args:
        toml_input (str): The input TOML string.
        max_line_length (int): Maximum line width for formatting (default: 44).

    Returns:
        str: Formatted Cloacal string.
    """
    data = OrderedDict(tomllib.loads(toml_input))
    return format_clo(data, max_line_length=max_line_length)
