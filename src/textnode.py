from enum import Enum
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGES = "images"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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
    from htmlnode import LeafNode

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
        return LeafNode("img", "", {"src": text_node.link, "alt": text_node.text})
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

def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_pattern, text)

def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.type == TextType.TEXT:
            remaining_text = node.text
            images = extract_markdown_images(node.text)
            for image_alt, image_url in images:
                remaining_text = remaining_text.split(f"![{image_alt}]({image_url})", 1)
                if remaining_text[0]:
                    new_nodes.append(TextNode(remaining_text[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGES, image_url))
                remaining_text = remaining_text[1]
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.type == TextType.TEXT:
            remaining_text = node.text
            links = extract_markdown_links(node.text)
            for link_text, link_url in links:
                remaining_text = remaining_text.split(f"[{link_text}]({link_url})", 1)
                if remaining_text[0]:
                    new_nodes.append(TextNode(remaining_text[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                remaining_text = remaining_text[1]
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    if block.startswith("# "):
        return BlockType.HEADING
    elif block.startswith("## "):
        return BlockType.HEADING
    elif block.startswith("### "):
        return BlockType.HEADING
    elif block.startswith("#### "):
        return BlockType.HEADING
    elif block.startswith("##### "):
        return BlockType.HEADING
    elif block.startswith("###### "):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block and block[0].isdigit() and block[1:3] == ". ":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def extract_title(markdown):
    """Extract the h1 header from markdown content.
    
    Returns the text of the h1 header (line starting with single #).
    Raises ValueError if no h1 header is found.
    """
    lines = markdown.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            return stripped[2:].strip()
    raise ValueError("No h1 header found in markdown")

    