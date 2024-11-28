import tkinter as tk
from tkinter import font
import Styles as sty

class Settings:
    """Eisenhower Matrix Settings."""
    def __init__(self, settings):
        def extract(key, default):
            return settings[key] if key in settings else default

        self.font_size = int(extract('font_size', 12)) or 12
        self.set_font()
        self.notes_1 = extract('notes_1', 'Notes 1')
        self.notes_2 = extract('notes_2', 'Notes 2')
        self.notes_3 = extract('notes_3', 'Notes 3')
        self.notes_4 = extract('notes_4', 'Notes 4')
        self.tab_chars = int(extract('tab_chars', 2)) or 1
        self.set_tab_width()
        self.title = extract('title', 'Eisenhower To-Do Matrix')

    def export(self):
        return {
            "font_size": self.font_size,
            "notes_1": self.notes_1,
            "notes_2": self.notes_2,
            "notes_3": self.notes_3,
            "notes_4": self.notes_4,
            "tab_chars": self.tab_chars,
            "tab_width": self.tab_width,
            "title": self.title
        }

    def get(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            return None

    def set(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

    def set_font(self):
        self.font = font.Font(family=sty.font_mono(), size=self.font_size)
    
    def set_tab_width(self, tab_chars=-1):
        tab_chars = (self.tab_chars if tab_chars < 0 else tab_chars) or 1
        self.tab_width = self.font.measure(' '*tab_chars)

class SettingsWindow:
    """Update Eisenhower Matrix Settings.
    
    Retrieves settings from caller.
    Allows user to update settings variables.
    Passes settings back to caller."""
    def __init__(self, parent, settings: Settings):
        self.parent = parent
        if settings is None:
            settings = Settings()
        self.settings = settings

        # Tkinter modifiable fields
        # Entry names match Settings parameters
        self.entry = {}

        # Child window of respective Matrix window
        window = tk.Toplevel(self.parent.window)
        self.window = window
        window.title(parent.title)
        title = tk.Label(window, text='Matrix Settings')
        title.config(font=sty.font['header3'])
        title.grid(row=0, column=0, columnspan=2)
        
        # Number key only callback
        dcmd = (window.register(self.numeric_callback))

        # Grid top row
        # Matrix title
        top = tk.Frame(window)
        tk.Label(top, text="Matrix Title").grid(row=0, column=0, sticky="E")
        self.entry['title'] = tk.Entry(top)
        self.entry['title'].grid(row=0, column=1, sticky="W")
        self.entry['title'].insert(0, settings.get('title'))
        top.grid(row=1, column=0, columnspan=2)

        # Grid left column
        # Note headers
        left = tk.Frame(window)
        tk.Label(left, text='Custom Notes 1').grid(row=1, column=0, sticky="E")
        tk.Label(left, text='Custom Notes 2').grid(row=2, column=0, sticky="E")
        tk.Label(left, text='Custom Notes 3').grid(row=3, column=0, sticky="E")
        tk.Label(left, text='Custom Notes 4').grid(row=4, column=0, sticky="E")
        
        # Fields
        self.entry['notes_1'] = tk.Entry(left)
        self.entry['notes_2'] = tk.Entry(left)
        self.entry['notes_3'] = tk.Entry(left)
        self.entry['notes_4'] = tk.Entry(left)

        self.entry['notes_1'].grid(row=1, column=1, sticky="W")
        self.entry['notes_2'].grid(row=2, column=1, sticky="W")
        self.entry['notes_3'].grid(row=3, column=1, sticky="W")
        self.entry['notes_4'].grid(row=4, column=1, sticky="W")

        # Set default values
        self.entry['notes_1'].insert(0, settings.get('notes_1'))
        self.entry['notes_2'].insert(0, settings.get('notes_2'))
        self.entry['notes_3'].insert(0, settings.get('notes_3'))
        self.entry['notes_4'].insert(0, settings.get('notes_4'))

        left.grid(row=2, column=0, sticky="NSEW", padx=10, pady=10)

        # Right column
        # Font size and matrix background colors
        right = tk.Frame(window)
        
        # Labels
        tk.Label(right, text='Font Size').grid(row=0, column=0, sticky="E")
        tk.Label(right, text='Tab Width').grid(row=1, column=0, sticky="E")
        self.entry['font_size'] = tk.Entry(right, validate='all', validatecommand=(dcmd, '%P'), width=3)
        self.entry['tab_chars'] = tk.Entry(right, validate='all', validatecommand=(dcmd, '%P'), width=2)
        self.entry['font_size'].grid(row=0, column=1, sticky="W")
        self.entry['tab_chars'].grid(row=1, column=1, sticky="W")
        self.entry['font_size'].insert(0, settings.get('font_size'))
        self.entry['tab_chars'].insert(0, settings.get('tab_chars'))

        right.grid(row=2, column=1, sticky="NSEW", padx=10, pady=10)

        # Bottom row
        # Interaction buttons
        bottom = tk.Frame(window)
        tk.Button(bottom, text="Update", command=self.save).grid(row=0, column=0)
        tk.Button(bottom, text="Cancel", command=self.close).grid(row=0, column=1)
        bottom.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

        # Make sure self.window is erased on window destroy
        window.protocol("WM_DELETE_WINDOW", self.close)

    def mainloop(self):
        """Separate from __init__ so that __init__ returns self appropriately."""
        self.window.mainloop()
    
    def focus(self):
        """Forces window focus. Used when attempt to open setting when settings already open."""
        self.window.focus_force()

    def is_closed(self):
        """Check if window has been destroyed."""
        return self.window is None

    def numeric_callback(self, key):
        if str.isdigit(key) or key == "":
            return True
        else:
            return False

    def save(self):
        """Update Settings object and pass it to parent. Close window."""
        self.settings.set('font_size', int(self.entry['font_size'].get()) or 12)
        self.settings.set_font()
        self.settings.set('notes_1', self.entry['notes_1'].get())
        self.settings.set('notes_2', self.entry['notes_2'].get())
        self.settings.set('notes_3', self.entry['notes_3'].get())
        self.settings.set('notes_4', self.entry['notes_4'].get())
        self.settings.set('tab_chars', int(self.entry['tab_chars'].get()))
        self.settings.set_tab_width()
        self.settings.set('title', self.entry['title'].get())
        self.parent.settings_set(self.settings)

        self.close()

    def close(self):
        """Close window."""
        self.window.destroy()
        self.parent.settings_close()