import argparse
import sys

from .format import format_clo_string
from .toml_to_clo import toml_to_clo


def main():
    argparser = argparse.ArgumentParser(description="Format a .clo file or convert TOML to Cloacal format")
    subparsers = argparser.add_subparsers(dest='command', required=True, help='Available commands')

    # Existing formatter command
    format_parser = subparsers.add_parser('format', help='Format a .clo file')
    format_parser.add_argument(
        "-f", "--file",
        help="Input .clo file (optional, reads from stdin if not provided)",
    )
    format_parser.add_argument(
        "--width", type=int, default=44, help="Maximum line width (default: 44)"
    )

    # New TOML conversion command
    toml_parser = subparsers.add_parser('toml', help='Convert TOML to Cloacal format')
    toml_parser.add_argument(
        "-f", "--file",
        required=True,
        help="Input TOML file"
    )
    toml_parser.add_argument(
        "--width", type=int, default=44, help="Maximum line width (default: 44)"
    )

    args = argparser.parse_args()

    if args.command == 'format':
        if args.file:
            with open(args.file, "r") as f:
                input_text = f.read()
        elif not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            argparser.print_help()
            sys.exit(1)

        formatted_output = format_clo_string(input_text, max_line_length=args.width)
        print(formatted_output)

    elif args.command == 'toml':
        with open(args.file, "r") as f:
            toml_input = f.read()
        formatted_output = toml_to_clo(toml_input, max_line_length=args.width)
        print(formatted_output)
