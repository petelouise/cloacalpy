import re
from collections import OrderedDict


def parse(input_text):
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
