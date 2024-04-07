import re

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(list(map(lambda kv: f"{kv[0]}=\"{kv[1]}\"", self.props.items())))
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, value: object) -> bool:
        return self.tag == value.tag and self.value == value.value and self.children == value.children and self.props == value.props
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("A value must be provided to use this method.")
        if not self.tag:
            return self.value
    
        return f"<{self.tag}" + f"{"" if not self.props else super().props_to_html()}>" + f"{self.value}" + f"</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=[], props=None) -> None:
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag or len(self.tag) == 0:
            raise ValueError("You must provide a tag for this method.")
        if len(self.children) == 0:
            raise ValueError("You must provide children.")

        return f"<{self.tag}{self.props_to_html()}>" + "".join(list(map(lambda child: child.to_html(), self.children))) + f"</{self.tag}>"

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
    

def markdown_to_blocks(markdown):
    components = markdown.split('\n\n')
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
    elif block.startswith("```") and block.endswith("```"):
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
    return LeafNode(f"h{h_num}", re.split(r"^#{1,6} ", block)[1])

def code_block_to_htmlnode(block):
    return ParentNode("pre", [LeafNode("code", block.strip('`'))])

def quote_block_to_htmlnode(block):
    leafs = []
    lines = block.split('>')
    for line in lines:
        if line == "":
            continue
        leafs.append(LeafNode("p", line))
    return ParentNode("blockquote", leafs)

def unordered_list_block_to_htmlnode(block):
    leafs = []
    lines = block.split('\n')
    for line in lines:
        leafs.append(LeafNode("li", line[1:].strip("\n")))
    return ParentNode("ul", leafs)

def ordered_list_block_to_htmlnode(block):
    leafs = []
    lines = block.split('\n')
    for line in lines:
        leafs.append(LeafNode("li", line[2:].strip("\n")))
    return ParentNode("ol", leafs)

def paragraph_block_to_htmlnode(block):
    return LeafNode("p", block)

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