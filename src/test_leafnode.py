import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_simple_tag(self):
        node = LeafNode("p", "Lorem Ipsum")
        self.assertEqual("<p>Lorem Ipsum</p>", node.to_html())

    def test_tag_with_props(self):
        node = LeafNode("a", "Call to action", {"href": "https://www.boot.dev"})
        self.assertEqual('<a href="https://www.boot.dev">Call to action</a>', node.to_html())

    def test_no_tag(self):
        node = LeafNode(None, "Some raw text")
        self.assertEqual("Some raw text", node.to_html())


if __name__ == "__main__":
    unittest.main()
