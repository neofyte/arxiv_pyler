import re
from PyPDF2 import PdfFileReader

#input:
#    file_source:file path
#    file_name:file name
#output:
#    the identifier of the pdf
#
#if a non-arXiv-pdf file is input
#it will raise a 'NonArxivPdf' error
def arxiv_id_parser(file_source, file_name):
    if re.search('.pdf$', file_name):
        print 'getting identifier of', file_name
        try:
        	pdf = PdfFileReader(open(file_source, "rb"))
        except:
        	raise Exception('OpenError')
        #read the first page of the pdf
        #since all the meta-info is on the first page
        raw_content = pdf.getPage(0).extractText()

        content = " ".join(raw_content.replace(u"\xa0", " ").strip().split())
        #two patterns used before and after 2004 respectively
        #    1:(before 2004) 'arXiv:hep-th/0612073v2'
        #    2:(after 2004) 'arXiv:1305.5767'
        pattern = 'arXiv:\d{4}\.\d{4}(v\d{1})?|arXiv:[a-zA-Z]+\-[a-zA-Z]+/\d{7}(v\d{1})?'
        identifier = re.search(pattern, content).group().split(':')[1]
        #identifier looks like 'hep-th/0612073v2' (unicode)
        if identifier:
        	return identifier
        else:
        	print 'no identifier returned'
        	raise Exception('NonArxivPdf')
    else:
    	print 'ignoring', file_name, 'since it is not a pdf'