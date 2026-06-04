import os

from markdown_to_blocks import markdown_to_html_node


def extract_title(markdown_text):
    lines = markdown_text.split("\n")

    for line in lines:
        if line.startswith("# "):
            title_text = line[2:]
            striped_title_text = title_text.strip()
            return striped_title_text
    raise Exception("no title found in markdown text")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    open_contents = open(from_path)
    contents = open_contents.read()
    open_contents.close()

    open_contents_template = open(template_path)
    contents_template = open_contents_template.read()
    open_contents_template.close()

    contents_html_nodes = markdown_to_html_node(contents)
    html_string = contents_html_nodes.to_html()
    title = extract_title(contents)

    replaced_title = contents_template.replace("{{ Title }}", title)
    replaced_html_string = replaced_title.replace("{{ Content }}", html_string)

    dir_name = os.path.dirname(dest_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    open_dest_path_file = open(dest_path, "w")
    open_dest_path_file.write(replaced_html_string)
    open_dest_path_file.close()
