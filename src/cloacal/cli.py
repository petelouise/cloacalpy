import argparse
import sys

from .format import format_clo_string

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Format a .clo file")
    argparser.add_argument(
        "file",
        nargs="?",
        help="Input file (optional, reads from stdin if not provided)",
    )
    argparser.add_argument(
        "--width", type=int, default=44, help="Maximum line width (default: 44)"
    )
    args = argparser.parse_args()

    if not args.file:
        input_text = sys.stdin.read()
    else:
        with open(args.file, "r") as f:
            input_text = f.read()

    formatted_output = format_clo_string(input_text, max_line_length=args.width)
    print(formatted_output)
