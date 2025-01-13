class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        if self.tag == "link":  # Handle self-closing tags
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        super().__init__(tag, None, children, props)
        if self.tag is None:
            raise ValueError("Must provide element tag")
        if self.children is None:
            self.children = []
        if self.children == []:
            raise ValueError("Parent class must have children")

    def to_html(self, indent=0):

        # Indentation for current tag
        indent_space = " " * indent
        # Indentation for children
        child_indent = indent + 4

        # Recursively generate HTML for children with indentation
        children_html = "\n".join(
            (
                child.to_html(child_indent)
                if isinstance(child, ParentNode)
                else f"{' ' * child_indent}{child.to_html()}"
            )
            for child in self.children
        )

        # Format the current node with its children
        return f"{indent_space}<{self.tag}{self.props_to_html()}>\n{children_html}\n{indent_space}</{self.tag}>"
