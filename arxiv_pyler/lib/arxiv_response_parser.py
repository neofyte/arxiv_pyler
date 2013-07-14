import urllib2
from xml.etree.ElementTree import ElementTree
from xml.dom.minidom import parseString

#from docs.python.org
#this snippet returns the text of the tag 'nodelist'
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

#parse the xml returned by the arXive api
#input:
#    xml_content:the xml returned
#    arxiv_idenfitier: e.g.'arXiv:hep-th/0612073v2'
#output:
#    entry_content:a dict containing meta-info
def xml_parser(xml_content, arxiv_identifier):
    print 'creating entries for', arxiv_identifier
    xml_dom = parseString(xml_content)
    #unicode
    #parse the xml by tags for meta-info
    title = getText(xml_dom.getElementsByTagName('title')[1].childNodes)
    summary = getText(xml_dom.getElementsByTagName('summary')[0].childNodes)
    author_nodes = xml_dom.getElementsByTagName('name')
    author_list = [getText(author.childNodes) for author in author_nodes]
    category = xml_dom.getElementsByTagName('arxiv:primary_category')[0].attributes['term'].value
    #return the dict containing meta-info in unicode
    entry_content = dict(title=title, summary=summary, author=author_list, category=category, identifier=arxiv_identifier)
    #TODO:link-href pdf-link-href
    return entry_content