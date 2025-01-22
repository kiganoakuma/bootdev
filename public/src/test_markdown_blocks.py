import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """
# Heading

## Heading

### Heading

#### Heading

##### Heading

###### Heading

```This is code```

- unordered list

* unordered list

. ordered list

> quote

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line
"""
        blocks = markdown_to_blocks(md)
        types = []
        for block in blocks:
            types.append(block_to_block_type(block))
        self.assertEqual(
            types,
            [
                "heading",
                "heading",
                "heading",
                "heading",
                "heading",
                "heading",
                "code",
                "unordered_list",
                "unordered_list",
                "ordered_list",
                "quote",
                "paragraph",
            ],
        )


if __name__ == "__main__":
    unittest.main()
