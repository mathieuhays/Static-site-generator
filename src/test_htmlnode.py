import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_prop_to_html(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(' href="https://www.boot.dev" target="_blank"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode("div", "test")
        self.assertEqual("HTMLNode(tag=div, value=test, children=None, props=None)", repr(node))


if __name__ == "__main__":
    unittest.main()
