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
    
    def test_markdown_to_blocks(self):
        markdown = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(expected, result)

    def test_markdown_to_blocks_whitespace(self):
        markdown = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\n\n\n\n\n\n\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here",
            "This is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(expected, result)
    
    def test_text_block_to_block_type(self):
        blocks = [
            "###### Heading",
            "```code block```",
            ">quote\n>quote",
            "* unordered list\n- unorderedlist",
            "1. ordered list\n2. ordered list\n3. ordered list",
            "########## normal paragraph",
            "> not q quote\n not a quote\n > not a quote"
        ]
        results = list(map(lambda block: block_to_block_type(block), blocks))
        expected = [
            block_type_heading,
            block_type_code,
            block_type_quote,
            block_type_unordered_list,
            block_type_ordered_list,
            block_type_paragraph,
            block_type_paragraph
        ]
        self.assertEqual(results, expected)

    def test_heading_block_to_htmlnode(self):
        block = "###### Heading"
        result = heading_block_to_htmlnode(block)
        expected = LeafNode("h6", "Heading")
        self.assertEqual(expected, result)

    def test_code_block_to_htmlnode(self):
        block = "```code block```"
        result = code_block_to_htmlnode(block)
        expected = ParentNode("pre", [LeafNode("code", "code block")])
        self.assertEqual(result, expected)

    def test_quote_block_to_htmlnode(self):
        block = ">quote\n>quote"
        result = quote_block_to_htmlnode(block)
        expected = ParentNode("blockquote", [LeafNode("p", "quote\n"), LeafNode("p", "quote")])
        self.assertEqual(expected, result)

    def test_unordered_list_block_to_htmlnode(self):
        block = "* unordered list\n- unorderedlist"
        result = unordered_list_block_to_htmlnode(block)
        expected = ParentNode("ul", [LeafNode("li", " unordered list"), LeafNode("li", " unorderedlist")])
        self.assertEqual(expected, result)

    def test_ordered_list_block_to_htmlnode(self):
        block = "1. ordered list\n2. ordered list\n3. ordered list"
        result = ordered_list_block_to_htmlnode(block)
        expected = ParentNode("ol", [LeafNode("li", " ordered list"), LeafNode("li", " ordered list"), LeafNode("li", " ordered list")])
        self.assertEqual(expected, result)

    def test_paragraph_block_to_htmlnode(self):
        block = "########## normal paragraph"
        result = paragraph_block_to_htmlnode(block)
        expected = LeafNode("p", block)
        self.assertEqual(expected, result)
    
    def test_markdown_to_html_node(self):
        markdown = "###### Heading\n\n```code block```\n\n>quote\n>quote\n\n* unordered list\n- unorderedlist\n\n1. ordered list\n2. ordered list\n3. ordered list\n\n########## normal paragraph\n\n> not q quote\n not a quote\n > not a quote"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            LeafNode("h6", "Heading"),
            ParentNode("pre", [LeafNode("code", "code block")]),
            ParentNode("blockquote", [LeafNode("p", "quote\n"), LeafNode("p", "quote")]),
            ParentNode("ul", [LeafNode("li", " unordered list"), LeafNode("li", " unorderedlist")]),
            ParentNode("ol", [LeafNode("li", " ordered list"), LeafNode("li", " ordered list"), LeafNode("li", " ordered list")]),
            LeafNode("p", "########## normal paragraph"),
            LeafNode("p", "> not q quote\n not a quote\n > not a quote")
        ])
        self.assertEqual(expected, result)



if __name__ == "__main__":
    unittest.main()