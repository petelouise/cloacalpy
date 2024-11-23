import tomllib

from .format import format_dict


def toml2clo(toml_input: str, max_line_length: int = 44) -> str:
    """
    Converts a TOML string to a formatted Cloacal string.

    Args:
        toml_input (str): The input TOML string.
        max_line_length (int): Maximum line width for formatting (default: 44).

    Returns:
        str: Formatted Cloacal string.
    """
    data = []
    for _, value in tomllib.loads(toml_input).items():
        data.append({k: str(v) if isinstance(v, int) else v for k, v in value.items()})
    # TODO: adjust to support multiple entries
    if len(data) > 1:
        raise NotImplementedError("multiple entries not supported yet.")
    if len(data) == 0:
        return ""
    return format_dict(data[0], max_line_length=max_line_length)
