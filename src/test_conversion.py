import unittest

from conversion import (text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link,
                        text_to_text_nodes, markdown_to_blocks, block_to_heading, block_to_code, block_to_list,
                        block_to_quote, block_to_paragraph, markdown_to_html_node)
from leafnode import LeafNode
from textnode import TextNode, text_type_bold, text_type_text, text_type_italic, text_type_image, text_type_link, \
    text_type_code
from parentnode import ParentNode


class TestConversion(unittest.TestCase):

    def test_text_to_html_node(self):
        text_node = TextNode("some text", text_type_bold)
        expected = LeafNode("b", "some text")
        self.assertEqual(expected, text_node_to_html_node(text_node), "expect bold TN to convert to bold LN")

        text_node2 = TextNode("other text", text_type_text)
        expected2 = LeafNode(None, "other text")
        self.assertEqual(expected2, text_node_to_html_node(text_node2), "expect text TN to convert to LN with no tag")

    def test_split_middle_delimiter(self):
        test_node = TextNode("Some text with **bold** text", text_type_text)
        expected = [
            TextNode("Some text with ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text)
        ]
        self.assertEqual(
            expected,
            split_nodes_delimiter([test_node], "**", text_type_bold)
        )

    def test_split_starting_delimiter(self):
        test_node = TextNode("**bold** other text", text_type_text)
        expected = [
            TextNode("bold", text_type_bold),
            TextNode(" other text", text_type_text)
        ]
        self.assertEqual(
            expected,
            split_nodes_delimiter([test_node], "**", text_type_bold)
        )

    def test_split_ending_delimiter(self):
        test_node = TextNode("other text **bold**", text_type_text)
        expected = [
            TextNode("other text ", text_type_text),
            TextNode("bold", text_type_bold)
        ]
        self.assertEqual(
            expected,
            split_nodes_delimiter([test_node], "**", text_type_bold)
        )

    def test_split_multi_node_input(self):
        test_nodes = [
            TextNode("**lorem** ipsum", text_type_text),
            TextNode("Dolor", text_type_text),
            TextNode("some other text **bold** test", text_type_text)
        ]
        expected = [
            TextNode("lorem", text_type_bold),
            TextNode(" ipsum", text_type_text),
            TextNode("Dolor", text_type_text),
            TextNode("some other text ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" test", text_type_text)
        ]
        self.assertEqual(
            expected,
            split_nodes_delimiter(test_nodes, '**', text_type_bold)
        )

    def test_split_skip_already_processed_nodes(self):
        test_nodes = [
            TextNode("Some text ", text_type_text),
            TextNode("bold *italic* yo", text_type_bold),
            TextNode(" with another *italics*", text_type_text)
        ]

        expected = [
            TextNode("Some text ", text_type_text),
            TextNode("bold *italic* yo", text_type_bold),
            TextNode(" with another ", text_type_text),
            TextNode("italics", text_type_italic)
        ]

        self.assertEqual(
            expected,
            split_nodes_delimiter(test_nodes, '*', text_type_italic)
        )

    def test_split_multiple_occurrence_in_one_node(self):
        test_node = TextNode("**test** other **bold** text **here**", text_type_text)
        expected = [
            TextNode("test", text_type_bold),
            TextNode(" other ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text ", text_type_text),
            TextNode("here", text_type_bold)
        ]

        self.assertEqual(
            expected,
            split_nodes_delimiter([test_node], '**', text_type_bold)
        )

    def test_split_raise_on_invalid_input(self):
        test_node = TextNode("Some **invalid input", text_type_text)
        self.assertRaises(Exception, lambda: split_nodes_delimiter([test_node], '**', text_type_bold))

    def test_split_images(self):
        test_node = TextNode(
            "Hello there ![alt text](https://example.com/image.jpeg)! Another: ![test](/image.jpeg)",
            text_type_text
        )
        expected = [
            TextNode("Hello there ", text_type_text),
            TextNode("alt text", text_type_image, "https://example.com/image.jpeg"),
            TextNode("! Another: ", text_type_text),
            TextNode("test", text_type_image, "/image.jpeg")
        ]
        self.assertEqual(expected, split_nodes_image([test_node]))

    def test_split_links(self):
        test_node = TextNode(
            "Lorem Ipsum [click here](https://test.com). [read more](/articles)",
            text_type_text
        )
        expected = [
            TextNode("Lorem Ipsum ", text_type_text),
            TextNode("click here", text_type_link, "https://test.com"),
            TextNode(". ", text_type_text),
            TextNode("read more", text_type_link, "/articles")
        ]
        self.assertEqual(expected, split_nodes_link([test_node]))

        test2 = TextNode("[Back Home](/)", text_type_text)
        expected = [TextNode("Back Home", text_type_link, "/")]
        self.assertEqual(expected, split_nodes_link([test2]))

    def test_text_to_nodes(self):
        test_string = "This is **text** with an *italic* word and a `code block` and an ![image](/img.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "/img.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ]
        self.assertEqual(expected, text_to_text_nodes(test_string))

    def test_markdown_to_block(self):
        test_input = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """
        expected = [
            "This is **bolded** paragraph",
            (
                "This is another paragraph with *italic* text and `code` here\n"
                "This is the same paragraph on a new line"
            ),
            (
                "* This is a list\n"
                "* with items"
            )
        ]
        self.assertEqual(expected, markdown_to_blocks(test_input))

    def test_block_to_heading(self):
        content = "### Heading *italic* test"
        expected = ParentNode("h3", [
            LeafNode(None, "Heading "),
            LeafNode("i", "italic"),
            LeafNode(None, " test")
        ])
        self.assertEqual(expected, block_to_heading(content))

    def test_block_to_code(self):
        content = "```\nbody { color: #fff; }\n```"
        expected = ParentNode("pre", [
            ParentNode("code", [
                LeafNode(None, "body { color: #fff; }")
            ])
        ])
        self.assertEqual(expected, block_to_code(content))

    def test_block_to_list_ul(self):
        content = "- item 1\n- item 2\n- item 3"
        expected = ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "item 1")]),
            ParentNode("li", [LeafNode(None, "item 2")]),
            ParentNode("li", [LeafNode(None, "item 3")])
        ])
        self.assertEqual(expected, block_to_list(content, "ul"))

    def test_block_to_list_ol(self):
        content = "1. item 1\n2. item 2\n3. item 3"
        expected = ParentNode("ol", [
            ParentNode("li", [LeafNode(None, "item 1")]),
            ParentNode("li", [LeafNode(None, "item 2")]),
            ParentNode("li", [LeafNode(None, "item 3")])
        ])
        self.assertEqual(expected, block_to_list(content, "ol"))

    def test_block_to_quote(self):
        content = "> Lorem Ipsum\n> Dolor"
        expected = ParentNode("blockquote", [
            LeafNode(None, "Lorem Ipsum\nDolor")
        ])
        self.assertEqual(expected, block_to_quote(content))

    def test_block_to_paragraph(self):
        content = "Some content"
        expected = ParentNode("p", [LeafNode(None, "Some content")])
        self.assertEqual(expected, block_to_paragraph(content))

    def test_markdown_to_html_node(self):
        content = """
# Heading

Lorem **Ipsum** Dolor

- list *item* 1
- list `item` 2
        """
        expected = ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "Heading")]),
            ParentNode("p", [
                LeafNode(None, "Lorem "),
                LeafNode("b", "Ipsum"),
                LeafNode(None, " Dolor")
            ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "list "),
                    LeafNode("i", "item"),
                    LeafNode(None, " 1")
                ]),
                ParentNode("li", [
                    LeafNode(None, "list "),
                    LeafNode("code", "item"),
                    LeafNode(None, " 2")
                ])
            ])
        ])
        self.assertEqual(expected, markdown_to_html_node(content))


if __name__ == "__main__":
    unittest.main()
