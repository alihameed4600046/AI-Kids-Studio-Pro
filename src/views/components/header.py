import tkinter as tk
from tkinter import ttk
import config

class Header(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style='Header.TFrame')
        
        # Application title
        self.title_label = ttk.Label(self, text=config.APP_TITLE, style='Header.TLabel')
        self.title_label.pack(side=tk.LEFT, padx=(10, 0))

        # Application version
        self.version_label = ttk.Label(self, text=config.APP_VERSION, style='Header.TLabel')
        self.version_label.pack(side=tk.RIGHT, padx=(0, 10))

        self.pack(fill=tk.X)

# Ensure theme awareness
def apply_theme(theme):
    ttk.Style().theme_use(theme)

if __name__ == "__main__":
    root = tk.Tk()
    header = Header(root)
    apply_theme('default')  # Replace with actual theme logic
    root.mainloop()