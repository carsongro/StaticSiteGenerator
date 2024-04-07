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

        return f"<{self.tag}" + f"{None if not self.props else super().props_to_html()}>" + f"{self.value}" + f"</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=[], props=None) -> None:
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag or len(self.tag) == 0:
            raise ValueError("You must provide a tag for this method.")
        if len(self.children) == 0:
            raise ValueError("You must provide children.")
        
        return f"<{self.tag}{self.props_to_html()}>" + "".join(list(map(lambda child: child.to_html(), self.children))) + f"</{self.tag}>"