


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError
    

    def props_to_html(self):
        if self.props == None:
            return ""
        html_attributes = []
        for key,value in self.props.items():
            html_attributes.append(f' {key}="{value}"')
        return "".join(html_attributes)
    

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    