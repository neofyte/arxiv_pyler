import os, re, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from lib.arxiv_id_parser import arxiv_id_parser
from lib.arxiv_query import arxiv_query
from lib.arxiv_response_parser import xml_parser
from lib.html_generator import html_generator

#sys.argv[0] = the path with arxiv pdf

def arxiv_pyler(path):
    if os.path.exists(path):
        COUNTER = 0
        if path==None:
            pass
        entry_list=[]
        print path
        for root, dirs, files in os.walk(path):
            for pdf in files:
                if re.search('.pdf$', pdf):
                    try:
                        source = os.path.join(root, pdf)
                        identifier = arxiv_id_parser(source, pdf)
                        xml_content = arxiv_query(identifier)
                        entry_content = xml_parser(xml_content, identifier)
                        entry_list.append(entry_content)
                        entry_list[COUNTER].update({'file_source':source})
                        #shutil.move(source, pdf_dir)
                        COUNTER += 1
                    except Exception as inst:
    					for error in inst.args:
                        	print error
                else:
                    continue
        html_generator(entry_list)
        print 'complete'
        return entry_list
    else:
        print 'path does not exits.'

if __name__ == '__main__':
    path = sys.argv[1]
    print path
    arxiv_pyler(path)