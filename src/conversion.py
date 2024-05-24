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