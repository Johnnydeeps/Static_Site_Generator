from enum import Enum


def markdown_to_blocks(markdown):
    # remove block separation, ie. new paragraphs "\n\n" in md text.
    markdown_split = markdown.split("\n\n")
    # removing any potential whitespace ie. " " with .strip()
    striped_blocks = []
    for block in markdown_split:
        # When you call .strip() with no arguments, it strips all leading and
        # trailing whitespace — spaces, tabs, newlines (\n), carriage returns, etc.
        strip_result = block.strip()
        if strip_result:
            striped_blocks.append(strip_result)
        else:
            continue
    return striped_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_striped_block):
    # checking an input block for a heading block, level 1 to 6.
    if markdown_striped_block.startswith(
        ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    ):
        return BlockType.HEADING

    # checking an input block for a code block.
    if markdown_striped_block.startswith("```\n") and markdown_striped_block.endswith(
        "```"
    ):
        return BlockType.CODE

    # checking an input block for a quote block.
    if markdown_striped_block.startswith((">", "> ")):
        split_result = markdown_striped_block.split("\n")
        for result in split_result:
            if not result.startswith((">", "> ")):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # checking an input block for an unordered list block.
    if markdown_striped_block.startswith("- "):
        split_result = markdown_striped_block.split("\n")
        for result in split_result:
            if not result.startswith(("- ")):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    # checking an input block for an ordered list block.
    if markdown_striped_block.startswith("1. "):
        split_result = markdown_striped_block.split("\n")
        i = 1
        for result in split_result:
            if not result.startswith((f"{i}. ")):
                return BlockType.PARAGRAPH
            else:
                i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
