from pathlib import Path

from markdown_blocks import markdown_to_blocks, markdown_to_html_node
from pub_update import copy_files, wipe_dir_contents


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    h1_header = [block[2:] for block in blocks if block.startswith("# ")]
    if h1_header:
        return h1_header[0]
    else:
        raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        markdown_contents = Path(from_path).read_text(encoding="utf-8")
        h1_header = extract_title(markdown_contents)
        node = markdown_to_html_node(markdown_contents)
        html_content = node.to_html()

        html = Path(template_path).read_text(encoding="utf-8")
        filled_template = html.replace("{{ Content }}", html_content)
        filled_template = filled_template.replace("{{ Title }}", h1_header)

        Path(dest_path).write_text(filled_template, encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Error: Could not find file: {e.filename}")
    except Exception as e:
        print(f"Error Generating page: {e}")


def main():
    static_dir = "./static"
    pub_dir = "./public"
    wipe_dir_contents(pub_dir)
    copy_files(static_dir, pub_dir)
    from_path = "./content/index.md"
    dest_path = "./public/index.html"
    template_path = "./template.html"
    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
