class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}
    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented for HTMLNode")
    def props_to_html(self) -> str:
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str
    def __repr__(self):
        return f"HTMLNode('{self.tag}', '{self.value}', {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None):
        super().__init__(tag, value, [], props)
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode('{self.tag}', '{self.value}', {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        super().__init__(tag, value, children, props)
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    def __repr__(self):
        return f"ParentNode('{self.tag}', '{self.value}', {self.children}, {self.props})"