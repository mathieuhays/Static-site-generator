from leafnode import LeafNode
from textnode import text_type_text, text_type_italic, text_type_bold, text_type_image, text_type_link, text_type_code, \
    TextNode


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
