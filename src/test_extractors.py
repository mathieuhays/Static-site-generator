import unittest

from extractors import extract_markdown_images, extract_markdown_links


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
        test_string = ("Lorem [homepage](https://example.com). Ipsum ![image](https://example.com/image.jpeg) Dolor. [contact page](https://example.com/contact)")
        self.assertEqual(expected, extract_markdown_links(test_string))

if __name__ == "__main__":
    unittest.main()
