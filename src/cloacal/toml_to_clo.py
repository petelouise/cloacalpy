import tomli
from collections import OrderedDict
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
    data = tomli.loads(toml_input)
    clo_data = OrderedDict()

    # Map TOML fields to Cloacal fields
    if 'name' in data:
        clo_data['name'] = data['name']
    if 'age' in data:
        clo_data['age'] = str(data['age'])
    if 'species' in data:
        clo_data['species'] = data['species']
    if 'ilk' in data:
        clo_data['ilk'] = data['ilk']
    if 'description' in data:
        clo_data['description'] = data['description']
    if 'memories' in data:
        clo_data['memories'] = data['memories']

    return format_clo(clo_data, max_line_length=max_line_length)
