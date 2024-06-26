import unittest

from src.leafnode import LeafNode
from textnode import TextNode, text_type_bold, text_type_text


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq_type_diff(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_text_diff(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node2", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Some text", text_type_text, "https://www.boot.dev")
        node2 = TextNode("Some text", text_type_text, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("my text", text_type_text, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(my text, text, https://www.boot.dev)")


if __name__ == "__main__":
    unittest.main()
