import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    # testing an empty string
    def test_no_title(self):
        markdown_text = ""
        with self.assertRaises(Exception):
            extract_title(markdown_text)

    # testing a multi line markdown text
    def test_title_multiline(self):
        markdown_text = "# This is a heading\n with multiple lines"
        title = extract_title(markdown_text)
        self.assertEqual(title, "This is a heading")

    # testing a multi line markdown text with heading in second line
    def test_title_heading_on_not_first_line(self):
        markdown_text = (
            "This is not a heading\n# This is a heading\n with multiple lines"
        )
        title = extract_title(markdown_text)
        self.assertEqual(title, "This is a heading")

    # testing a multi line markdown text with a h3 heading rather than an h1
    # to check is raises error correctly
    def test_title_wrong_heading_level(self):
        markdown_text = "This is a heading\n## with multiple lines"
        with self.assertRaises(Exception):
            extract_title(markdown_text)
