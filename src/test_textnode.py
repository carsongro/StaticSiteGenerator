import unittest

from textnode import *
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        
        self.assertEqual(new_nodes, result)
    
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = extract_markdown_images(text)
        self.assertEqual([("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")], result)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = extract_markdown_links(text)
        self.assertEqual([("link", "https://www.example.com"), ("another", "https://www.example.com/another")], result)
    
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ]

        self.assertEqual(expected, new_nodes)
    
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode(
                "another", text_type_link, "https://www.example.com/another"
            ),
        ]
        self.assertEqual(expected, new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(expected, result)
    
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
        expected = HTMLNode("h6", None, [HTMLNode("p", None, [HTMLNode(None, "Heading", None, None)], None)], None) 
        self.assertEqual(expected, result)

    def test_code_block_to_htmlnode(self):
        block = "```code block```"
        result = code_block_to_htmlnode(block)
        expected = ParentNode("pre", [LeafNode("code", "code block")])
        self.assertEqual(result, expected)

    def test_quote_block_to_htmlnode(self):
        block = ">quote\n>quote"
        result = quote_block_to_htmlnode(block)
        expected = HTMLNode("blockquote", None, [HTMLNode("p", None, [HTMLNode(None, "quote\n", None, None)], None), HTMLNode("p", None, [HTMLNode(None, "quote", None, None)], None)], None)
        self.assertEqual(expected, result)

    def test_unordered_list_block_to_htmlnode(self):
        block = "* unordered list\n- unorderedlist"
        result = unordered_list_block_to_htmlnode(block)
        expected = HTMLNode("ul", None, [HTMLNode("li", None, [HTMLNode(None, "unordered list\n", None, None)], None), HTMLNode("li", None, [HTMLNode(None, " unorderedlist", None, None)], None)], None)
        self.assertEqual(expected, result)

    def test_ordered_list_block_to_htmlnode(self):
        block = "1. ordered list\n2. ordered list\n3. ordered list"
        result = ordered_list_block_to_htmlnode(block)
        expected = HTMLNode("ol", None, [HTMLNode("li", None, [HTMLNode(None, " ordered list\n", None, None)], None), HTMLNode("li", None, [HTMLNode(None, " ordered list\n", None, None)], None), HTMLNode("li", None, [HTMLNode(None, " ordered list", None, None)], None)], None)
        self.assertEqual(expected, result)

    def test_paragraph_block_to_htmlnode(self):
        block = "########## normal paragraph"
        result = paragraph_block_to_htmlnode(block)
        expected = HTMLNode("p", None, [HTMLNode(None, "########## normal paragraph", None, None)], None)
        self.assertEqual(expected, result)
    
    def test_markdown_to_html_node(self):
        markdown = "###### Heading\n\n```code block```\n\n>quote\n>quote\n\n* unordered list\n- unorderedlist\n\n1. ordered list\n2. ordered list\n3. ordered list\n\n########## normal paragraph\n\n> not q quote\n not a quote\n > not a quote"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
                HTMLNode("h6", None, [HTMLNode("p", None, [HTMLNode(None, "Heading", None, None)], None)], None),
                ParentNode("pre", [LeafNode("code", "code block")]),
                HTMLNode("blockquote", None, [HTMLNode("p", None, [HTMLNode(None, "quote\n", None, None)], None), HTMLNode("p", None, [HTMLNode(None, "quote", None, None)], None)], None),
                HTMLNode("ul", None, [HTMLNode("li", None, [HTMLNode(None, "unordered list\n", None, None)], None), HTMLNode("li", None, [HTMLNode(None, " unorderedlist", None, None)], None)], None),
                HTMLNode("ol", None, [HTMLNode("li", None, [HTMLNode(None, " ordered list\n", None, None)], None), HTMLNode("li", None, [HTMLNode(None, " ordered list\n", None, None)], None), HTMLNode("li", None, [HTMLNode(None, " ordered list", None, None)], None)], None),
                HTMLNode("p", None, [HTMLNode(None, "########## normal paragraph", None, None)], None),
                HTMLNode("p", None, [HTMLNode(None, "> not q quote\n not a quote\n > not a quote", None, None)], None)
            ]
        )
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()