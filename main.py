import customtkinter as ctk
import tkinter as tk
from cryptography.fernet import Fernet

key = b'0a05AKJZCXwFejpTn0gVzc_cFUAG5vCGmcFvywkIdDM='
print(f"Key: {key}")
fernet = Fernet(key)

class NoteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.bind("<Control-s>", lambda event: self.save_note(False))

        self.title("Note Taker")
        self.geometry("600x500")

        # Textbox for writing
        self.textbox = ctk.CTkTextbox(self, width=550, height=400)
        self.textbox.pack(padx=20, pady=20, expand=True, fill="both")

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Note...", command=self.new_note)
        file_menu.add_command(label="Save", command=lambda: self.save_note(False))
        file_menu.add_command(label="Save and Encrypt", command=lambda: self.save_note(True))
        file_menu.add_command(label="Load", command=self.load_note)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Attach menu to window
        self.config(menu=menubar)
    
    def new_note(self):
        self.textbox.delete("1.0", "end")

    def save_note(self, permission_to_encrypt=False) -> bool:
        content = self.textbox.get("1.0", "end").strip()

        filename = tk.filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Note"
        )

        try:
            if permission_to_encrypt:
                content = fernet.encrypt(content.encode())

                if not filename.endswith(".enc"):
                    filename += ".enc"

                with open(filename, "wb") as file:
                    file.write(content)
            else:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(content)
            return True
        
        except Exception as e:
            print("Save failed:", e)
            return False
    
    def load_note(self):
        filename = tk.filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt *.enc"), ("All Files", "*.*")],
            title="Open Note"
        )

        try:
            if filename.endswith(".enc"):
                with open(filename, "rb") as file:
                    content = file.read()
                content = fernet.decrypt(content).decode("utf-8")
            else:
                with open(filename, "r", encoding="utf-8") as file:
                    content = file.read()

            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", content)

        except Exception as e:
            print("Load failed:", e)

if __name__ == "__main__":
    app = NoteApp()
    app.mainloop()
