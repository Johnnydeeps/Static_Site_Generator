import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "click me", None, {"href": "https://google.com"})
        node2 = HTMLNode("a", "click me", None, {"href": "https://google.com"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("a", "click me", None, {"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_html_none(self):
        node = HTMLNode("a", "click me", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "click me", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">click me</a>')

    def test_to_html_fail_no_children(self):
        bad_node = ParentNode("b", None)
        with self.assertRaises(ValueError):
            bad_node.to_html()

    def test_to_html_fail_no_tag(self):
        # Create a node with no tag, but with valid children
        child_node = LeafNode("p", "child")
        bad_node = ParentNode(None, [child_node])
        with self.assertRaisesRegex(ValueError, "All parent nodes must have a tag."):
            bad_node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_with_props_and_multiple_children(self):
        child1 = LeafNode("span", "hello")
        child2 = LeafNode("b", "world")
        parent = ParentNode("div", [child1, child2], {"class": "box", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="box" id="main"><span>hello</span><b>world</b></div>',
        )


if __name__ == "__main__":
    unittest.main()
