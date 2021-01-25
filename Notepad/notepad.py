import os
import sys
from PySide2.QtGui import QKeySequence, QFont
from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtPrintSupport import QPrintDialog
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QPlainTextEdit, QWidget, QStatusBar, QToolBar, QAction, \
    QMessageBox, QFileDialog, QApplication


class Notepad(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Notepad, self).__init__(*args, **kwargs)

        self.setGeometry(200, 100, 700, 400)

        self.setStyleSheet("background-color: rgb(50, 50, 55);\n"
                           "font: 11pt \"Roboto\";\n"
                           "color: rgb(255, 255, 255);")

        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont('Roboto', 12))

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)
        open_file_action.setShortcut(QKeySequence('Ctrl+O'))

        save_file_action = QAction(QIcon(), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)
        save_file_action.setShortcut(QKeySequence('Ctrl+S'))

        saveas_file_action = QAction(QIcon(), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)
        saveas_file_action.setShortcut(QKeySequence('Ctrl+Shift+S'))

        print_action = QAction(QIcon(), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)
        print_action.setShortcut(QKeySequence('Ctrl+P'))

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        undo_action.setShortcut(QKeySequence('Ctrl+Z'))

        redo_action = QAction(QIcon(), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)
        redo_action.setShortcut(QKeySequence('Ctrl+Y'))

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)
        cut_action.setShortcut(QKeySequence('Ctrl+X'))

        copy_action = QAction(QIcon(), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)
        copy_action.setShortcut(QKeySequence('Ctrl+C'))

        paste_action = QAction(QIcon(), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)
        paste_action.setShortcut(QKeySequence('Ctrl+V'))

        select_action = QAction(QIcon(), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)
        select_action.setShortcut(QKeySequence('Ctrl+A'))

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        self.update_title()
        self.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt)")

        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path is None:
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt)")

        if not path:
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - Notepad" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Notepad()
    win.show()
    sys.exit(app.exec_())
