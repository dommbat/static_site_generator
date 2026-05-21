from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGES = "images"

class TextNode:
    def __init__(self, text: str, type: TextType = TextType.TEXT, link: str = None):
        self.text = text
        self.type = type
        self.link = link

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.type == other.type and self.link == other.link
    def __repr__(self):
        return f"TextNode('{self.text}', '{self.type}', '{self.link}')"

def text_node_to_html_node(text_node):
    if text_node.type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.link})
    elif text_node.type == TextType.IMAGES:
        return LeafNode("img", None, {"src": text_node.link})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.type}")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type): 
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                    raise ValueError(f"Delimiter '{delimiter}' appears an even number of times in text: '{node.text}'")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:  
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes