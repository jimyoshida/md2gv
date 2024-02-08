#!/usr/bin/env python
import sys
import markdown_it
from xml.dom import minidom
from pydot import Node, Edge, Dot

# Global variables
Graph = Dot(graph_type='digraph', rankdir="LR")
Num = 1

def encode_to_xml_string(input_string):
    doc = minidom.Document()
    text_node = doc.createTextNode(input_string)
    encoded_string = text_node.toxml()
    return encoded_string

# Make the XML string for DOM
def convert_markdown_to_xml(markdown_text):
    md = markdown_it.MarkdownIt()
    tokens = md.parse(markdown_text)
    xml = ""
    lv = 0
    
    for token in tokens:
        if token.type == 'heading_open':
            while (int)(token.tag[1]) <= lv:
                lv -= 1
                xml += "</node>"
            xml += "<node>"
        elif token.type == 'heading_close':
            lv += 1
        elif token.type == 'list_item_open':
            xml += "<node>"
        elif token.type == 'list_item_close':
            xml += "</node>"
        elif token.type == 'inline':
            xml += encode_to_xml_string(token.content)
    
    while lv > 0:
        lv -= 1
        xml += "</node>"

    return xml

# Process an XML element for DOT
def process_node(n_parent, e_this):
    global Num

    # create the DOT node from the XML text node
    for e_child in e_this.childNodes:
        if e_child.nodeType == e_child.TEXT_NODE:
            n_this = Node(f"n-{Num}", label=e_child.data)
            Graph.add_node(n_this)
            if n_parent is not None:
                e_new = Edge(n_parent, n_this)
                Graph.add_edge(e_new)
            Num += 1
            break

    # process the nested element nodes
    for e_child in e_this.childNodes:
        if e_child.nodeType == e_child.ELEMENT_NODE:
            process_node(n_this, e_child)

# Start
filename = "../self-taught-devops/ch1/README.md" # for default debug
if len(sys.argv) > 1:
    filename = sys.argv[1]

with open(filename, 'r', encoding='utf8') as f:
    markdown_text = f.read()

xml_string = convert_markdown_to_xml(markdown_text)
dom = minidom.parseString(xml_string)
process_node(None, dom.documentElement)

dot_string = Graph.to_string()
print(dot_string)
