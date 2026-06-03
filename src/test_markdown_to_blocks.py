import unittest

from markdown_to_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    # testing basic conversion, text from lesson.
    def test_markdown_to_blocks(self):
        md = (
            "This is **bolded** paragraph"
            "\n\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line"
            "\n\n"
            "- This is a list\n"
            "- with items"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    # testing the removal of multiple new lines between blocks ie. \n\n x2 or more.
    def test_markdown_to_blocks_multiple_no_new_lines(self):
        md = (
            "\n\n"
            "This is **bolded** paragraph"
            "\n\n"
            "\n\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line"
            "\n\n"
            "- This is a list\n"
            "- with items"
            "\n\n"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    # testing single block with no new lines ie. no \n\n
    def test_markdown_to_blocks_multiple_new_lines(self):
        md = (
            "This is **bolded** paragraph"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line"
            "- This is a list\n"
            "- with items"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                (
                    "This is **bolded** paragraph"
                    "This is another paragraph with _italic_ text and `code` here\n"
                    "This is the same paragraph on a new line"
                    "- This is a list\n- with items"
                )
            ],
            blocks,
        )
        # testing removal of extra white space before and after blocks

    def test_markdown_to_blocks_extra_whitespace(self):
        md = (
            "  This is **bolded** paragraph"
            "\n\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line"
            "\n\n"
            "- This is a list\n"
            "- with items  "
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )


class TestBlockToBlockType(unittest.TestCase):
    # testing overall basic functionality for converting all types starting with headings.
    def test_block_to_block_type_headings(self):
        block = "# this is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    # testing an code block.
    def test_block_to_block_type_code(self):
        block = "```\n this is code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    # testing an quote block.
    def test_block_to_block_type_quote(self):
        block = "> this is a quote block"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    # testing an quote block with multiple lines.
    def test_block_to_block_type_quote_multiline(self):
        block = "> this is a quote block\n> with multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    # testing an unordered list block.
    def test_block_to_block_type_unordered_list(self):
        block = "- this is an unordered list block"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    # testing an unordered list block with multiple lines.
    def test_block_to_block_type_unordered_list_multiline(self):
        block = "- this is an unordered list block\n- with multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    # testing an ordered list block.
    def test_block_to_block_type_ordered_list(self):
        block = "1. this is an ordered list block"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    # testing an ordered block with multiple lines.
    def test_block_to_block_type_ordered_list_multiline(self):
        block = "1. this is an ordered list block\n2. with multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    # testing an incorrectly ordered block with multiple lines.
    def test_block_to_block_type_incorrect_ordered_list_multiline(self):
        block = "1. this is an unordered list block\n3. with multiple lines\n2. that is incorrect"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNodes(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
