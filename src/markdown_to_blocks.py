from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_blocks(markdown_text):
    # remove block separation, ie. new paragraphs "\n\n" in md text.
    markdown_split = markdown_text.split("\n\n")
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


# helper to create a list of children (leaf nodes) using helpers from textnode.py and inline_markdown.py
def text_to_leaf_nodes(markdown_text):
    children = []
    text_nodes = text_to_textnodes(markdown_text)
    for text_node in text_nodes:
        child_node = text_node_to_html_node(text_node)
        children.append(child_node)
    return children


def block_to_html_parent_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        lines = block.split("\n")
        striped_lines = []
        for line in lines:
            striped_line = line.strip()
            striped_lines.append(striped_line)
        text = " ".join(striped_lines)
        children = text_to_leaf_nodes(text)
        return ParentNode("p", children)

    if block_type == BlockType.HEADING:
        level = 0
        for char in block:
            if char == "#":
                level += 1
            else:
                break

        parts = block.split("# ", 1)
        text = parts[1]
        children = text_to_leaf_nodes(text)
        return ParentNode(f"h{level}", children)

    if block_type == BlockType.CODE:
        lines = block.split("\n")
        striped_lines = []
        for line in lines:
            striped_line = line.strip()
            striped_lines.append(striped_line)
        text = "\n".join(striped_lines[1:-1]) + "\n"
        node = TextNode(text, TextType.TEXT)
        children = text_node_to_html_node(node)
        return ParentNode("pre", [ParentNode("code", [children])])

    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        striped_lines = []
        for line in lines:
            if line.startswith(">"):
                striped_result = line.lstrip(">")
                remove_whitespace = striped_result.strip()
                striped_lines.append(remove_whitespace)
        content = " ".join(striped_lines)
        children = text_to_leaf_nodes(content)
        return ParentNode("blockquote", children)

    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        htmlnodes = []
        for line in lines:
            if line.startswith("- "):
                text = line[2:]
                children = text_to_leaf_nodes(text)
                htmlnodes.append(ParentNode("li", children))
        return ParentNode("ul", htmlnodes)

    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        htmlnodes = []
        i = 1
        for line in lines:
            if line.startswith(f"{i}"):
                split_line = line.split(". ", 1)
                text = split_line[1]
                children = text_to_leaf_nodes(text)
                htmlnodes.append(ParentNode("li", children))
                i += 1
        return ParentNode("ol", htmlnodes)


def markdown_to_html_node(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    htmlnodes = []
    for block in blocks:
        htmlnode = block_to_html_parent_node(block)
        htmlnodes.append(htmlnode)
    return ParentNode("div", htmlnodes)
