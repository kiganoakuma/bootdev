import re
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, split_node_image, split_node_link


text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"


def text_to_textnodes(text):
    nodes = []
    new_text = ""
    match_types = {
        "bold": r"\*\*(.*?)\*\*",
        "bold_": r"__(.*?)__",
        "italic": r"\*(.*?)\*",
        "italic_": r"_(.*?)_",
        "code": r"\`(.*?)\`",
        "image": r"\!\[(.*?)\]\((.*?)\)",
        "link": r"\[(.*?)\]\((.*?)\)",
    }

    for type, pattern in match_types.items():
        while True:
            match = re.search(pattern, text)
            if not match:
                break
            matched_text = match.group(0)
            inner_text = match.group(1)

            pre_text, post_text = text[: match.start()], text[match.end() :]
            new_text = new_text + pre_text + matched_text + "|" + type + "\n"
            text = post_text

    lines = new_text.split("\n")
    text_types = {
        "bold": TextType.BOLD,
        "italic": TextType.ITALIC,
        "code": TextType.CODE,
        "link": TextType.LINK,
        "image": TextType.IMAGE,
    }
    for line in lines:
        if line == "":
            continue
        a = line.split("|")
        nodes.extend([TextNode(a[0], text_types[a[1]])])
    return nodes


lines = text_to_textnodes(text)
for line in lines:
    print(line)
