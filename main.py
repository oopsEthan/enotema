from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QMenuBar, QMenu, QMessageBox
)
from PySide6.QtGui import QKeySequence, QTextCharFormat, QFont, QAction
from PySide6.QtCore import Qt
from cryptography.fernet import Fernet
import sys, os
from functools import partial

from ui_elements import MENU_DATA

key = b'0a05AKJZCXwFejpTn0gVzc_cFUAG5vCGmcFvywkIdDM='
fernet = Fernet(key)

# Constants / beautifiers
SAVE = "save"
LOAD = "load"

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enotema")
        self.resize(600, 500)

        self.textbox = QTextEdit(self)
        self.setCentralWidget(self.textbox)
        self.setStyleSheet("* { border: none; }")

        self.filename = ""
        self.textbox.textChanged.connect(lambda: self.update_file_ext(True))
        self.create_menu()
        self.bind_shortcuts()

    def create_menu(self):
        menubar = self.menuBar()
        
        external_actions = {
            "textbox.undo": self.textbox.undo,
            "textbox.redo": self.textbox.redo
        }

        for menu in MENU_DATA:
            new_menu = menubar.addMenu(menu["title"])
            for item in menu["items"]:
                action = QAction(item["label"], self)

                if item.get("shortcut"):
                    action.setShortcut(item["shortcut"])
                
                if item["action"] in external_actions:
                    func = external_actions[item["action"]]
                else:
                    func = getattr(self, item["action"])

                params = item.get("params")
                if params:
                    action.triggered.connect(partial(func, *params))
                else:
                    action.triggered.connect(func)

                new_menu.addAction(action)

                if item["end"]:
                    new_menu.addSeparator()

    def bind_shortcuts(self):
        self.textbox.setFocus()
        self.textbox.setShortcutEnabled(True)

        self.textbox.shortcut = QKeySequence(Qt.CTRL | Qt.Key_A)
        self.textbox.addAction(QAction(self, shortcut=self.textbox.shortcut, triggered=self.select_all))

    def new_file(self):
        self.textbox.clear()

    def save_file(self, encrypt=False, force_save=False) -> bool:
        content = self.textbox.toHtml() if self.has_formatting() else self.textbox.toPlainText()

        if not self.filename or force_save:
            self.filename = self.request_filename(SAVE)

        try:
            if encrypt:
                content = fernet.encrypt(content.encode())
                if not self.filename.endswith(".enc"):
                    self.filename = f"{self.filename}.enc"
                with open(self.filename, "wb") as file:
                    file.write(content)
                    QMessageBox.information(self, "Note Saved and Encrypted!", f"Saved to:\n{self.filename}")

            else:
                with open(self.filename, "w", encoding="utf-8") as file:
                    file.write(content)
                    QMessageBox.information(self, "Note Saved!", f"Saved to:\n{self.filename}")

        except Exception as e:
            print("Save failed:", e)
            return False
        
        self.update_file_ext()
        return True

    def open_file(self):
        self.filename = self.request_filename(LOAD)

        try:
            if self.filename.endswith(".enc"):
                with open(self.filename, "rb") as file:
                    content = file.read()
                content = fernet.decrypt(content).decode("utf-8")
            else:
                with open(self.filename, "r", encoding="utf-8") as file:
                    content = file.read()

            self.textbox.setHtml(content)
            
        except Exception as e:
            print("Load failed:", e)
        
        self.update_file_ext()

    def request_filename(self, request):
        if request == LOAD:
            filename, _ = QFileDialog.getOpenFileName(self, "Open Note", "", "Text Files (*.enote *.txt *.enc);;All Files (*)")
        elif request == SAVE and self.has_formatting():
            filename, _ = QFileDialog.getSaveFileName(self, "Save Note", f"{self.filename}", "Enote (*.enote);;All Files (*)")
        elif request == SAVE and not self.has_formatting():
            filename, _ = QFileDialog.getSaveFileName(self, "Save Note", f"{self.filename}", "Text Files (*.txt);;All Files (*)")

        if not filename:
            return ""
        return filename
        
    def update_file_ext(self, change_detected=False):
        if self.filename.endswith(".enc"):
            self.filename = os.path.splitext(self.filename)[0]

        indicator = "*" if change_detected else ""
        self.setWindowTitle(f"Enotema - {self.filename}{indicator}")
        
        self.filename = self.filename

    def select_all(self):
        self.textbox.selectAll()

    def format_text(self, format_request):
        cursor = self.textbox.textCursor()
        if not cursor.hasSelection():
            return

        input_format = cursor.charFormat()
        output_format = QTextCharFormat()

        if format_request == "bold":
            is_bold = input_format.fontWeight() == QFont.Bold
            output_format.setFontWeight(QFont.Normal if is_bold else QFont.Bold)

        elif format_request == "italic":
            is_italics = input_format.fontItalic()
            output_format.setFontItalic(not is_italics)

        elif format_request == "underline":
            is_underlined = input_format.fontUnderline()
            output_format.setFontUnderline(not is_underlined)

        cursor.mergeCharFormat(output_format)

    def has_formatting(self):
        plain = self.textbox.toPlainText()
        html = self.textbox.toHtml()
        return plain != html

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec())