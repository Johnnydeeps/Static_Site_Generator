import unittest

from markdown_to_blocks import markdown_to_blocks


# testing basic conversion, text from lesson.
class TestMarkdownToBlocks(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
