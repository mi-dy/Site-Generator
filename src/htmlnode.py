class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f'tag = "{self.tag}"\nvalue = "{self.value}"\nchildren = "{self.children}"\nprops = "{self.props}"'

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        if self.props == {}:
            return ""
        
        result = ""
        for key, value in self.props.items():
            result = result + f' {key}="{value}"'
        
        return result

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f'tag = "{self.tag}"\nvalue =  "{self.value}"\nprops = "{self.props}"'

    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    
    def to_html(self):
        if self.tag == None:
            raise ValueError('"tag" missing')
        if self.children == ValueError():
            raise ValueError('children values missing')
        children_html = ""
        for child in self.children:
            children_html = children_html + child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
