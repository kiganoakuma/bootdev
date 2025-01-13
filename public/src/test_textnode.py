import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://hello.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://hello.com")
        node3 = TextNode("This is a text node", TextType.BOLD, "https://hello.com")
        node4 = TextNode("This is a text node", TextType.BOLD, "https://hello.com")
        self.assertEqual(node, node2)
        self.assertEqual(node2, node3)
        self.assertEqual(node3, node4)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Hello, world!")

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Click me!", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(), '<a href="https://example.com">Click me!</a>'
        )

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("A beautiful image", TextType.IMAGE, url="image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(), '<img src="image.jpg" alt="A beautiful image" />'
        )

    def test_text_node_to_html_node_missing_url_for_link(self):
        text_node = TextNode("Click me!", TextType.LINK)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Link nodes must have a URL")

    def test_text_node_to_html_node_missing_url_for_image(self):
        text_node = TextNode("An image", TextType.IMAGE)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Image nodes must have a URL")

    def test_text_node_to_html_node_invalid_type(self):
        text_node = TextNode("Unsupported", "unsupported_type")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertIn("Unsupported TextType", str(context.exception))


if __name__ == "__main__":
    unittest.main()
