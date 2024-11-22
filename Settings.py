import tkinter as tk
import Styles as sty

class Settings:
    """Eisenhower Matrix Settings."""
    def __init__(self, settings):
        self.font_size = settings['font_size'] if 'font_size' in settings else 12
        self.notes_1 = settings['notes_1'] if 'notes_1' in settings else 'Notes 1'
        self.notes_2 = settings['notes_2'] if 'notes_2' in settings else 'Notes 2'
        self.notes_3 = settings['notes_3'] if 'notes_3' in settings else 'Notes 3'
        self.notes_4 = settings['notes_4'] if 'notes_4' in settings else 'Notes 4'

    def get(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            return None

    def set(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

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

        root = tk.Tk()
        self.root = root

        root.title(parent.title)
        title = tk.Label(root, text='Matrix Settings')
        title.config(font=sty.font['header3'])
        title.pack(expand=True)

        center = tk.Frame(root)

        # Numerical entry only
        dcmd = (root.register(self.numeric_callback))
        
        # Labels
        tk.Label(center, text='Font Size').grid(row=0, column=0, sticky="E")
        tk.Label(center, text='Custom Notes 1').grid(row=1, column=0, sticky="E")
        tk.Label(center, text='Custom Notes 2').grid(row=2, column=0, sticky="E")
        tk.Label(center, text='Custom Notes 3').grid(row=3, column=0, sticky="E")
        tk.Label(center, text='Custom Notes 4').grid(row=4, column=0, sticky="E")
        
        # Fields
        self.entryfs = tk.Entry(center, validate='all', validatecommand=(dcmd, '%P'), width=3)
        self.entry1 = tk.Entry(center)
        self.entry2 = tk.Entry(center)
        self.entry3 = tk.Entry(center)
        self.entry4 = tk.Entry(center)

        self.entryfs.grid(row=0, column=1, sticky="W")
        self.entry1.grid(row=1, column=1, sticky="W")
        self.entry2.grid(row=2, column=1, sticky="W")
        self.entry3.grid(row=3, column=1, sticky="W")
        self.entry4.grid(row=4, column=1, sticky="W")

        # Set default values
        self.entryfs.insert(0, settings.get('font_size'))
        self.entry1.insert(0, settings.get('notes_1'))
        self.entry2.insert(0, settings.get('notes_2'))
        self.entry3.insert(0, settings.get('notes_3'))
        self.entry4.insert(0, settings.get('notes_4'))

        center.pack(fill="both", expand=True, padx=10, pady=10)

        submit = tk.Frame(root)
        tk.Button(submit, text="Update", command=self.save).grid(row=0, column=0)
        tk.Button(submit, text="Cancel", command=self.root.destroy).grid(row=0, column=1)
        submit.pack(padx=20, pady=10)

        # Make sure self.root is erased on window destroy
        root.protocol("WM_DELETE_WINDOW", self.close)

    def mainloop(self):
        """Separate from __init__ so that __init__ returns self appropriately."""
        self.root.mainloop()
    
    def focus(self):
        """Forces window focus. Used when attempt to open setting when settings already open."""
        self.root.focus_force()

    def is_closed(self):
        """Check if window has been destroyed."""
        return self.root is None

    def numeric_callback(self, entry):
        if str.isdigit(entry) or entry == "":
            return True
        else:
            return False

    def save(self):
        """Update Settings object and pass it to parent. Close window."""
        self.settings.set('font_size', self.entryfs.get())
        self.settings.set('notes_1', self.entry1.get())
        self.settings.set('notes_2', self.entry2.get())
        self.settings.set('notes_3', self.entry3.get())
        self.settings.set('notes_4', self.entry4.get())
        self.parent.settings_set(self.settings)

        self.close()

    def close(self):
        """Close window."""
        self.root.destroy()
        self.root = None