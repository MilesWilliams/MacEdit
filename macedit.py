import sys
from PyQt5 import QtGui, QtCore
from PyQt5 import QtPrintSupport
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, QFileDialog, QDialog
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.filename = ""
        self.initUI()

    def initToolbar(self):

        self.newAction = QAction(QtGui.QIcon("icons/new.png"), "New", self)
        self.newAction.setStatusTip("Create a new document")
        self.newAction.setShortcut("ctrl+N")
        self.newAction.triggered.connect(self.new)

        self.openAction = QAction(QtGui.QIcon("icons/open.png"), "Open file", self)
        self.openAction.setStatusTip("Open and existing document")
        self.openAction.setShortcut("ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QAction(QtGui.QIcon("icons/save.png"), "Save", self)
        self.saveAction.setStatusTip("Save your document")
        self.saveAction.setShortcut("ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        # Makes the next toolbar appear under this one
        self.addToolBarBreak()

        self.printAction = QAction(QtGui.QIcon("icons/print.png"), "Print document", self)
        self.printAction.setStatusTip("Print the document")
        self.printAction.setShortcut("ctrl+P")
        self.printAction.triggered.connect(self.print)

        self.previewAction = QAction(QtGui.QIcon("icons/preview.png"), "Preview document", self)
        self.previewAction.setStatusTip("Preview this document before printing")
        self.previewAction.setShortcut("ctrl+shift+P")
        self.previewAction.triggered.connect(self.preview)

        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)

        self.addToolBarBreak()

    def initFormatbar(self):

        self.formatBar = self.addToolBar("Format")

    def initMenuBar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)


    def initUI(self):

        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)

        self.initToolbar()
        self.initFormatbar()
        self.initMenuBar()

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()
        # x and y coords on the screen
        self.setGeometry(100, 100, 1030, 800)

        self.setWindowTitle('MacEdit')

    def new(self):

        create = MainWindow(self)
        create.show()

    def open(self):

        # Get file name and show only .macedit files
        self.filename = QFileDialog.getOpenFileName(self, 'Open file',".","(*.macedit)")[0]

        if self.filename:
            with open(self.filename, "rt") as file:
                self.text.setText(file.read())

    def save(self):

        # Only open dialog if there is no filename yet
        if not self.filename:
            self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]

        # Append extension if not there yet
        if not self.filename.endswith(".macedit"):
            self.filename += ".macedit"

        # We just store the contents of the text file along with the format in
        # html
        with open(self.filename, "wt") as file:
            file.write(self.text.toHtml())

    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()

        # If a print is requested, open up the print dialogue
        preview.paintRequested.connect(lambda p: self.text.print_(p))

        preview.exec_()

    def print(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec() == QDialog.Accepted:
            self.text.document().print_(dialog.printer())


def main():

    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
