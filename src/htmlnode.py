class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method is not implemented")

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""

        attributes = ""
        for key in self.props:
            value = self.props[key]
            attributes += f" {key}=\"{value}\""

        return attributes

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
