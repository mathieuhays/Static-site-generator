from leafnode import LeafNode
from textnode import (
    text_type_text,
    text_type_italic,
    text_type_bold,
    text_type_image,
    text_type_link,
    text_type_code,
    TextNode
)
from extractors import extract_markdown_links, extract_markdown_images
from block import (
    get_block_type,
    block_type_heading,
    block_type_paragraph,
    block_type_ordered_list,
    block_type_code,
    block_type_quote,
    block_type_unordered_list
)
from parentnode import ParentNode


def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            final.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) == 0:
            final.append(node)
            continue
        if len(parts) % 2 == 0:
            raise Exception("Invalid markup")

        if len(parts[0]) > 1:
            final.append(TextNode(parts[0], text_type_text))

        i = 1
        while i < len(parts):
            final.append(TextNode(parts[i], text_type))

            if i + 1 < len(parts) and len(parts[i + 1]) > 0:
                final.append(TextNode(parts[i + 1], text_type_text))

            i += 2

    return final


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        node_text = node.text
        images = extract_markdown_images(node_text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for alt_text, image_url in images:
            parts = node_text.split(f"![{alt_text}]({image_url})", 1)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(TextNode(alt_text, text_type_image, image_url))
            node_text = parts[1]

        if node_text != "":
            new_nodes.append(TextNode(node_text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node_text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link_text, link_href in links:
            parts = node_text.split(f"[{link_text}]({link_href})", 1)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(TextNode(link_text, text_type_link, link_href))
            node_text = parts[1]

        if node_text != "":
            new_nodes.append(TextNode(node_text, text_type_text))

    return new_nodes


def text_to_text_nodes(text):
    nodes = split_nodes_link([TextNode(text, text_type_text)])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    return nodes


def markdown_to_blocks(text):
    blocks = []
    lines = text.split("\n\n")

    for line in lines:
        stripped = line.strip()
        if stripped == "":
            continue

        blocks.append(stripped)

    return blocks


def block_to_heading(block):
    markup, text = block.split(' ', 1)
    heading_num = len(markup)
    return ParentNode(f"h{heading_num}", text_to_text_nodes(text))


def block_to_code(block):
    return ParentNode("pre", [
        ParentNode("code", text_to_text_nodes(block.strip("```").strip()))
    ])


def block_to_list(block, list_tag):
    nodes = []

    for line in block.split("\n"):
        nodes.append(ParentNode("li", text_to_text_nodes(line.split(' ', 1)[1])))

    return ParentNode(list_tag, nodes)


def block_to_quote(block):
    content = []
    for line in block.split("\n"):
        content.append(line[2:])

    return ParentNode("blockquote", text_to_text_nodes("\n".join(content)))


def block_to_paragraph(block):
    return ParentNode("p", text_to_text_nodes(block))


def block_to_html_node(block):
    block_type = get_block_type(block)

    if block_type == block_type_heading:
        return block_to_heading(block)
    if block_type == block_type_code:
        return block_to_code(block)
    if block_type == block_type_unordered_list:
        return block_to_list(block, "ul")
    if block_type == block_type_ordered_list:
        return block_to_list(block, "ol")
    if block_type == block_type_quote:
        return block_to_quote(block)
    if block_type == block_type_paragraph:
        return block_to_paragraph(block)

    raise ValueError("Invalid block type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = list(map(lambda b: block_to_html_node(b), blocks))
    return ParentNode("div", nodes)

