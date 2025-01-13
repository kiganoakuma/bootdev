from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode


def main():

    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)

    leaf_node = LeafNode(
        "a",
        "hello world!",
        props={"href": "https://www.google.com", "target": "_blank"},
    )

    print(LeafNode.to_html(leaf_node))


if __name__ == "__main__":
    main()
