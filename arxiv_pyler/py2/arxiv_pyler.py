import os, re
import urllib2
from xml.etree.ElementTree import ElementTree
from xml.dom.minidom import parseString
from PyPDF2 import PdfFileReader

#sys.argv[0] = the path with arxiv pdf

#sys.argv[0]

def arxiv_pyler(path):
    COUNTER = 0
    if path==None:
        pass
    entry_list=[]
    print path
    for root, dirs, files in os.walk(path):
        #if root != path:
        #try:
        for pdf in files:
            if re.search('.pdf$', pdf):
                
                source = os.path.join(root, pdf)
                identifier = arxiv_id_parser(source, pdf)
                xml_content = arxiv_query(identifier)
                entry_content = xml_parser(xml_content, identifier)
                entry_list.append(entry_content)
                entry_list[COUNTER].update({'file_source':source})
                #shutil.move(source, pdf_dir)
                COUNTER += 1
        #except:
            #continue
    html_generator(entry_list)
    print 'complete'
    return entry_list

def arxiv_id_parser(file_source, file_name):
    print 'get identifier of ', file_name
    #the encode of root
    pdf = PdfFileReader(open(file_source, "rb"))
    
    raw_content = pdf.getPage(0).extractText()
    content = " ".join(raw_content.replace(u"\xa0", " ").strip().split())
    pattern = 'arXiv:\d{4}\.\d{4}(v\d{1})?|arXiv:[a-zA-Z]+\-[a-zA-Z]+/\d{7}(v\d{1})?'
    identifier = re.search(pattern, content).group().split(':')[1]
    #identifier looks like hep-th/0612073v2 (unicode)
    return identifier

def arxiv_query(arxiv_identifier):
    print 'querying', arxiv_identifier, 'via arXiv api'
    query_header = u'http://export.arxiv.org/api/query?id_list='
    query_url = ''.join([query_header, arxiv_identifier])
    html_data = urllib2.urlopen(query_url).read()
    return html_data

#from docs.python.org
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def xml_parser(xml_content, arxiv_identifier):
    print 'creating entries for ', arxiv_identifier
    xml_dom = parseString(xml_content)
    #unicode
    title = getText(xml_dom.getElementsByTagName('title')[1].childNodes)
    summary = getText(xml_dom.getElementsByTagName('summary')[0].childNodes)
    author_nodes = xml_dom.getElementsByTagName('name')
    author_list = [getText(author.childNodes) for author in author_nodes]
    category = xml_dom.getElementsByTagName('arxiv:primary_category')[0].attributes['term'].value
    entry = dict(title=title, summary=summary, author=author_list, category=category, identifier=arxiv_identifier)
    #TODO:link-href pdf-link-href
    return entry

HTML_HEAD = u'''
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">
        <title>arXiv files</title>
        <!-- Bootstrap -->
        <link media="screen" rel="stylesheet" href="components/bootstrap/css/bootstrap.min.css">
      </head>

      <body>
      <div class="container">
        <legend><h2>arXiv files</h2></legend>
        <div class="row">
        <div class="span9">
        <div class="row-fluid">
    '''

HTML_TAIL = u'''
        </div><!--RowFluidThumbnail-->
        </div>
        </div>
        </div><!--Container-->
        <script type="text/javascript" src="components/jquery-1.9.1.js"></script>
        <script type="text/javascript" src="components/bootstrap/js/bootstrap.min.js"></script>
      </body>
     </html>
     '''

def html_generator(entry_list):
    print 'generating html'
    f = open('output.html', 'w')
    f.write(HTML_HEAD)
    for entry in entry_list:
        a = '''<div class="thumbnail"><div class="caption">'''
        b = '''<p>'''
        c = '''</p>'''
        d = '''</div></div><!--Thumbnail--><br><!--divider-->'''
        
        # ENTRY['AUTHOR'] IS A LIST
        s=[a,
           '''<p><a href=\'''',entry['file_source'],'''\'>''',
           entry['title'],'''</a></p>''',
           b,entry['identifier'],c,
           b,', '.join(entry['author']),c,
           b,entry['summary'],c,
           d]
        string = ''.join(s)
        f.write(string)
    f.write(HTML_TAIL)
    f.close()




if __name__ == '__main__':
    PATH = os.path.dirname(__file__)
    print PATH
    arxiv_pyler(PATH)