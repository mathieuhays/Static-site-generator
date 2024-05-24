import unittest

from block import (
    block_type_unordered_list,
    block_type_quote,
    block_type_code,
    block_type_heading,
    block_type_paragraph,
    block_type_ordered_list,
    block_to_block_type
)


class TestBlock(unittest.TestCase):

    def test_block_conversion_heading(self):
        self.assertEqual(
            block_type_heading,
            block_to_block_type("# Heading")
        )

    def test_block_conversion_code(self):
        self.assertEqual(
            block_type_code,
            block_to_block_type("```print('Hello world')```"),
            "expect valid code block"
        )

        self.assertEqual(
            block_type_paragraph,
            block_to_block_type("```print('Hello world')"),
            "expect malformed code block falling back to paragraph"
        )

    def test_block_conversion_quote(self):
        self.assertEqual(
            block_type_quote,
            block_to_block_type("> lorem\n> Ipsum"),
            "expect valid quote block"
        )

        self.assertEqual(
            block_type_paragraph,
            block_to_block_type("> starts as a quote\n- but end up being malformed"),
            "expect malformed quote falling back to paragraph"
        )

    def test_block_conversion_ul(self):
        self.assertEqual(
            block_type_unordered_list,
            block_to_block_type("- item 1\n- item 2"),
            "expect valid unordered list using dash"
        )

        self.assertEqual(
            block_type_unordered_list,
            block_to_block_type("* item 1\n* item 2"),
            "expect valid unordered list using star"
        )

        self.assertEqual(
            block_type_paragraph,
            block_to_block_type("- item 1\n> item 2"),
            "expect malformed list falling back to paragraph"
        )

    def test_block_conversion_ol(self):
        self.assertEqual(
            block_type_ordered_list,
            block_to_block_type("1. item 1\n2. item 2"),
            "expect valid ordered list"
        )

        self.assertEqual(
            block_type_paragraph,
            block_to_block_type("2. item 1\n5. item 2"),
            "expect malformed ordered list falling back to paragraph"
        )

    def test_block_conversion_paragraph(self):
        self.assertEqual(block_type_paragraph, block_to_block_type("Some text here"))
        self.assertEqual(
            block_type_paragraph,
            block_to_block_type("Some text\nwith multiple lines")
        )



if __name__ == "__main__":
    unittest.main()
