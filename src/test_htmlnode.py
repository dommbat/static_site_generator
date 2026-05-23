from htmlnode import *
from textnode import *
import unittest 

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello World", [], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})
    def test_repr(self):
        node = HTMLNode("div", "Hello World", [], {"class": "container"})
        self.assertEqual(repr(node), "HTMLNode('div', 'Hello World', [], {'class': 'container'})")
    def test_props_to_html(self):
        node = HTMLNode("div", "Hello World", [], {"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!", {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container">Hello, world!</div>')
    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "LeafNode('p', 'Hello, world!', {})")
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", None, [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", None, [grandchild_node])
        parent_node = ParentNode("div", None, [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )  
if __name__ == "__main__":
    unittest.main()