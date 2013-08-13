import urllib2, re
from xml.etree.ElementTree import ElementTree
from xml.dom.minidom import parseString

import sys

class ArxivRetriever():
    """
    accept an arxiv_id
    request info via arxiv api
    put them into a dict
    """

    def __init__(self):
        self.arxiv_id = None

    def arxiv_id_cleaner(self, arxiv_id):
        self.pattern = 'arXiv:\d{4}\.\d{4}(v\d{1})?|arXiv:[a-zA-Z]+\-[a-zA-Z]+/\d{7}(v\d{1})?'
        self.arxiv_id = re.search(self.pattern, arxiv_id).group().split(':')[1]
        return self.arxiv_id

    # input:
    #     arxiv_id: e.g.'arXiv:hep-th/0612073v2'
    # output:
    #     the xml responsed by the arXiv api
    def arxiv_query(self):
        if self.arxiv_id:
            print 'querying', self.arxiv_id, 'via arXiv api'
            query_header = 'http://export.arxiv.org/api/query?id_list='
            query_url = ''.join([query_header, self.arxiv_id])
            xml_data = urllib2.urlopen(query_url).read()
            return xml_data
        else:
            print  'no arxiv_id passed'
            return


    # from docs.python.org
    # this snippet returns the text of the tag 'nodelist'

    def getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    # parse the xml returned by the arXive api
    # input:
    #     xml_content:the xml returned
    #     arxiv_idenfitier: e.g.'arXiv:hep-th/0612073v2'
    # output:
    #     entry_content:a dict containing meta-info
    def xml_parser(self, xml_content):
        print 'creating entries for', self.arxiv_id
        self.xml_dom = parseString(xml_content)
        #unicode
        #parse the xml by tags for meta-info
        self.title = self.getText(self.xml_dom.getElementsByTagName('title')[1].childNodes)
        self.summary = self.getText(self.xml_dom.getElementsByTagName('summary')[0].childNodes)
        self.author_nodes = self.xml_dom.getElementsByTagName('name')
        self.author_list = [self.getText(self.author.childNodes) for self.author in self.author_nodes]
        self.category = self.xml_dom.getElementsByTagName('arxiv:primary_category')[0].attributes['term'].value
        #return the dict containing meta-info in unicode
        self.entry_content = dict(title=self.title, 
        	summary=self.summary, 
        	author=self.author_list, 
        	category=self.category, 
        	identifier=self.arxiv_id)
        #TODO:link-href pdf-link-href
        return self.entry_content

    def fetch(self, arxiv_id):
    	self.arxiv_id = self.arxiv_id_cleaner(arxiv_id)
        self.xml_content = self.arxiv_query()
        self.entry_content = self.xml_parser(self.xml_content)
        return self.entry_content

if __name__ == "__main__":
	path = sys.argv[1]
	print path
	res = ArxivRetriever().fetch(path)
	print res
