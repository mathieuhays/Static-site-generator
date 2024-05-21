from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag missing on parent node")
        if self.children is None or len(self.children) == 0:
            raise ValueError("missing children in parent node")

        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
