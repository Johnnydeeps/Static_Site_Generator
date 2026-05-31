import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("hello `world` bye", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_link_not_image(self):
        matches = extract_markdown_links(
            "![image](https://imgur.com/pic.png) and [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_unclosed_delimiter(self):
        node = TextNode("This has **unclosed bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestSplitNodesImages(unittest.TestCase):
    # test one image
    def test_split_nodes_image_one_image(self):
        node = TextNode(
            "before ![alt text](https://example.com/img.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    # test two images
    def test_split_nodes_image_two_images(self):
        node = TextNode(
            "before ![alt text](https://example.com/img.png) middle ![alt text1](https://example.com/img1.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("alt text1", TextType.IMAGE, "https://example.com/img1.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    # test one image at the start with text after, function should not create a text node before the image node
    def test_split_nodes_image_one_image_no_text_before(self):
        node = TextNode(
            "![alt text](https://example.com/img.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt text", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    # test one image with text at the start, function should not create a text node after the image node
    def test_split_nodes_image_one_image_no_text_after(self):
        node = TextNode(
            "before ![alt text](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    # test one image with no text, function should not create a text node before/after the image node
    def test_split_nodes_image_one_image_no_text(self):
        node = TextNode(
            "![alt text](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt text", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )

    # no image, should return the original TextNode unchanged as a list
    def test_split_nodes_image_no_image(self):
        node = TextNode(
            "before after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before after", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLinks(unittest.TestCase):
    # test one link
    def test_split_nodes_link_one_link(self):
        node = TextNode(
            "before [link text](https://example.com) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://example.com"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    # test two links
    def test_split_nodes_link_two_links(self):
        node = TextNode(
            "before [link text](https://example.com) middle [link text1](https://example1.com) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://example.com"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("link text1", TextType.LINK, "https://example1.com"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    # test one link at the start with text after, function should not create a text node before the link node
    def test_split_nodes_link_one_link_no_text_before(self):
        node = TextNode(
            "[link text](https://example.com) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link text", TextType.LINK, "https://example.com"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    # test one link with text at the start, function should not create a text node after the link node
    def test_split_nodes_link_one_link_no_text_after(self):
        node = TextNode(
            "before [link text](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    # test one link with no text, function should not create a text node before/after the link node
    def test_split_nodes_link_one_link_no_text(self):
        node = TextNode(
            "[link text](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link text", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    # no link, should return the original TextNode unchanged as a list
    def test_split_nodes_link_no_link(self):
        node = TextNode(
            "before after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("before after", TextType.TEXT),
            ],
            new_nodes,
        )


class TestTextToTextnodes(unittest.TestCase):
    # testing text_to_textnodes conversion from markdown to TextType nodes with a mix of types
    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    # testing text_to_textnodes conversion from markdown to TextType nodes with no delimiters just plain text
    def test_text_to_textnodes_no_delimiters(self):
        text = "This is plain text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is plain text", TextType.TEXT),
            ],
            new_nodes,
        )

    # testing text_to_textnodes conversion from markdown to TextType nodes with two texttypes with no plain text between.
    def test_text_to_textnodes_no_text_between_types(self):
        text = (
            "**text**_italic_`code block`"
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)"
        )
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("text", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code block", TextType.CODE),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
