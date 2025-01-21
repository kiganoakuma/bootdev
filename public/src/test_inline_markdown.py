import unittest
from inline_markdown import (
    split_nodes_delimiter,  # or split_nodes_delimiter if that's your actual function name
    split_node_image,
    split_node_link,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_no_delimiter(self):
        """
        If the input text has no delimiter, it should just return the original node.
        """
        node = TextNode("This has no special delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This has no special delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_single_pair_of_backticks(self):
        """
        A single pair of backticks should split into three parts:
            - text before
            - code inside backticks
            - text after
        """
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_unmatched_delimiter(self):
        """
        When there's only a single backtick in the text, or an odd number,
        anything after the first delimiter remains as TEXT (no closing delimiter).
        """
        node = TextNode(
            "Unmatched delimiter here: `code block not closed", TextType.TEXT
        )
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Mismatched delimiter")

    def test_split_nodes_multiple_text_nodes(self):
        """
        If the input list has multiple text nodes, the function should process each one and return a combined new list.
        """
        nodes = [
            TextNode("Text with `code1`", TextType.TEXT),
            TextNode(" and another `code2` block", TextType.TEXT),
            TextNode(" plus plain text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 6)

    def test_image_split(self):
        node = TextNode(
            "This is text with an image ![alt text](www.google.com) embeded",
            TextType.TEXT,
        )

        extracted = split_node_image([node])
        expected_result = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "www.google.com"),
            TextNode(" embeded", TextType.TEXT),
        ]
        self.assertEqual(extracted, expected_result)

    def test_multi_image_split(self):
        node = TextNode(
            "This is text ![alt text](www.google.com) with an image ![alt text](www.google.com) embeded",
            TextType.TEXT,
        )

        extracted = split_node_image([node])
        expected_result = [
            TextNode("This is text ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "www.google.com"),
            TextNode(" with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "www.google.com"),
            TextNode(" embeded", TextType.TEXT),
        ]
        self.assertEqual(extracted, expected_result)

    def test_multi_node_image_split(self):
        node = TextNode(
            "This is text with an image ![alt text](www.google.com) embeded",
            TextType.TEXT,
        )
        node1 = TextNode(
            "This is text with an image ![alt text](www.google.com) embeded",
            TextType.TEXT,
        )

        extracted = split_node_image([node, node1])
        expected_result = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "www.google.com"),
            TextNode(" embeded", TextType.TEXT),
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "www.google.com"),
            TextNode(" embeded", TextType.TEXT),
        ]
        self.assertEqual(extracted, expected_result)

    def test_link_split(self):
        node = TextNode(
            "This is text with a [link](www.google.com) to an image", TextType.TEXT
        )

        extracted = split_node_link([node])
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.google.com"),
            TextNode(" to an image", TextType.TEXT),
        ]
        self.assertEqual(extracted, expected_result)

    def test_multi_link_split(self):
        node = TextNode(
            "This is [link](www.google.com) text with a [link](www.google.com) to an image",
            TextType.TEXT,
        )

        extracted = split_node_link([node])
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.google.com"),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.google.com"),
            TextNode(" to an image", TextType.TEXT),
        ]
        self.assertEqual(extracted, expected_result)

    def test_multi_node_link_split(self):
        node = TextNode(
            "This is text with a [link](www.google.com) to an image", TextType.TEXT
        )
        node1 = TextNode(
            "This is text with a [link](www.google.com) to an image", TextType.TEXT
        )

        extracted = split_node_link([node, node1])
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.google.com"),
            TextNode(" to an image", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.google.com"),
            TextNode(" to an image", TextType.TEXT),
        ]
        self.assertEqual(extracted, expected_result)


if __name__ == "__main__":
    unittest.main()
