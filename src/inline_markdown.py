import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        new_node = old_node.text.split(delimiter)
        if len(new_node) % 2 == 0:
            raise ValueError("invalid markdown: unmatched delimiter")
        for i in range(len(new_node)):
            if new_node[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(new_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(new_node[i], text_type))

    return new_nodes


# regex, use website to build the search code https://regexr.com/
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_images = extract_markdown_images(old_node.text)
        if not len(extracted_images):
            new_nodes.append(old_node)
            continue
        working_text = old_node.text
        for alt, url in extracted_images:
            before, after = working_text.split(f"![{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            working_text = after
        if working_text:
            new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_links = extract_markdown_links(old_node.text)
        if not len(extracted_links):
            new_nodes.append(old_node)
            continue
        working_text = old_node.text
        for link_text, url in extracted_links:
            before, after = working_text.split(f"[{link_text}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            working_text = after
        if working_text:
            new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes


# manual/hardcoded markdown delimters added here, and turned into a node with the correct
# TextType nodes to associate delimiters and TextTypes correctly with the above helper
# functions. **this is the link between TEXTType Enums values and markdown plain text.**
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # delimiter bold ** markdown text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # delimiter italics _ markdown text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    # delimiter italics _ markdown text
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # split_nodes_images from markdown text
    nodes = split_nodes_image(nodes)
    # split_nodes_links from markdown text
    nodes = split_nodes_link(nodes)
    return nodes
