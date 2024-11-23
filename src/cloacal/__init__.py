from collections import OrderedDict
from typing import Any

from .format import format_dict, format_str
from .parse import parse


def load(path: str) -> OrderedDict[Any, Any]:
    with open(path, "r") as f:
        return parse(f.read())


__all__ = ["parse", "format_str", "format_dict"]
