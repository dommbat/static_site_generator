import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertEqual(repr(node), "TextNode('This is a text node', 'TextType.BOLD', 'https://www.google.com')")
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_split_nodes_delimiter(self):
        node = TextNode("This is a text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], " ", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[1].text, "is")
        self.assertEqual(new_nodes[2].text, "a")
        self.assertEqual(new_nodes[3].text, "text")
        self.assertEqual(new_nodes[4].text, "node")
if __name__ == "__main__":
    unittest.main()