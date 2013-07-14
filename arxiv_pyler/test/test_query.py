import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from lib import arxiv_query, arxiv_response_parser
import unittest

IDENTIFIER = u'hep-th/0612073v2'


class TestIDParser(unittest.TestCase):

    def test_query(self):

        self.xml = arxiv_query.arxiv_query(IDENTIFIER)
        self.entry = arxiv_response_parser.xml_parser(self.xml, IDENTIFIER)
        self.assertEqual(self.entry['title'], 
        	'Gauge Theory, Ramification, And The Geometric Langlands Program'
        )

if __name__ == '__main__':
    unittest.main()