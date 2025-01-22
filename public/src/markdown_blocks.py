def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    for line in block.split("\n"):
        start, start_three, end_three = line[0], line[:3], line[-3:]
        if start == "#":
            return "heading"
        elif start in ["*", "-"]:
            return "unordered_list"
        elif start == ".":
            return "ordered_list"
        elif start == ">":
            return "quote"
        elif start_three == end_three == "```":
            return "code"
        else:
            return "paragraph"
