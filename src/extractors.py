import re


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.*?)]\((.*?)\)", text)


def extract_title(markdown):
    parts = re.findall(r"(?m)^# (.*)$", markdown)
    if len(parts) == 0:
        raise Exception("No title found")
    return parts[0]
