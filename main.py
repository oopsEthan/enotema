from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QMenuBar, QMenu
)
from PySide6.QtGui import QKeySequence, QTextCharFormat, QFont, QAction
from PySide6.QtCore import Qt
from cryptography.fernet import Fernet
import sys

key = b'0a05AKJZCXwFejpTn0gVzc_cFUAG5vCGmcFvywkIdDM='
fernet = Fernet(key)

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enotema")
        self.resize(600, 500)

        self.textbox = QTextEdit(self)
        self.setCentralWidget(self.textbox)

        self.create_menu()
        self.bind_shortcuts()

    def create_menu(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")

        new_action = QAction("New Note...", self)
        new_action.triggered.connect(self.new_note)
        file_menu.addAction(new_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_note)
        file_menu.addAction(save_action)

        save_enc_action = QAction("Save and Encrypt", self)
        save_enc_action.triggered.connect(lambda: self.save_note(True))
        file_menu.addAction(save_enc_action)

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_note)
        file_menu.addAction(load_action)

        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        # Edit Menu
        edit_menu = menubar.addMenu("Edit")

        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.textbox.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.textbox.redo)
        edit_menu.addAction(redo_action)

    def bind_shortcuts(self):
        self.textbox.setFocus()
        self.textbox.setShortcutEnabled(True)

        self.textbox.shortcut = QKeySequence(Qt.CTRL | Qt.Key_A)
        self.textbox.addAction(QAction(self, shortcut=self.textbox.shortcut, triggered=self.select_all))

        bold_action = QAction(self)
        bold_action.setShortcut(QKeySequence.Bold)
        bold_action.triggered.connect(self.bold_text)
        self.addAction(bold_action)

    def new_note(self):
        self.textbox.clear()

    def save_note(self, encrypt=False):
        content = self.textbox.toPlainText()

        filename, _ = QFileDialog.getSaveFileName(self, "Save Note", "", "Text Files (*.txt);;All Files (*)")
        if not filename:
            return

        try:
            if encrypt:
                content = fernet.encrypt(content.encode())
                if not filename.endswith(".enc"):
                    filename += ".enc"
                with open(filename, "wb") as file:
                    file.write(content)
            else:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(content)
        except Exception as e:
            print("Save failed:", e)

    def load_note(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Note", "", "Text Files (*.txt *.enc);;All Files (*)")
        if not filename:
            return

        try:
            if filename.endswith(".enc"):
                with open(filename, "rb") as file:
                    content = file.read()
                content = fernet.decrypt(content).decode("utf-8")
            else:
                with open(filename, "r", encoding="utf-8") as file:
                    content = file.read()

            self.textbox.setPlainText(content)
        except Exception as e:
            print("Load failed:", e)

    def select_all(self):
        self.textbox.selectAll()

    def bold_text(self):
        cursor = self.textbox.textCursor()
        if cursor.hasSelection():
            fmt = QTextCharFormat()
            fmt.setFontWeight(QFont.Bold)
            cursor.mergeCharFormat(fmt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec())