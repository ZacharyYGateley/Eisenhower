import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser as cc
from tkinter import PhotoImage as pi
import Styles as sty
import pathlib, os

class Settings:
    """Eisenhower Matrix Settings."""
    def __init__(self, settings):
        def extract(key, default):
            return settings[key] if key in settings else default

        self.bg_1 = extract('bg_1', sty.bg['iu'])
        self.bg_2 = extract('bg_2', sty.bg['inu'])
        self.bg_3 = extract('bg_3', sty.bg['niu'])
        self.bg_4 = extract('bg_4', sty.bg['ninu'])
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
            "bg_1": self.bg_1,
            "bg_2": self.bg_2,
            "bg_3": self.bg_3,
            "bg_4": self.bg_4,
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
        self.window.iconbitmap('images/feather.ico')
        window.title('Matrix Settings')
        
        # Number key only callback
        dcmd = (window.register(self.callback_numeric))

        # Color picker image
        img_file_name = "images/color_picker.png"
        current_dir = pathlib.Path(__file__).parent.resolve()
        img_path = os.path.join(current_dir, img_file_name)
        self.picker = tk.PhotoImage(file=img_path)

        # Grid top row
        # Matrix title
        top = ttk.Frame(window)
        tk.Label(top, text="Matrix Title", font=sty.font['header3']).grid(row=0, column=0, sticky="E")
        self.entry['title'] = ttk.Entry(top, font=sty.font['header3'])
        self.entry['title'].grid(row=0, column=1, sticky="W")
        self.entry['title'].insert(0, settings.get('title'))
        top.grid(row=0, column=0, columnspan=2, pady=10)

        # Title separator
        sep = ttk.Separator(window, orient="horizontal")
        sep.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Grid left column
        left = ttk.Frame(window)

        # Note headers
        tk.Label(left, text='Headers', font=sty.font['header3']).grid(row=0, column=0, columnspan=2)
        tk.Label(left, text='Custom Notes 1').grid(row=1, column=0, sticky="E")
        tk.Label(left, text='Custom Notes 2').grid(row=2, column=0, sticky="E")
        tk.Label(left, text='Custom Notes 3').grid(row=3, column=0, sticky="E")
        tk.Label(left, text='Custom Notes 4').grid(row=4, column=0, sticky="E")
        self.entry['notes_1'] = ttk.Entry(left)
        self.entry['notes_2'] = ttk.Entry(left)
        self.entry['notes_3'] = ttk.Entry(left)
        self.entry['notes_4'] = ttk.Entry(left)
        self.entry['notes_1'].grid(row=1, column=1, sticky="W")
        self.entry['notes_2'].grid(row=2, column=1, sticky="W")
        self.entry['notes_3'].grid(row=3, column=1, sticky="W")
        self.entry['notes_4'].grid(row=4, column=1, sticky="W")
        self.entry['notes_1'].insert(0, settings.get('notes_1'))
        self.entry['notes_2'].insert(0, settings.get('notes_2'))
        self.entry['notes_3'].insert(0, settings.get('notes_3'))
        self.entry['notes_4'].insert(0, settings.get('notes_4'))

        # Styles
        tk.Label(left, text='Styles', font=sty.font['header3']).grid(row=5, column=0, columnspan=4, pady=(5, 0))
        tk.Label(left, text='Font Size').grid(row=6, column=0, sticky="E")
        tk.Label(left, text='Tab Width').grid(row=7, column=0, sticky="E")
        self.entry['font_size'] = ttk.Entry(left, validate='all', validatecommand=(dcmd, '%P'), width=3)
        self.entry['tab_chars'] = ttk.Entry(left, validate='all', validatecommand=(dcmd, '%P'), width=2)
        self.entry['font_size'].grid(row=6, column=1, sticky="W")
        self.entry['tab_chars'].grid(row=7, column=1, sticky="W")
        self.entry['font_size'].insert(0, settings.get('font_size'))
        self.entry['tab_chars'].insert(0, settings.get('tab_chars'))

        left.grid(row=3, column=0, sticky="NSEW", padx=10, pady=10)

        # Right column
        # Font size and matrix background colors
        right = ttk.Frame(window)
        
        # Backgrounds
        tk.Label(right, text='Backgrounds', font=sty.font['header3']).grid(row=0, column=0, columnspan=4)
        tk.Label(right, text='Matrix 1').grid(row=1, column=0)
        tk.Label(right, text='Matrix 2').grid(row=2, column=0)
        tk.Label(right, text='Matrix 3').grid(row=3, column=0)
        tk.Label(right, text='Matrix 4').grid(row=4, column=0)
        bg_1 = settings.get('bg_1')
        bg_2 = settings.get('bg_2')
        bg_3 = settings.get('bg_3')
        bg_4 = settings.get('bg_4')
        self.entry['bg_1'] = ttk.Entry(right, width=7)
        self.entry['bg_2'] = ttk.Entry(right, width=7)
        self.entry['bg_3'] = ttk.Entry(right, width=7)
        self.entry['bg_4'] = ttk.Entry(right, width=7)
        self.entry['bg_1'].grid(row=1, column=1)
        self.entry['bg_2'].grid(row=2, column=1)
        self.entry['bg_3'].grid(row=3, column=1)
        self.entry['bg_4'].grid(row=4, column=1)
        self.entry['bg_1'].insert(0, settings.get('bg_1'))
        self.entry['bg_2'].insert(0, settings.get('bg_2'))
        self.entry['bg_3'].insert(0, settings.get('bg_3'))
        self.entry['bg_4'].insert(0, settings.get('bg_4'))
        ex_1 = tk.Frame(right, bg=bg_1, width=16, height=16)
        ex_2 = tk.Frame(right, bg=bg_2, width=16, height=16)
        ex_3 = tk.Frame(right, bg=bg_3, width=16, height=16)
        ex_4 = tk.Frame(right, bg=bg_4, width=16, height=16)
        ex_1.grid(row=1, column=2, sticky="NSEW", padx=2, pady=2)
        ex_2.grid(row=2, column=2, sticky="NSEW", padx=2, pady=2)
        ex_3.grid(row=3, column=2, sticky="NSEW", padx=2, pady=2)
        ex_4.grid(row=4, column=2, sticky="NSEW", padx=2, pady=2)
        ttk.Button(right, image=self.picker, command=lambda: self.colorpick(self.entry['bg_1'], ex_1), width=1).grid(row=1, column=3)
        ttk.Button(right, image=self.picker, command=lambda: self.colorpick(self.entry['bg_2'], ex_2), width=1).grid(row=2, column=3)
        ttk.Button(right, image=self.picker, command=lambda: self.colorpick(self.entry['bg_3'], ex_3), width=1).grid(row=3, column=3)
        ttk.Button(right, image=self.picker, command=lambda: self.colorpick(self.entry['bg_4'], ex_4), width=1).grid(row=4, column=3)

        right.grid(row=3, column=1, sticky="NSEW", padx=10, pady=10)

        # Bottom row
        # Interaction buttons
        bottom = ttk.Frame(window)
        ttk.Button(bottom, text="Update", command=self.save).grid(row=0, column=0)
        ttk.Button(bottom, text="Cancel", command=self.close).grid(row=0, column=1)
        bottom.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

        # Make sure self.window is erased on window destroy
        window.protocol("WM_DELETE_WINDOW", self.close)
        window.bind('<Return>', lambda event: self.save())

    def colorpick(self, field, sample):
        color_code = cc.askcolor(title="Choose color", color=field.get())
        if color_code[1] is not None:
            field.delete(0, tk.END)
            field.insert(0, color_code[1])
            sample.config(bg=color_code[1])

    def focus(self):
        """Forces window focus. Used when attempt to open setting when settings already open."""
        self.window.focus_force()

    def is_closed(self):
        """Check if window has been destroyed."""
        return self.window is None

    def callback_numeric(self, key):
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