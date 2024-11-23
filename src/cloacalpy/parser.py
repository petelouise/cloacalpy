import re
import textwrap
from collections import OrderedDict


def parse_clo(input_text):
    """
    Parses the clo input text and returns an OrderedDict representing the data.
    """

    lines = input_text.strip("\n").split("\n")
    data = OrderedDict()
    i = 0
    n = len(lines)

    # Patterns to match block headers and key-value pairs
    block_header_pattern = re.compile(r"^\s*(\w+)\s*[-~>*]+\s*$")
    key_value_pattern = re.compile(
        r"^\s*(\w+)\s*[-~>*]+\s*(.+)$"
    )  # Accept various separators

    while i < n:
        line = lines[i]
        stripped_line = line.strip()

        # Skip empty lines
        if not stripped_line:
            i += 1
            continue

        # Check for name box
        if stripped_line.startswith("+"):
            # Name box detected
            if i + 1 < n and lines[i + 1].strip().startswith("|"):
                name_line = lines[i + 1].strip()
                name = name_line.strip("|").strip()
                data["name"] = name
                i += 3  # Skip the name box lines (+, | name |, +)
                continue
            else:
                i += 1
                continue

        # Check for block header (e.g., description ----)
        m = block_header_pattern.match(line)
        if m:
            key = m.group(1)
            i += 1
            block_lines = []
            list_items = []
            while i < n:
                block_line = lines[i]
                stripped_block_line = block_line.strip()

                if not stripped_block_line:
                    i += 1
                    continue

                # Check if this line is a new block header or key-value pair
                new_block_match = block_header_pattern.match(block_line)
                new_kv_match = key_value_pattern.match(block_line)
                if new_block_match or new_kv_match:
                    break  # New block or key-value pair detected

                if stripped_block_line.startswith(">"):
                    # Start of a new list item
                    current_item_lines = []
                    subtask_lines = []
                    # Get the first line of the item
                    item_line = stripped_block_line.lstrip(">").strip()
                    current_item_lines.append(item_line)
                    i += 1

                    # Collect continuation lines and subtasks for this item
                    while i < n:
                        next_line = lines[i].rstrip()
                        if not next_line.strip():
                            i += 1
                            continue

                        # Check if this is a new top-level list item or block
                        if (
                            (
                                next_line.strip().startswith(">")
                                and not next_line.startswith("        >")
                            )
                            or block_header_pattern.match(next_line)
                            or key_value_pattern.match(next_line)
                        ):
                            break

                        # If it's a subtask (more indented '>')
                        if next_line.strip().startswith(">") and next_line.startswith(
                            "        "
                        ):
                            subtask_lines.append(next_line.strip().lstrip(">").strip())
                            i += 1
                        # If it's an indented continuation line
                        elif next_line.startswith(" ") or next_line.startswith("\t"):
                            current_item_lines.append(next_line.strip())
                            i += 1
                        else:
                            break

                    # Join all lines for this item and its subtasks
                    item_text = " ".join(current_item_lines + subtask_lines)
                    list_items.append(item_text)
                elif block_line.startswith(" ") or block_line.startswith("\t"):
                    # Part of block text
                    block_lines.append(stripped_block_line)
                    i += 1
                else:
                    i += 1  # Skip unrecognized lines within a block
            # Check if this is a list block by looking for any '>' markers
            is_list_block = any(
                line.strip().startswith(">") for line in lines[i - 10 : i]
            )

            if list_items:
                data[key] = list_items
            elif block_lines:
                block_text = " ".join(block_lines)
                data[key] = block_text
            elif is_list_block:
                data[key] = []  # Empty list block
            else:
                data[key] = ""  # Empty text block
            continue

        # Check for key-value pair with value (e.g., age -- 99)
        m = key_value_pattern.match(line)
        if m:
            key = m.group(1)
            value = m.group(2).strip()
            data[key] = value
            i += 1
            continue

        # Unrecognized line, skip it
        i += 1

    return data


