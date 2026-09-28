from enum import Enum
from htmlnode import LeafNode
from raw_helpers import extract_markdown_images, extract_markdown_links
import re
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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    def split_node_images(node:TextNode)->list[TextNode]:
        imgs = extract_markdown_images(node.text)
        imlinks = [f"![{alt}]({url})" for alt, url in imgs]
        inds = [ match.start() for match in re.finditer(r"\!\[.*?\]\(.*?\)",node.text)]
        sti = 0
        nodes = []
        for i,ind in enumerate(inds):
            if sti < ind:
                s = node.text[sti:ind]
                nodes.append(TextNode(s,TextType.TEXT))
            ln = len(imlinks[i])
            sti = ind + ln
            nodes.append(TextNode(imgs[i][0],TextType.IMAGE,imgs[i][1]))
        if sti < len(node.text):
            s = node.text[sti:len(node.text)]
            nodes.append(TextNode(s,TextType.TEXT))
        return nodes
    for ond in old_nodes:
        if ond.text_type != TextType.TEXT:
            new_nodes.append(ond)
            continue
        new_nodes.extend(split_node_images(ond))
    return new_nodes
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    def split_node_links(node:TextNode)->list[TextNode]:
        anchors = extract_markdown_links(node.text)
        alinks = [f"[{alt}]({url})" for alt, url in anchors]
        inds = [ match.start() for match in re.finditer(r"\[.*?\]\(.*?\)",node.text)]
        sti = 0
        nodes = []
        for i,ind in enumerate(inds):
            if sti < ind:
                s = node.text[sti:ind]
                nodes.append(TextNode(s,TextType.TEXT))
            ln = len(alinks[i])
            sti = ind + ln
            nodes.append(TextNode(anchors[i][0],TextType.LINK,anchors[i][1]))
        if sti < len(node.text):
            s = node.text[sti:len(node.text)]
            nodes.append(TextNode(s,TextType.TEXT))
        return nodes
    for ond in old_nodes:
        if ond.text_type != TextType.TEXT:
            new_nodes.append(ond)
            continue
        new_nodes.extend(split_node_links(ond))
    return new_nodes

def text_to_textnodes(text:str)->list[TextNode]:
    nd = TextNode(text,TextType.TEXT)
    delims = [('**',TextType.BOLD),('_',TextType.ITALIC),('`',TextType.CODE)]
    nodes = [nd]
    for delim,type in delims:
        nodes = split_nodes_delimiter(nodes,delim,type)
        # print(nodes)
    nodes = split_nodes_image(nodes)
    # print(nodes)
    nodes = split_nodes_link(nodes)
    # print(nodes)
    return nodes