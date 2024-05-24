
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def get_block_type(block):
    if (
        block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")
    ):
        return block_type_heading

    if len(block) >= 6 and block[:3] == "```" and block[-3:] == "```":
        return block_type_code

    lines = block.split("\n")

    if __all_items_starts_with(lines, "> "):
        return block_type_quote
    if __all_items_starts_with(lines, "* "):
        return block_type_unordered_list
    if __all_items_starts_with(lines, "- "):
        return block_type_unordered_list
    if __items_are_sequential(lines):
        return block_type_ordered_list

    return block_type_paragraph


def __all_items_starts_with(items, char):
    for item in items:
        if not item.startswith(char):
            return False
    return True


def __items_are_sequential(items):
    for i in range(0, len(items)):
        if not items[i].startswith(f"{i + 1}. "):
            return False
    return True
