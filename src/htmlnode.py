class HTMLNode:
    def __init__(self, tag:str | None = None, value: str | None = None, children:list["HTMLNode"] | None = None, props: dict[str,str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        pass
    
    def to_html(self):
        raise NotImplementedError("child class will implement")
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ''
        
        s = ''
        for k,v in self.props.items():
            s += f' {k}=\"{v}\"'
        return s
    
    def __repr__(self):
        output = ''
        if self.tag is not None:
            output += f'tag: {self.tag}\n'
        else:
            output += f'tag: \n'
        if self.value is not None:
            output += f'value: {self.value}\n'
        else:
            output += f'value: \n'
        if self.children is not None:
            output += f'children: {self.children}\n'
        else:
            output += f'children: \n'
        if self.props is not None:
            output += f'props: {self.props}\n'
        else:
            output += f'props: \n'
        return output

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value:str, props:dict[str,str] | None = None):
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        raw = self.value
        if self.tag is not None:
            tagged = f'<{self.tag}{self.props_to_html()}>{raw}</{self.tag}>'
            return tagged
        return raw
    
    def __repr__(self):
        output = ''
        if self.tag is not None:
            output += f'tag: {self.tag}\n'
        else:
            output += f'tag: \n'
        if self.value is not None:
            output += f'value: {self.value}\n'
        else:
            output += f'value: \n'
        if self.props is not None:
            output += f'props: {self.props}\n'
        else:
            output += f'props: \n'
        return output

class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:str, props:dict[str,str] = None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self):
        if self.tag is None or len(self.tag) == 0:
            raise ValueError("Empty Tag Not allowed")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent Node must have at least one child")
        
        html =f'<{self.tag}{self.props_to_html()}>'
        for c in self.children:
            html+=c.to_html()
        html+=f'</{self.tag}>'
        return html