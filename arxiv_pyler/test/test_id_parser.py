import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from lib import arxiv_id_parser
import unittest

FILE_SOURCE_PDF = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testpdf\\1305.5767.pdf'))
FILE_NAME_PDF = '1305.5767.pdf'

FILE_SOURCE_TXT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testpdf\\a.txt'))
FILE_NAME_TXT = 'a.txt'

class TestIDParser(unittest.TestCase):

    def test_id_parser(self):

        self.identifier = arxiv_id_parser.arxiv_id_parser(FILE_SOURCE_PDF, FILE_NAME_PDF)
        self.assertEqual(self.identifier, u'1305.5767v1')

        self.identifier = arxiv_id_parser.arxiv_id_parser(FILE_SOURCE_TXT, FILE_NAME_TXT)
        self.assertRaises(Exception('NonArxivPdf'), self.identifier)

if __name__ == '__main__':
    unittest.main()