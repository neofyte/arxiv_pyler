# -*- coding: utf-8 -*-
 
import os, sys, re
import arxiv_pyler

from PySide import QtCore, QtGui

class arxiv_pyler_work(QtCore.QThread):
    
    sinOut = QtCore.Signal(str)
    resultOut = QtCore.Signal(dict, int)
    
    def __init__(self, path, parent=None):
        QtCore.QThread.__init__(self)
        self.exiting = False
        #self.isWait=False
        self.entry_list=[]
        self.path=path
        
    def run(self):
        counter = 0
        for root, dirs, files in os.walk(self.path):
            for pdf in files:
                #try:
                if re.search('.pdf$', pdf):
                    source = os.path.join(root, pdf)
                    self.sinOut.emit('getting identifier of %s' % pdf)
                    identifier = arxiv_pyler.arxiv_id_parser(source, pdf)
                    self.sinOut.emit('querying for %s via arXiv api' % pdf)
                    xml_content = arxiv_pyler.arxiv_query(identifier)
                    self.sinOut.emit('creating entries for %s' % pdf)
                    entry_content = arxiv_pyler.xml_parser(xml_content, identifier)
                    entry_content['file_source']=source
                    self.entry_list.append(entry_content)
                    self.resultOut.emit(self.entry_list[counter], counter)
                    counter +=1
                    #shutil.move(source, pdf_dir)
                #except:
                    #continue
        arxiv_pyler.html_generator(self.entry_list)
        self.sinOut.emit('complete')
        
        #return self.entry_list

class arxiv_pyler_gui(QtGui.QWidget):
    def __init__(self, parent=None):
        super(arxiv_pyler_gui, self).__init__()
        
        self.setWindowTitle("arXiv.Pyler 0.1")
        x, y, w, h = 300, 200, 600, 400
        self.setGeometry(x, y, w, h)
        
        #buttons
        browseButton = self.createButton("&Browse...", self.browse)
        scanButton = self.createButton("&Scan", self.scan)
        
        #dir box
        self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
        
        self.statusLabel = QtGui.QLabel()

        self.createFilesTable()
        
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(browseButton, 0, 0)
        mainLayout.addWidget(self.directoryComboBox, 0, 1)
        mainLayout.addWidget(scanButton, 1, 0)
        mainLayout.addWidget(self.statusLabel, 1, 1, 1, 2)
        mainLayout.addWidget(self.filesTable, 2, 0, 1, 3)
        self.setLayout(mainLayout)

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button
    
    def createComboBox(self, text=""):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Preferred)
        return comboBox
    
    def createFilesTable(self):
        self.filesTable = QtGui.QTableWidget(0, 4)
        self.filesTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.filesTable.setHorizontalHeaderLabels(("#", "id", "title", "author"))
        self.filesTable.horizontalHeader()#.setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)
        self.filesTable.setColumnWidth(0,50)
        self.filesTable.setColumnWidth(1,150)
        self.filesTable.setColumnWidth(2,250)
        self.filesTable.setColumnWidth(3,150)

        self.filesTable.cellActivated.connect(self.openFileOfItem)
    
    @QtCore.Slot(str)
    def set_statusLabel(self, text):
        self.statusLabel.setText(text)
        print text
        
    def scan(self):
        path = self.directoryComboBox.currentText()
        
        if path==None:
            pass
        
        file_counter=0
        for root, dirs, files in os.walk(path):
            for pdf in files:
                if re.search('.pdf$', pdf):
                    file_counter+=1

        self.thread = arxiv_pyler_work(path=path)
        self.thread.sinOut.connect(self.set_statusLabel, QtCore.Qt.QueuedConnection)
        self.thread.resultOut.connect(self.showEntries, QtCore.Qt.QueuedConnection)
        entry_list=self.thread.start()
        #self.thread.arxiv_pyler_main()

        #arxiv_pyler.html_generator(entry_list)
        #self.showEntries(entry_list)
    
    def browse(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Add Pdf Directory",
                QtCore.QDir.currentPath())

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(self.directoryComboBox.findText(directory))
            
    def openFileOfItem(self, row, column):
        item = self.filesTable.item(row, 0)

        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.currentDir.absoluteFilePath(item.text())))
        
    @QtCore.Slot(dict, int)
    def showEntries(self, entry, counter):
        #COUNTER=1
        #for entry in entry_list:
            
        counter_col = QtGui.QTableWidgetItem(str(counter+1))
        id_col = QtGui.QTableWidgetItem(entry['identifier'])
        title_col = QtGui.QTableWidgetItem(entry['title'])
        author_col = QtGui.QTableWidgetItem(', '.join(entry['author']))
        
        #fileNameItem = QtGui.QTableWidgetItem(fn)
        #fileNameItem.setFlags(fileNameItem.flags() ^ QtCore.Qt.ItemIsEditable)

        row = self.filesTable.rowCount()
        self.filesTable.insertRow(row)
        self.filesTable.setItem(row, 0, counter_col)
        self.filesTable.setItem(row, 1, id_col)
        self.filesTable.setItem(row, 2, title_col)
        self.filesTable.setItem(row, 3, author_col)
            
            #COUNTER += 1
        


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    arxiv_pyler_gui = arxiv_pyler_gui()
    arxiv_pyler_gui.show()
    sys.exit(app.exec_())