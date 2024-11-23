import argparse
import sys

from .format import format_clo_string


def main():
    argparser = argparse.ArgumentParser(description="Format a .clo file")
    argparser.add_argument(
        "-f", "--file",
        help="Input file (optional, reads from stdin if not provided)",
    )
    argparser.add_argument(
        "--width", type=int, default=44, help="Maximum line width (default: 44)"
    )
    args = argparser.parse_args()

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
