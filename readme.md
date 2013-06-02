This repo gives a simple wrapper around PyPdf2, which aims to help those blind-hoarding-arxiv-paper guys. arxiv_pyler.py searches the pdf under the directory given by the user, and output the meta data about the papers in an html file. The html file uses bootstrap so as to look much better than the raw html. 
arxiv_pyler_gui.py is the gui version of the script. It does basically the same thing and is written in PySide.
Both scripts are written in Python2.7

how to run it:
run following command in termianal/command line: python arxiv_pyler.py

dependencies:
to run the script, one needs to install, besides Python2.7, PyPdf2.
to make the script work, one has to connect to network.