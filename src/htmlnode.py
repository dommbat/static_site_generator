from textnode import BlockType, markdown_to_blocks, block_to_block_type, text_node_to_html_node, text_to_textnodes

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
    
def markdown_to_html_node(markdown_text):
    blocks = markdown_to_blocks(markdown_text)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            html_nodes.append(ParentNode("h1", None, [LeafNode(None, block[2:].strip())]))
        elif block_type == BlockType.PARAGRAPH:
            paragraph_text = block.replace("\n", " ")
            html_nodes.append(
                ParentNode(
                    "p",
                    None,
                    [text_node_to_html_node(node) for node in text_to_textnodes(paragraph_text)],
                )
            )
        elif block_type == BlockType.CODE:
            code_text = block[3:]
            if code_text.startswith("\n"):
                code_text = code_text[1:]
            if code_text.endswith("```"):
                code_text = code_text[:-3]
            html_nodes.append(ParentNode("pre", None, [LeafNode("code", code_text)]))
        elif block_type == BlockType.QUOTE:
            html_nodes.append(ParentNode("blockquote", None, [LeafNode(None, block[2:].strip())]))
        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            html_nodes.append(
                ParentNode(
                    "ul",
                    None,
                    [
                        ParentNode(
                            "li",
                            None,
                            [text_node_to_html_node(node) for node in text_to_textnodes(item[2:].strip())],
                        )
                        for item in items
                    ],
                )
            )
        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            html_nodes.append(
                ParentNode(
                    "ol",
                    None,
                    [
                        ParentNode(
                            "li",
                            None,
                            [text_node_to_html_node(node) for node in text_to_textnodes(item[3:].strip())],
                        )
                        for item in items
                    ],
                )
            )
    return ParentNode("div", None, html_nodes)
