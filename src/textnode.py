from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def __eq__(self, value: object) -> bool:
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url

def text_node_to_html_node(text_node):
    type = text_node.text_type

    if type == text_type_text:
        return LeafNode(None, text_node.text)
    elif type == text_type_bold:
        return LeafNode("b", text_node.text)
    elif type == text_type_italic:
        return LeafNode("i", text_node.text)
    elif type == text_type_code:
        return LeafNode("code", text_node.text)
    elif type == text_type_link:
        return LeafNode("a", text_node.text)
    elif type == text_type_image:
        return LeafNode("b", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception(f"Could not find text type {type}")