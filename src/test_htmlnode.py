import unittest

from htmlnode import *

class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "value", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"", node.props_to_html())
    
    def test_to_html_leaf(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 =LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual("<p>This is a paragraph of text.</p>", node.to_html())
        self.assertEqual("<a href=\"https://www.google.com\">Click me!</a>", node2.to_html())
    
    def test_to_html_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        html = node.to_html()

        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", html)



if __name__ == "__main__":
    unittest.main()