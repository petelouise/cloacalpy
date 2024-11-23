import textwrap

from .parse import parse_clo


def format_clo(data: dict[str, str | list], max_line_length=44):
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