def format_clo(data, max_line_length=44):
    """
    formats the data ordereddict into a beautiful clo string.

    args:
        data: ordereddict containing the parsed clo data
        max_line_length: maximum length for wrapped lines (default: 44)
    """
    wrap_width = max_line_length
    indent = 2  # indentation for block texts

    lines = []

    # format the name box
    if "name" in data:
        name = data["name"]
        name_length = len(name)
        # use max_line_length for box width, adjust if name length is odd
        box_width = max_line_length if name_length % 2 == 0 else max_line_length - 1
        top_bottom = "+" + "-" * (box_width - 2) + "+"
        # calculate padding needed for perfect centering
        total_padding = box_width - 4 - name_length  # -4 for "| " and " |"
        padding = " " * (total_padding // 2)
        middle = f"| {padding}{name}{padding} |"
        lines.append(top_bottom)
        lines.append(middle)
        lines.append(top_bottom)
        lines.append("")  # blank line

    # sort simple key-value pairs
    simple_pairs = [
        (k, v)
        for k, v in data.items()
        if k != "name" and isinstance(v, str) and "\n" not in v and len(v.split()) <= 5
    ]
    sorted_pairs = sorted(simple_pairs)

    # find the longest value to align all values
    max_value_pos = max(
        (len(key) + 3 for key, value in sorted_pairs),  # +3 for minimum dashes
        default=0,
    )

    # process simple key-value pairs first
    for key, value in sorted_pairs:
        # calculate dashes needed to align the value at max_value_pos
        dash_count = max_value_pos - len(key)
        dashes = "-" * dash_count
        line = f"{key} {dashes} {value}"
        lines.append(line)

    if simple_pairs:  # add blank line after key-value pairs if any exist
        lines.append("")

    # process remaining blocks in original order
    for key, value in data.items():
        if key == "name" or (key, value) in simple_pairs:
            continue

        if isinstance(value, list):
            # list block
            # fill remaining space with dashes to reach max_line_length
            dash_count = (
                max_line_length - len(key) - 2
            )  # -2 for the space after key and end
            header_dashes = "-" * dash_count
            header_line = f"{key} {header_dashes}"
            lines.append(header_line)
            for item in value:
                # calculate effective width for wrapping
                effective_width = wrap_width - indent - 2
                # use break_long_words=false to prevent word splitting
                wrapped_item = textwrap.fill(
                    item,
                    width=effective_width,
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                item_lines = wrapped_item.split("\n")
                indented_item = [" " * indent + "> " + item_lines[0]]
                indented_item += [" " * (indent + 2) + line for line in item_lines[1:]]
                lines.extend(indented_item)
            lines.append("")  # blank line after each block
        else:
            # block text
            # fill remaining space with dashes to reach max_line_length
            dash_count = (
                max_line_length - len(key) - 2
            )  # -2 for the space after key and end
            header_dashes = "-" * dash_count
            header_line = f"{key} {header_dashes}"
            lines.append(header_line)
            # calculate effective width for wrapping
            effective_width = wrap_width - indent
            # use break_long_words=false to prevent word splitting
            wrapped_text = textwrap.fill(
                value,
                width=effective_width,
                break_long_words=False,
                break_on_hyphens=False,
            )
            indented_lines = [" " * indent + line for line in wrapped_text.split("\n")]
            lines.extend(indented_lines)
            lines.append("")  # blank line after each block

    # remove any trailing spaces from each line and join with newlines
    formatted_text = "\n".join(line.rstrip() for line in lines)
    # ensure single trailing newline
    return formatted_text.strip("\n")


def format_clo_string(input_text, max_line_length=44):
    """
    takes an ugly clo input string and returns a nicely formatted clo string.

    args:
        input_text: the input clo string to format
        max_line_length: maximum length for wrapped lines (default: 44)
    """
    data = parse_clo(input_text)
    formatted_output = format_clo(data, max_line_length=max_line_length)
    return formatted_output


if __name__ == "__main__":
    import argparse
    import sys

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
