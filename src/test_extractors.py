import unittest

from extractors import extract_markdown_images, extract_markdown_links, extract_title


class TestExtractors(unittest.TestCase):

    def test_image_extractor(self):
        expected = [
            ("alt text", "https://example.com/image.jpeg"),
            ("helpful description", "http://some.net/website.webp")
        ]
        test_string = ("Lorem ![alt text](https://example.com/image.jpeg). Ipsum [link](https://example.com) Dolor. ![helpful description](http://some.net/website.webp)")
        self.assertEqual(expected, extract_markdown_images(test_string))

    def test_link_extractor(self):
        expected = [
            ("homepage", "https://example.com"),
            ("contact page", "https://example.com/contact")
        ]
        test_string = ("Lorem [homepage](https://example.com). Ipsum Dolor. [contact page](https://example.com/contact)")
        self.assertEqual(expected, extract_markdown_links(test_string))

        test2 = "[Back Home](/)"
        expected = [("Back Home", "/")]
        self.assertEqual(expected, extract_markdown_links(test2))

    def test_title_extractor(self):
        test_string = "# Lorem Ipsum"
        self.assertEqual("Lorem Ipsum", extract_title(test_string))

        test2 = "Some text\n# test\nanother test"
        self.assertEqual("test", extract_title(test2))


if __name__ == "__main__":
    unittest.main()
