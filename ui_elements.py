from PySide6.QtGui import QKeySequence

# DEFAULT_MENU_ITEM =
# {"label": "", "action": "", "shortcut": None, "params": [], "end": False},

MENU_DATA = [
    {
        "title": "File",
        "items": [
            {"label": "New File...", "action": "new_file", "shortcut": None, "params": [], "end": True},
            {"label": "Save", "action": "save_file", "shortcut": QKeySequence.Save, "params": [False, False], "end": False},
            {"label": "Save As...", "action": "save_file", "shortcut": QKeySequence.SaveAs, "params": [False, True], "end": False},
            {"label": "Save and Encrypt", "action": "save_file", "shortcut": QKeySequence("Ctrl+Alt+S"), "params": [True, True], "end": True},
            {"label": "Open File...", "action": "open_file", "shortcut": QKeySequence.Open, "params": [], "end": True},
            {"label": "Exit", "action": "close", "shortcut": None, "end": False}
        ]
    },
    {
        "title": "Edit",
        "items": [
                {"label": "Undo", "action": "textbox.undo", "shortcut": QKeySequence.Undo, "params": [] , "end": False},
                {"label": "Redo", "action": "textbox.redo", "shortcut": QKeySequence.Redo, "params": [] , "end": False}
        ]
    },
    {
        "title": "Format",
        "items": [
                {"label": "Bold", "action": "format_text", "shortcut": QKeySequence.Bold, "params": ["bold"] , "end": False},
                {"label": "Italic", "action": "format_text", "shortcut": QKeySequence.Italic, "params": ["italic"] , "end": False},
                {"label": "Underline", "action": "format_text", "shortcut": QKeySequence.Underline, "params": ["underline"] , "end": False}
        ]
    }
]
