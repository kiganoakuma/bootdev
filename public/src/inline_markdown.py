from textnode import TextType, TextNode
import re


def extract_markdown_images(text):
    match = re.search(r"\!\[(.*?)\]\((.*?)\)", text)
    # Extract the matched part
    if match:
        ignore = match.group(0)
        text_ = match.group(1)  # Only the content: "bold text"
        url_str = match.group(2)

        return ((text_, url_str),)
    else:
        raise ValueError("No images found in text")


def extract_markdown_links(text):
    match = re.search(r"\[(.*?)\]\((.*?)\)", text)
    # Extract the matched part
    if match:
        ignore = match.group(0)
        text_ = match.group(1)  # Only the content: "bold text"
        url_str = match.group(2)

        return ((text_, url_str),)
    else:
        raise ValueError("No links found in text")


def split_nodes_delimeter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        text = node.text
        match_types = {
            "**": re.search(r"\*\*(.*?)\*\*", text),
            "__": re.search(r"__(.*?)__", text),
            "*": re.search(r"\*(.*?)\*", text),
            "_": re.search(r"_(.*?)_", text),
            "`": re.search(r"\`(.*?)\`", text),
        }
        match = match_types[delimiter]
        if match:
            # Extract the matched part
            matched_text = match.group(0)  # Entire match: "**bold text**"
            inner_text = match.group(1)  # Only the content: "bold text"

            # "Pop" the matched part by slicing the text
            pre_text, post_text = text[: match.start()], text[match.end() :]

            new_nodes.extend(
                [
                    TextNode(pre_text, TextType.TEXT),
                    TextNode(inner_text, text_type),
                    TextNode(post_text, TextType.TEXT),
                ]
            )
        else:
            raise ValueError("Markdown format for delimiter: {delimiter} not found")

    return new_nodes
