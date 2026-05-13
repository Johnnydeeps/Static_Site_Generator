class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html not implemented")

    # helper function used below in to_html() for each child class
    def props_to_html(self):
        if self.props:
            result = ""
            for key, value in self.props.items():
                result += f' {key}="{value}"'
            return result
        else:
            return ""


class LeafNode(HTMLNode):
    # controls what the caller must provide as arguements to run
    def __init__(self, tag, value, props=None):
        # controls what is passed up to HTMLNode
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("All parent nodes must have a child or children.")
        else:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()

            return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
