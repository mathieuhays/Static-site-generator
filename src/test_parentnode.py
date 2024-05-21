import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("p", [
            LeafNode(None, "test"),
            LeafNode("b", "bold")
        ])
        self.assertEqual("<p>test<b>bold</b></p>", node.to_html())

    def test_nested(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "test")
            ])
        ])

        self.assertEqual("<div><p>test</p></div>", node.to_html())

    def test_multi_nested(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode("i", "italic")
            ]),
            LeafNode("u", "underline")
        ])
        self.assertEqual("<div><p><i>italic</i></p><u>underline</u></div>", node.to_html())


if __name__ == "__main__":
    unittest.main()
