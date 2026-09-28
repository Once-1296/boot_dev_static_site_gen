from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes
from htmlnode import HTMLNode,ParentNode, LeafNode
class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"

def markdown_to_blocks(markdown:str)->list[str]:
    blocks = markdown.split('\n\n')
    # print(blocks)
    blocks = [block for block in blocks if len(block)>0]
    # print(blocks)
    blocks = ['\n'.join([line.strip() for line in block.split('\n') if len(line.strip())>0]) for block in blocks]
    # print(blocks)
    blocks = [block for block in blocks if len(block)>0]
    return blocks

def matchHeading(block:str)->bool:
    if '\n' in block:
        return False
    i = 0
    while i < len(block):
        if block[i] != '#':
            break
        i += 1
    if i == len(block):
        return False
    return i > 0 and i <= 6 and block[i] == ' '
    
def matchCode(block:str):
    if len(block) < 7:
        return False
    return block[:4]=='```\n' and block[-3:] == '```'

def matchQuote(block:str):
    lines = block.split('\n')
    return all([len(line) > 0 and line[0]=='>' for line in lines])

def matchUOList(block:str):
    lines = block.split('\n')
    fg = all([len(line)>2 for line in lines])
    if not fg:
        return False
    return all([line[:2]=='- ' for line in lines])

def matchOList(block:str):
    def matchLine(line:str, num:int):
        start = str(num)+'. '
        return line.startswith(start)
    return all([matchLine(line,i+1) for i, line in enumerate(block.split('\n'))])

def block_to_blocktype(block:str)->BlockType:
    if matchHeading(block):
        return BlockType.HEADING
    elif matchCode(block):
        return BlockType.CODE
    elif matchQuote(block):
        return BlockType.QUOTE
    elif matchUOList(block):
        return BlockType.UNORDERED_LIST
    elif matchOList(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def processCodeBlock(block:str)->HTMLNode:
    code = block[4:-3]
    codeNode = TextNode(code, TextType.CODE)
    htmlNode = text_node_to_html_node(codeNode)
    parent = ParentNode("pre",[htmlNode])
    return parent

def processHeadingBlock(block:str)->HTMLNode:
    i = 0
    while block[i] == '#':
        i += 1
    cnt = i
    heading = block[i+1:]
    textnodes = text_to_textnodes(heading)
    htmlnodes = [text_node_to_html_node(text_node) for text_node in textnodes]
    return ParentNode(f"h{cnt}",htmlnodes)

def processParagraphBlock(block:str)->HTMLNode:
    para = block.replace('\n',' ')
    textnodes = text_to_textnodes(para)
    htmlnodes = [text_node_to_html_node(text_node) for text_node in textnodes]
    return ParentNode("p",htmlnodes)

def processQuoteBlock(block: str) -> HTMLNode:
    lines = block.split('\n')
    stripped = []
    for line in lines:
        stripped.append(line.lstrip('>').strip())
    text = ' '.join(stripped)
    textnodes = text_to_textnodes(text)
    htmlnodes = [text_node_to_html_node(tn) for tn in textnodes]
    return ParentNode("blockquote", htmlnodes)

def processUOListBlock(block:str)->HTMLNode:
    lines = block.split('\n')
    children=[]
    for line in lines:
        text = line[2:]
        textnodes = text_to_textnodes(text)
        htmlnodes = [text_node_to_html_node(text_node) for text_node in textnodes]
        children.append(ParentNode("li",htmlnodes))
    return ParentNode("ul",children)

def processOListBlock(block:str)->HTMLNode:
    lines = block.split('\n')
    children=[]
    for i,line in enumerate(lines):
        num = str(i+1)
        text = line[len(num) + 2:]
        textnodes = text_to_textnodes(text)
        htmlnodes = [text_node_to_html_node(text_node) for text_node in textnodes]
        children.append(ParentNode("li",htmlnodes))
    return ParentNode("ol",children)

def markdown_to_html_node(markdown:str)->HTMLNode:
    blocks = markdown_to_blocks(markdown=markdown)
    # for block in blocks:
    #     print(repr(block), block_to_blocktype(block))
    def block_to_html_node(block:str):
        btype = block_to_blocktype(block)
        if btype == BlockType.CODE:
            return processCodeBlock(block)
        elif btype == BlockType.HEADING:
            return processHeadingBlock(block)
        elif btype == BlockType.PARAGRAPH:
            return processParagraphBlock(block)
        elif btype == BlockType.QUOTE:
            return processQuoteBlock(block)
        elif btype == BlockType.UNORDERED_LIST:
            return processUOListBlock(block)
        elif btype == BlockType.ORDERED_LIST:
            return processOListBlock(block)
        else:
            raise ValueError("Unknown block type")
    children = [ block_to_html_node(block) for block in blocks]
    return ParentNode("div",children)
        