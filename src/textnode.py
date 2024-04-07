from htmlnode import LeafNode
from htmlnode import ParentNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

bold_delimiter = "**"
italic_delimiter = "*"
code_delimiter = "`"

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
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif type == text_type_image:
        return LeafNode("img", " ", {"src": text_node.url, "alt": text_node.text})
    raise Exception(f"Could not find text type {type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if not node.text_type == text_type_text:
            new_nodes.append(node)
            continue
        if not node.text.count(delimiter) % 2 == 0 and not (node.text.startswith(delimiter) and node.text.endswith(delimiter)):
            print(node)
            raise Exception("The delimiter must be closed.")

        components = node.text.split(delimiter)
        for idx, component in enumerate(components):
            if idx % 2 == 0:
                new_nodes.append(TextNode(component, text_type_text))
            else:
                new_nodes.append(TextNode(component, text_type))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    def getNodeList(node):
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            node = [node] if not (node.text == "" or node.text == "\n") else []
            return node

        components = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
        before, after = components[0], components[1]

        nodes = []
        nodes.extend(getNodeList(TextNode(before, text_type_text)))
        nodes.append(TextNode(images[0][0], text_type_image, images[0][1]))
        nodes.extend(getNodeList(TextNode(after, text_type_text)))
            
        return nodes
    
    for node in old_nodes:
        new_nodes.extend(getNodeList(node))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    def getNodeList(node):
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            node = [node] if not (node.text == "" or node.text == "\n") else []
            return node

        components = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
        before, after = components[0], components[1]

        nodes = []
        nodes.extend(getNodeList(TextNode(before, text_type_text)))
        nodes.append(TextNode(links[0][0], text_type_link, links[0][1]))
        nodes.extend(getNodeList(TextNode(after, text_type_text)))
            
        return nodes
    
    for node in old_nodes:
        new_nodes.extend(getNodeList(node))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]

    nodes = split_nodes_delimiter(nodes, bold_delimiter, text_type_bold)
    nodes = split_nodes_delimiter(nodes, italic_delimiter, text_type_italic)
    nodes = split_nodes_delimiter(nodes, code_delimiter, text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    components = []
    code_components = markdown.split("```")

    for idx, component in enumerate(code_components):
        if idx % 2 == 1: # in a code block
            components.append("```" + component + "```")
        else:
            components.extend(component.split("\n\n"))
    # components = markdown.split("\n\n")
    components = list(filter(lambda item: not len(item) == 0, map(lambda component: component.strip('\n '), components)))
    return components

def block_to_block_type(block):
    def isOrderedList(block):
        lines = block.split("\n")
        for idx, line in enumerate(lines):
            if not line.startswith(f"{idx + 1}."):
                return False
        return True

    if re.split(r"^#{1,6} ", block)[0] == "":
        return block_type_heading
    elif block.startswith("`") and block.endswith("`"):
        return block_type_code
    elif len(list(filter(lambda line: not line.startswith(">"), block.split("\n")))) == 0:
        return block_type_quote
    elif len(list(filter(lambda line: not (line.startswith("*") or line.startswith("-")), block.split("\n")))) == 0:
        return block_type_unordered_list
    elif isOrderedList(block):
        return block_type_ordered_list

    return block_type_paragraph

def heading_block_to_htmlnode(block):
    components = block.split()
    h_num = len(components[0])

    parents = []
    lines = re.split(r"^#{1,6} ", block)
    for line in list(filter(lambda line: not len(line) == 0, lines)):
        parents.append(ParentNode("p", list(map(lambda node: text_node_to_html_node(node), text_to_textnodes(line)))))
    return ParentNode(f"h{h_num}", parents)

def code_block_to_htmlnode(block):
    return ParentNode("pre", [LeafNode("code", block.strip('`'))])

def quote_block_to_htmlnode(block):
    parents = []
    lines = re.split(r">", block)
    for line in list(filter(lambda line: not len(line) == 0, lines)):
        parents.append(ParentNode("p", list(map(lambda node: text_node_to_html_node(node), text_to_textnodes(line)))))
    return ParentNode("blockquote", parents)

def unordered_list_block_to_htmlnode(block):
    parents = []
    lines = re.split(r"\* |\-", block)
    for line in list(filter(lambda line: not len(line) == 0, lines)):
        parents.append(ParentNode("li", list(map(lambda node: text_node_to_html_node(node), text_to_textnodes(line)))))
    return ParentNode("ul", parents)

def ordered_list_block_to_htmlnode(block):
    parents = []
    lines = re.split(r"\d.", block)
    for line in list(filter(lambda line: not len(line) == 0, lines)):
        parents.append(ParentNode("li", list(map(lambda node: text_node_to_html_node(node), text_to_textnodes(line)))))
    return ParentNode("ol", parents)

def paragraph_block_to_htmlnode(block):
    nodes = text_to_textnodes(block)

    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))

    return ParentNode("p", children)

def markdown_to_html_node(markdown):
    def getHTMLNode(block):
        type = block_to_block_type(block)
        if type == block_type_heading:
            return heading_block_to_htmlnode(block)
        elif type == block_type_code:
            return code_block_to_htmlnode(block)
        elif type == block_type_quote:
            return quote_block_to_htmlnode(block)
        elif type == block_type_unordered_list:
            return unordered_list_block_to_htmlnode(block)
        elif type == block_type_ordered_list:
            return ordered_list_block_to_htmlnode(block)
        return paragraph_block_to_htmlnode(block)
    
    return ParentNode("div", list(map(getHTMLNode, markdown_to_blocks(markdown))))