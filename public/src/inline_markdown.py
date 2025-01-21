from textnode import TextType, TextNode
import re


def split_node_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        # Extract the matched part
        while True:
            match = re.search(r"\!\[(.*?)\]\((.*?)\)", text)
            if not match:
                break

            ignore = match.group(0)
            text_ = match.group(1)  # Only the content: "bold text"
            url_str = match.group(2)
            new_nodes.extend(
                [
                    TextNode(text[: match.start()], TextType.TEXT),
                    TextNode(text_, TextType.IMAGE, url_str),
                ]
            )
            text = text[match.end() :]
        if text != "":
            new_nodes.extend([TextNode(text, TextType.TEXT)])
        else:
            raise ValueError("No images found in text")
    return new_nodes


def split_node_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        # Extract the matched part
        while True:
            match = re.search(r"\[(.*?)\]\((.*?)\)", text)
            if not match:
                break

            ignore = match.group(0)
            text_ = match.group(1)  # Only the content: "bold text"
            url_str = match.group(2)
            new_nodes.extend(
                [
                    TextNode(text[: match.start()], TextType.TEXT),
                    TextNode(text_, TextType.LINK, url_str),
                ]
            )
            text = text[match.end() :]
        if text != "":
            new_nodes.extend([TextNode(text, TextType.TEXT)])
        else:
            raise ValueError("No images found in text")
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.extend([node])
        text = node.text
        match_types = {
            "**": r"\*\*(.*?)\*\*",
            "__": r"__(.*?)__",
            "*": r"\*(.*?)\*",
            "_": r"_(.*?)_",
            "`": r"\`(.*?)\`",
        }

        count = 0
        for idx, val in enumerate(text):
            if val == delimiter:
                count += 1
        if count % 2 != 0:
            raise ValueError("Mismatched delimiter")

        while True:
            match = re.search(match_types[delimiter], text)
            if not match:
                break
            matched_text = match.group(0)
            inner_text = match.group(1)

            pre_text, post_text = text[: match.start()], text[match.end() :]

            new_nodes.extend(
                [
                    TextNode(pre_text, TextType.TEXT),
                    TextNode(inner_text, text_type),
                ]
            )
            text = post_text
        if text != "":
            new_nodes.extend([TextNode(text, TextType.TEXT)])

    return new_nodes
