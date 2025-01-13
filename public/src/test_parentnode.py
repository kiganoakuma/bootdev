import unittest
from textwrap import dedent
from htmlnode import ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_parent_parent_with_children(self):
        # Creating nodes
        l_node1 = LeafNode("p", "This is paragraph element")
        l_node2 = LeafNode(None, "This is paragraph element")
        l_node3 = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        p_node1 = ParentNode(
            "div",
            [l_node1, l_node2, l_node3],
            {
                "className": "p_node1",
            },
        )
        p_node2 = ParentNode("div", [p_node1], {"className": "p_node2"})
        p_node3 = ParentNode("div", [p_node2], {"className": "p_node3"})
        expected_html = dedent(
            """
        <div className="p_node3">
            <div className="p_node2">
                <div className="p_node1">
                    <p>This is paragraph element</p>
                    This is paragraph element
                    <a href="https://www.google.com">Click me!</a>
                </div>
            </div>
        </div>
        """
        )

        self.assertEqual(
            p_node3.to_html(), expected_html.strip()
        )  # Correct expected output

    def test_parent_with_children_with_children(self):
        # Creating nodes
        l_node1 = LeafNode("p", "This is paragraph element")
        l_node2 = LeafNode(None, "This is paragraph element")
        l_node3 = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        p_node1 = ParentNode(
            "div",
            [l_node1, l_node2, l_node3],
            {
                "className": "p_node1",
            },
        )
        p_node2 = ParentNode(
            "div",
            [
                p_node1,
                l_node1,
                l_node2,
                l_node3,
            ],
            {"className": "p_node2"},
        )
        p_node3 = ParentNode("div", [p_node2], {"className": "p_node3"})
        expected_html = dedent(
            """
        <div className="p_node3">
            <div className="p_node2">
                <div className="p_node1">
                    <p>This is paragraph element</p>
                    This is paragraph element
                    <a href="https://www.google.com">Click me!</a>
                </div>
                <p>This is paragraph element</p>
                This is paragraph element
                <a href="https://www.google.com">Click me!</a>
            </div>
        </div>
        """
        )

        self.assertEqual(
            p_node3.to_html(), expected_html.strip()
        )  # Correct expected output

    def test_parent_node_without_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)  # Attempt to create a ParentNode with no children
        self.assertEqual(
            str(context.exception), "Parent class must have children"
        )  # Check the error message is correct

    def test_parent_node_without_tag(self):
        l_node1 = LeafNode("p", "This is paragraph element")
        p_node1 = ParentNode(
            "div",
            [l_node1],
            {
                "className": "p_node1",
            },
        )

        with self.assertRaises(ValueError) as context:
            ParentNode(
                None, [p_node1]
            )  # Attempt to create a ParentNode with no children
        self.assertEqual(
            str(context.exception), "Must provide element tag"
        )  # Check the error message is correct

    def test_parent_node_with_many_children(self):
        children = [LeafNode("p", f"Child {i}") for i in range(100)]
        node = ParentNode("div", children)
        expected_html = (
            "<div>\n"
            + "".join(f"    <p>Child {i}</p>\n" for i in range(100))
            + "</div>"
        )
        self.assertEqual(node.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
