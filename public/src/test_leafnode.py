import unittest
from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_tag(self):
        node = LeafNode("p", "This is paragraph element")
        self.assertEqual(node.to_html(), "<p>This is paragraph element</p>")

    def test_props_to_html_tag_empty(self):
        node = LeafNode(None, "This is paragraph element")
        self.assertEqual(node.to_html(), "This is paragraph element")

    def test_props_to_html_one_prop(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


if __name__ == "__main__":
    unittest.main()
