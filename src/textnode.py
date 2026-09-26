from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
    TEXT="plain"
    BOLD="bold"
    ITALIC="italic"
    CODE="code"
    LINK="link"
    IMAGE="image"

class TextNode:
    def __init__(self, text:str, text_type:TextType, url:str | None = None):
        self.text, self.text_type, self.url = text, text_type, url
    def __eq__(self, other:"TextNode"):
        return self.text == other.text and self. text_type == other.text_type and ((self.url is None) == (other.url is None)) and (self.url == other.url)  
    
    def __repr__(self):
        url = self.url if self.url is not None else ''
        return f"TextNode({self.text}, {self.text_type.value}, {url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text is None or len(text_node.text) == 0:
        raise ValueError("No content in tag")
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag='b', value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag='i', value=text_node.text)
    elif text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None,value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None or len(text_node.url) == 0:
            raise ValueError("Anchor tag has no link")
        return LeafNode(tag='a', value=text_node.text, props={"href":text_node.url})
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag='code', value=text_node.text)
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None or len(text_node.url) == 0:
            raise ValueError("Image tag has no link")
        return LeafNode(tag='img', value='',props={"src":text_node.url, "alt":text_node.text})
    raise ValueError("Invalid Text Type")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    def convert(old_node:TextNode, delim:str, text_type:TextType)->list[TextNode]:
        if old_node.text_type != TextType.TEXT:
            return [old_node]
        parts = old_node.text.split(delim)
        if len(parts) % 2 == 0:
            raise ValueError(f"non terminated {delim} or empty list")
        nodes =[]
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_node = TextNode(part, old_node.text_type, old_node.url)
                nodes.append(new_node)
            else:
                new_node = TextNode(part, text_type)
                nodes.append(new_node)
        return nodes
    new_nodes = []
    for old_node in old_nodes:
        new_nodes.extend(convert(old_node,delimiter,text_type))
    return new_nodes