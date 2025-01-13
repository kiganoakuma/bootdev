import unittest
from inline_markdown import (
    split_nodes_delimeter,  # or split_nodes_delimiter if that's your actual function name
    extract_markdown_images,
    extract_markdown_links,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_no_delimiter(self):
        """
        If the input text has no delimiter, it should just return the original node.
        """
        node = TextNode("This has no special delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)
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
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_multiple_pairs_of_backticks(self):
        """
        Multiple pairs of backticks in one node.
        Each pair should be interpreted separately, resulting in alternating TEXT and CODE nodes.
        """
        node = TextNode("Here is `code1` and more `code2` done", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Here is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "code1")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

        self.assertEqual(new_nodes[2].text, " and more ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[3].text, "code2")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

        self.assertEqual(new_nodes[4].text, " done")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_split_nodes_unmatched_delimiter(self):
        """
        When there's only a single backtick in the text, or an odd number,
        anything after the first delimiter remains as TEXT (no closing delimiter).
        """
        node = TextNode(
            "Unmatched delimiter here: `code block not closed", TextType.TEXT
        )
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)

        # We expect only two nodes, because after the first backtick we cannot find a closing one.
        # One approach is to consider everything after the opening delimiter as part of the original text (no actual code).
        # If your implementation differs, adjust the test accordingly.
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Unmatched delimiter here: ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        # The second piece might be "code block not closed" if your parser thinks it didn't find a closing backtick.
        # Or you might handle unmatched delimiters differently. Adjust if needed.
        self.assertEqual(new_nodes[1].text, "code block not closed")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_split_nodes_multiple_text_nodes(self):
        """
        If the input list has multiple text nodes, the function should process each one and return a combined new list.
        """
        nodes = [
            TextNode("Text with `code1`", TextType.TEXT),
            TextNode(" and another `code2` block", TextType.TEXT),
            TextNode(" plus plain text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimeter(nodes, "`", TextType.CODE)

        # We expect them all processed in order:
        # 1) "Text with " (TEXT)
        # 2) "code1" (CODE)
        # 3) " and another " (TEXT)
        # 4) "code2" (CODE)
        # 5) " block" (TEXT)
        # 6) " plus plain text" (TEXT)

        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code1")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "code2")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " block")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, " plus plain text")
        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)

    def test_split_nodes_different_delimiters(self):
        """
        Test that the function works for different delimiters and text types, such as bold (**),
        italic (*), code (`), etc. This assumes you've extended your function in some way
        or you are testing separate calls with different delimiters.
        """
        # Example: * = italic
        node_italic = TextNode("This *text* has italic markers", TextType.TEXT)
        new_nodes_italic = split_nodes_delimeter([node_italic], "*", TextType.ITALIC)

        self.assertEqual(len(new_nodes_italic), 3)
        self.assertEqual(new_nodes_italic[0].text, "This ")
        self.assertEqual(new_nodes_italic[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes_italic[1].text, "text")
        self.assertEqual(new_nodes_italic[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes_italic[2].text, " has italic markers")
        self.assertEqual(new_nodes_italic[2].text_type, TextType.TEXT)

        # Example: ** = bold
        node_bold = TextNode("Now we have **bold** text", TextType.TEXT)
        new_nodes_bold = split_nodes_delimeter([node_bold], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes_bold), 3)
        self.assertEqual(new_nodes_bold[0].text, "Now we have ")
        self.assertEqual(new_nodes_bold[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes_bold[1].text, "bold")
        self.assertEqual(new_nodes_bold[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes_bold[2].text, " text")
        self.assertEqual(new_nodes_bold[2].text_type, TextType.TEXT)


if __name__ == "__main__":
    unittest.main()
