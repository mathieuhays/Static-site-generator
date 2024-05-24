import os.path

from conversion import markdown_to_html_node
from extractors import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    source_file = open(from_path)
    source_content = source_file.read()
    source_file.close()

    tpl_file = open(template_path)
    tpl_content = tpl_file.read()
    tpl_file.close()

    html_node = markdown_to_html_node(source_content)
    html = html_node.to_html()

    title = extract_title(source_content)

    tpl_with_title = tpl_content.replace('{{ Title }}', title)
    rendered = tpl_with_title.replace('{{ Content }}', html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    dest_file = open(dest_path, 'w')
    dest_file.write(rendered)
    dest_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)

    for item in items:
        content_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item.replace('.md', '.html'))

        if os.path.isdir(content_item_path):
            generate_pages_recursive(content_item_path, template_path, dest_item_path)
        else:
            generate_page(content_item_path, template_path, dest_item_path)
