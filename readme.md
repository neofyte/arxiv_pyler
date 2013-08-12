Introduction
============

arXiv-pyler, collects information of  arXiv:Pdf's on the path given by the user, generates a html and pile the pdfs.

This repo still needs further furnishments.

scripts under py2 work normally while others need further check. I will port it to py3 asap and make it work as smoothly as possible.

Situation
==========

When a user has lots of pdf downloaded from [arXiv.org](arxiv.org), all of whose names are something unrecognizable as '1305.5767.pdf' or 'arXiv:hep-th/0612073v2' etc. 

Or even worse, if the user renamed some of the files to its title, eg. '1305.5767.pdf' to 'Categories of Massless D-Branes', it might happens that there are two duplicates '1305.5767.pdf','Categories of Massless D-Branes' on the same path and the user does not realize it.

To help one manage the arXive:Pdf's easily, I write this stuff.
If you have encountered the situation above, then you are encouraged to try this.

How to use it
=============

Open the commandline/terminal and type:

	python arxiv_pyler.py path/to/folder [commands]

If only the html containing info of the Pdf are needed, then one can stop reading here and use arXiv-pyler.

Commands
========

Up to now, **arXiv-pyler** will soon implement commands to pile files in different ways.

###Pile commands(To be implemented)

- flatten: put all files in the same directory path/to/folder
- hierarchy: sort all files according to the arXiv category eg. hep-th pdf's are all collected into the hep-th folder.

Dependencies
============

It runs under Python27.
Following packages are required:

- PyPdf2
- htmltag(already included)

How it works
=============

- gets the `path/to/file`
- scans the arXiv:Pdf
- retrieves infomation of the pdf via arXiv api
- generates the html, where users can open the pdf and look up the info's

Todo
====

- Porting to Python33
- Update the GUI version
- Improve the html_generator.py or implement a simple template engine

On the 'Py2' folder
===================

This folder contains the original version written under Python2.7. The two scripts depends on Pypdf2 and PySide(for the GUI).
To make both scripts work, one has to connect to network.
