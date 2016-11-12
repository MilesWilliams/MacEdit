import sys
from PyQt5 import QtGui, QtCore
from PyQt5 import QtPrintSupport
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, QFileDialog, QDialog
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.filename = ""
        self.initUI()

    def initToolbar(self):

        self.newAction = QAction(QtGui.QIcon("icons/new.png"),
                                 "New", self)
        self.newAction.setStatusTip("Create a new document")
        self.newAction.setShortcut("ctrl+N")
        self.newAction.triggered.connect(self.new)

        self.openAction = QAction(QtGui.QIcon("icons/open.png"),
                                  "Open file", self)
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

        self.toolbar.addSeparator()

        self.printAction = QAction(QtGui.QIcon("icons/print.png"),
                                   "Print document", self)
        self.printAction.setStatusTip("Print the document")
        self.printAction.setShortcut("ctrl+P")
        self.printAction.triggered.connect(self.print)

        self.previewAction = QAction(QtGui.QIcon("icons/preview.png"),
                                     "Preview document", self)
        self.previewAction.setStatusTip("Preview this document before printing")
        self.previewAction.setShortcut("ctrl+shift+P")
        self.previewAction.triggered.connect(self.preview)

        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)

        self.toolbar.addSeparator()

        self.cutAction = QAction(QtGui.QIcon("icons/cut.png"),
                                 "Cut to clipboard", self)
        self.cutAction.setStatusTip("Delete and cut text to clipboard")
        self.cutAction.setShortcut("ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QAction(QtGui.QIcon("icons/copy.png"),
                                  "Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QAction(QtGui.QIcon("icons/paste.png"),
                                   "Paste to document", self)
        self.pasteAction.setStatusTip("Paste to document")
        self.pasteAction.setShortcut("ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QAction(QtGui.QIcon("icons/undo.png"),
                                  "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QAction(QtGui.QIcon("icons/redo.png"),
                                  "Redo the last undone action", self)
        self.redoAction.setStatusTip("Redo the last undone action")
        self.redoAction.setShortcut("ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()

        bulletAction = QAction(QtGui.QIcon("icons/bullet.png"),
                               "Insert bullet list", self)
        bulletAction.setStatusTip("Insert a bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QAction(QtGui.QIcon("icons/number.png"),
                                 "Insert a numbered list", self)
        numberedAction.setStatusTip("Insert a numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        self.toolbar.addAction(bulletAction)
        self.toolbar.addAction(numberedAction)

        self.toolbar.addSeparator

    def initFormatbar(self):

        self.formatBar = self.addToolBar("Format")

        indentAction = QAction(QtGui.QIcon("icons/indent.png"),
                               "Indent Area", self)
        indentAction.setStatusTip("Indent your text")
        indentAction.setShortcut("Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QAction(QtGui.QIcon("icons/dedent.png"),
                               "Dedent Area", self)
        dedentAction.setStatusTip("Dedent your text")
        dedentAction.setShortcut("shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        self.formatBar.addAction(indentAction)
        self.formatBar.addAction(dedentAction)

    def initMenuBar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)

        # We dont need any seperate slot functions as our QTextEdit object
        # already has very handy methods for all of these actions.
        edit.addAction(self.copyAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)

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

        # Setting PyQt tab length tp 33px
        self.text.setTabStopWidth(33)

        # Setting the window icon
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

        # Displaying the cursor's current line and column number in the
        # status bar
        self.text.cursorPositionChanged.connect(self.cursorPosition)

    def new(self):

        create = MainWindow(self)
        create.show()

    def open(self):

        # Get file name and show only .macedit files
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', ".",
                                                    "(*.macedit)")[0]

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


    # As you can see, we don't make these actions (bulletList and numberList)
    # class members because we don't need to access them anywhere else in our
    # class. We only need to create and use them within the scope of initToolbar
    def bulletList(self):

        cursor = self.text.textCursor()

        # Insert bulleted list
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.text.textCursor()

        # Insert numbered list
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def indent(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            # Iterate over lines
            for n in range(diff + 1):

                # Move to selection of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)

                # Insert Tabbing
                cursor.insertText("\t")

                # And Move Back
                cursor.movePosition(QtGui.QTextCursor.Up)

        # If there is no selection just move cursor
        else:

            cursor.insertText("\t")

    def cursorPosition(self):

        cursor = self.text.textCursor()

        # Starting the index at 1 and not 0
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line, col))

    def dedent(self):

        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            for n in range(diff + 1):

                self.handleDedent(cursor)

                # Move Up
                cursor.movePosition(QtGui.QTextCursor.Up)

        else:
            self.handleDedent(cursor)

    def handleDedent(self, cursor):

        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab charachter, delete it
        if line.startswith("\t"):

            # Delete next charachter
            cursor.deleteChar()

        else:
            for char in line[:8]:

                if char != " ":

                    break

                cursor.deleteChar()


def main():

    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
