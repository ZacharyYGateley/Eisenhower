import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser as cc
from tkinter import PhotoImage as pi
import Styles as sty
import pathlib, os
import re

class Settings:
    """Eisenhower Matrix Settings."""
    def __init__(self, settings = {}):
        def extract(key, default):
            return settings[key] if key in settings else default

        # Matrix background colors
        self.bgm_1 = extract('bgm_1', sty.bg['iu'])
        self.bgm_2 = extract('bgm_2', sty.bg['inu'])
        self.bgm_3 = extract('bgm_3', sty.bg['niu'])
        self.bgm_4 = extract('bgm_4', sty.bg['ninu'])
        # Side note background colors
        self.bgn_1 = extract('bgn_1', '#ffffff')
        self.bgn_2 = extract('bgn_2', '#ffffff')
        self.bgn_3 = extract('bgn_3', '#ffffff')
        self.bgn_4 = extract('bgn_4', '#ffffff')
        # Matrix foreground colors
        self.fgm_1 = extract('fgm_1', '#000000')
        self.fgm_2 = extract('fgm_2', '#000000')
        self.fgm_3 = extract('fgm_3', '#000000')
        self.fgm_4 = extract('fgm_4', '#000000')
        # Side note foreground colors
        self.fgn_1 = extract('fgn_1', '#000000')
        self.fgn_2 = extract('fgn_2', '#000000')
        self.fgn_3 = extract('fgn_3', '#000000')
        self.fgn_4 = extract('fgn_4', '#000000')
        # Universal font size
        self.font_family = extract('font_family', sty.font_mono())
        self.font_size = int(extract('font_size', 12)) or 12
        self.set_font()
        # Side note headers
        self.notes_1 = extract('notes_1', 'Notes 1')
        self.notes_2 = extract('notes_2', 'Notes 2')
        self.notes_3 = extract('notes_3', 'Notes 3')
        self.notes_4 = extract('notes_4', 'Notes 4')
        # Tab width in chars and in pixels
        self.tab_chars = int(extract('tab_chars', 2)) or 1
        self.set_tab_width()
        self.title = extract('title', 'Eisenhower To-Do Matrix')

    def export(self):
        return {
            "bgm_1": self.bgm_1,
            "bgm_2": self.bgm_2,
            "bgm_3": self.bgm_3,
            "bgm_4": self.bgm_4,
            "bgn_1": self.bgn_1,
            "bgn_2": self.bgn_2,
            "bgn_3": self.bgn_3,
            "bgn_4": self.bgn_4,
            "fgm_1": self.fgm_1,
            "fgm_2": self.fgm_2,
            "fgm_3": self.fgm_3,
            "fgm_4": self.fgm_4,
            "fgn_1": self.fgn_1,
            "fgn_2": self.fgn_2,
            "fgn_3": self.fgn_3,
            "fgn_4": self.fgn_4,
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

    def set_font(font):
        pass

    def set_font(self):
        self.font = font.Font(family=self.font_family, size=self.font_size)

    def set_tab_width(self):
        self.tab_width = self.font.measure(' '*Settings.valid_tab_chars(self.tab_chars))

    def valid_tab_chars(tab_chars):
        # Tkinter requires non-zero tab-width
        return int(tab_chars or 2) or 2

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
        
        # Color picker image
        img_file_name = "images/color_picker.png"
        current_dir = pathlib.Path(__file__).parent.resolve()
        img_path = os.path.join(current_dir, img_file_name)
        self.picker = tk.PhotoImage(file=img_path)

        # Grid top row
        # Matrix title
        top = ttk.Frame(window)
        tk.Label(top, text="Matrix Title", font=sty.font['header3']).grid(row=0, column=0, sticky="E", padx=(0, 5), pady=10)
        self.entry['title'] = ttk.Entry(top, font=sty.font['header3'])
        self.entry['title'].grid(row=0, column=1, sticky="W")
        self.entry['title'].insert(0, settings.get('title'))

        # Title separator
        sep = ttk.Separator(window, orient="vertical")

        # Grid left column
        notes_headers = ttk.Frame(window)

        # Note headers
        tk.Label(notes_headers, text='Side Notes', font=sty.font['header3']).grid(row=0, column=0, columnspan=2, pady=(0, 5))
        tk.Label(notes_headers, text='Header 1').grid(row=1, column=0, sticky="E")
        tk.Label(notes_headers, text='Header 2').grid(row=2, column=0, sticky="E")
        tk.Label(notes_headers, text='Header 3').grid(row=3, column=0, sticky="E")
        tk.Label(notes_headers, text='Header 4').grid(row=4, column=0, sticky="E")
        self.entry['notes_1'] = ttk.Entry(notes_headers)
        self.entry['notes_2'] = ttk.Entry(notes_headers)
        self.entry['notes_3'] = ttk.Entry(notes_headers)
        self.entry['notes_4'] = ttk.Entry(notes_headers)
        self.entry['notes_1'].grid(row=1, column=1, sticky="W")
        self.entry['notes_2'].grid(row=2, column=1, sticky="W")
        self.entry['notes_3'].grid(row=3, column=1, sticky="W")
        self.entry['notes_4'].grid(row=4, column=1, sticky="W")
        self.entry['notes_1'].insert(0, settings.get('notes_1'))
        self.entry['notes_2'].insert(0, settings.get('notes_2'))
        self.entry['notes_3'].insert(0, settings.get('notes_3'))
        self.entry['notes_4'].insert(0, settings.get('notes_4'))


        # Text settings
        text_settings = tk.Frame(window)

        # Dynamic example
        # Font captured by closure
        f = font.Font(window)
        # Displayed example box
        self.font_ex = tk.Text(text_settings, bg="#ffffff", fg="#000000", width=10, height=2)
        self.font_ex.insert(tk.END, "AaBbCc\r\n\tDdEeFf")
        self.font_ex.configure(state="disabled")
        
        def update_font_ex(event=None):
            # Update floating font
            fam = self.entry['font_family'].get() or sty.font_mono()
            siz = int(self.entry['font_size'].get() or 12)
            f.config(family=fam, size=siz)
            t = f.measure(' '*Settings.valid_tab_chars(self.entry['tab_chars'].get()))
            # Update displayed example box
            self.font_ex.configure(state="normal")
            self.font_ex.configure(font=f, tabs=t)
            self.font_ex.configure(state="disabled")
        
        # Number key only callback
        dcmd = (window.register(self.callback_numeric))

        tk.Label(text_settings, text='Font Settings', font=sty.font['header3']).grid(row=0, column=0, columnspan=2, pady=(0, 5))
        tk.Label(text_settings, text='Font Family').grid(row=1, column=0, sticky="E")
        tk.Label(text_settings, text='Font Size').grid(row=2, column=0, sticky="E")
        tk.Label(text_settings, text='Tab Width').grid(row=3, column=0, sticky="E")
        self.entry['font_family'] = ttk.Combobox(text_settings, values=self.font_families(), state="readonly")
        self.entry['font_size'] = ttk.Entry(text_settings, validate='all', validatecommand=(dcmd, '%P'), width=3)
        self.entry['tab_chars'] = ttk.Entry(text_settings, validate='all', validatecommand=(dcmd, '%P'), width=2)
        self.entry['font_family'].grid(row=1, column=1, sticky="W")
        self.entry['font_size'].grid(row=2, column=1, sticky="W")
        self.entry['tab_chars'].grid(row=3, column=1, sticky="W")
        self.entry['font_family'].set(settings.get('font_family'))
        self.entry['font_size'].insert(0, settings.get('font_size'))
        self.entry['tab_chars'].insert(0, settings.get('tab_chars'))
        self.font_ex.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.entry['font_family'].bind('<<ComboboxSelected>>', update_font_ex)
        self.entry['font_size'].bind('<KeyRelease>', update_font_ex)
        self.entry['tab_chars'].bind('<KeyRelease>', update_font_ex)
        update_font_ex()


        # Custom note colors
        notes_colors = ttk.Frame(window)
        nc_header = ttk.Frame(notes_colors)
        tk.Label(nc_header, text='Side Notes', font=sty.font['header3']).pack()
        ttk.Button(nc_header, text="Defaults", command=self.default_note_colors).place(relx=1.0, rely=0.5, anchor="e")
        nc_header.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="EW")

        notes_bg = ttk.Frame(notes_colors)
        notes_fg = ttk.Frame(notes_colors)
        
        # Backgrounds
        (self.entry['bgn_1'], self.entry['bgn_2'], self.entry['bgn_3'], self.entry['bgn_4']) = self.build_colorset(notes_bg, 
                            ('BG 1', 'BG 2', 'BG 3', 'BG 4'), 
                            (settings.get('bgn_1'), settings.get('bgn_2'), settings.get('bgn_3'), settings.get('bgn_4')))
        
        # Foregrounds
        (self.entry['fgn_1'], self.entry['fgn_2'], self.entry['fgn_3'], self.entry['fgn_4']) = self.build_colorset(notes_fg, 
                            ('FG 1', 'FG 2', 'FG 3', 'FG 4'), 
                            (settings.get('fgn_1'), settings.get('fgn_2'), settings.get('fgn_3'), settings.get('fgn_4')))

        notes_bg.grid(row=1, column=0)
        notes_fg.grid(row=1, column=1, padx=(10, 0))



        # Matrix colors
        matrix_colors = ttk.Frame(window)
        mc_header = ttk.Frame(matrix_colors)
        tk.Label(mc_header, text='Matrix', font=sty.font['header3']).pack()
        ttk.Button(mc_header, text="Defaults", command=self.default_matrix_colors).place(relx=1.0, rely=0.5, anchor="e")
        mc_header.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="EW")


        matrix_bg = ttk.Frame(matrix_colors)
        matrix_fg = ttk.Frame(matrix_colors)
        
        # Backgrounds
        (self.entry['bgm_1'], self.entry['bgm_2'], self.entry['bgm_3'], self.entry['bgm_4']) = self.build_colorset(matrix_bg, 
                            ('BG 1', 'BG 2', 'BG 3', 'BG 4'), 
                            (settings.get('bgm_1'), settings.get('bgm_2'), settings.get('bgm_3'), settings.get('bgm_4')))
        
        # Foregrounds
        (self.entry['fgm_1'], self.entry['fgm_2'], self.entry['fgm_3'], self.entry['fgm_4']) = self.build_colorset(matrix_fg, 
                            ('FG 1', 'FG 2', 'FG 3', 'FG 4'), 
                            (settings.get('fgm_1'), settings.get('fgm_2'), settings.get('fgm_3'), settings.get('fgm_4')))

        matrix_bg.grid(row=1, column=0)
        matrix_fg.grid(row=1, column=1, padx=(10, 0))


        # Bottom row
        # Interaction buttons
        bottom = ttk.Frame(window)
        ttk.Button(bottom, text="Update", command=self.save).grid(row=0, column=0)
        ttk.Button(bottom, text="Cancel", command=self.close).grid(row=0, column=1)

        
        top.grid(row=0, column=0, columnspan=3, pady=10)
        sep.grid(row=1, column=1, rowspan=2, sticky="NS")
        notes_headers.grid(row=1, column=0, sticky="NS", padx=10, pady=10)
        text_settings.grid(row=1, column=2, padx=10, sticky="NS", pady=10)
        notes_colors.grid(row=2, column=0, sticky="NS", padx=10, pady=10)
        matrix_colors.grid(row=2, column=2, sticky="NS", padx=10, pady=10)
        bottom.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

        # Make sure self.window is erased on window destroy
        window.protocol("WM_DELETE_WINDOW", self.close)
        window.bind('<Return>', lambda event: self.save())
    
    def build_colorset(self, parent, labels, colors):
        tk.Label(parent, text=labels[0]).grid(row=1, column=0)
        tk.Label(parent, text=labels[1]).grid(row=2, column=0)
        tk.Label(parent, text=labels[2]).grid(row=3, column=0)
        tk.Label(parent, text=labels[3]).grid(row=4, column=0)
        c_1 = colors[0]
        c_2 = colors[1]
        c_3 = colors[2]
        c_4 = colors[3]
        color_1 = ttk.Entry(parent, width=8)
        color_2 = ttk.Entry(parent, width=8)
        color_3 = ttk.Entry(parent, width=8)
        color_4 = ttk.Entry(parent, width=8)
        color_1.grid(row=1, column=1)
        color_2.grid(row=2, column=1)
        color_3.grid(row=3, column=1)
        color_4.grid(row=4, column=1)
        color_1.insert(0, c_1)
        color_2.insert(0, c_2)
        color_3.insert(0, c_3)
        color_4.insert(0, c_4)
        ex_1 = tk.Frame(parent, bg=c_1, width=16, height=16)
        ex_2 = tk.Frame(parent, bg=c_2, width=16, height=16)
        ex_3 = tk.Frame(parent, bg=c_3, width=16, height=16)
        ex_4 = tk.Frame(parent, bg=c_4, width=16, height=16)
        ex_1.grid(row=1, column=2, sticky="NSEW", padx=2, pady=2)
        ex_2.grid(row=2, column=2, sticky="NSEW", padx=2, pady=2)
        ex_3.grid(row=3, column=2, sticky="NSEW", padx=2, pady=2)
        ex_4.grid(row=4, column=2, sticky="NSEW", padx=2, pady=2)
        color_1.color_set = lambda event=None: self.color_set(color_1, ex_1)
        color_2.color_set = lambda event=None: self.color_set(color_2, ex_2)
        color_3.color_set = lambda event=None: self.color_set(color_3, ex_3)
        color_4.color_set = lambda event=None: self.color_set(color_4, ex_4)
        ttk.Button(parent, image=self.picker, command=lambda: self.color_pick(color_1, ex_1), width=1).grid(row=1, column=3)
        ttk.Button(parent, image=self.picker, command=lambda: self.color_pick(color_2, ex_2), width=1).grid(row=2, column=3)
        ttk.Button(parent, image=self.picker, command=lambda: self.color_pick(color_3, ex_3), width=1).grid(row=3, column=3)
        ttk.Button(parent, image=self.picker, command=lambda: self.color_pick(color_4, ex_4), width=1).grid(row=4, column=3)
        color_1.bind('<KeyRelease>', color_1.color_set)
        color_2.bind('<KeyRelease>', color_2.color_set)
        color_3.bind('<KeyRelease>', color_3.color_set)
        color_4.bind('<KeyRelease>', color_4.color_set)

        return (color_1, color_2, color_3, color_4)

    def callback_numeric(self, key):
        if str.isdigit(key) or key == "":
            return True
        else:
            return False

    def color_pick(self, field, sample):
        """Select color from color picker."""
        color_code = cc.askcolor(title="Choose color", color=field.get())
        if color_code[1] is not None:
            field.delete(0, tk.END)
            field.insert(0, color_code[1])
            self.color_set(field, sample)
    
    def color_set(self, field, sample):
        """Set color of example square if color is valid."""
        # Only accept hex colors
        valid_color = re.compile(r'^#([\dabcdefABCDEF]{3}){1,2}$')
        color = field.get()
        if not isinstance(re.search(valid_color, color), re.Match):
            # Invalid color? Set to background color of window
            color = "#f0f0f0"
        sample.config(bg=color)
        

    def default_matrix_colors(self):
        default = Settings()
        for i in range(0, 4):
            key = 'gm_' + str(i + 1)
            bg = self.entry['b' + key]
            bg.delete(0, tk.END)
            bg.insert(0, default.get('b' + key))
            bg.color_set()
            fg = self.entry['f' + key]
            fg.delete(0, tk.END)
            fg.insert(0, default.get('f' + key))
            fg.color_set()
    
    def default_note_colors(self):
        default = Settings()
        for i in range(0, 4):
            key = 'gn_' + str(i + 1)
            bg = self.entry['b' + key]
            bg.delete(0, tk.END)
            bg.insert(0, default.get('b' + key))
            bg.color_set()
            fg = self.entry['f' + key]
            fg.delete(0, tk.END)
            fg.insert(0, default.get('f' + key))
            fg.color_set()

    def focus(self):
        """Forces window focus. Used when attempt to open setting when settings already open."""
        self.window.focus_force()

    def font_families(self):
        return list(font.families())

    def is_closed(self):
        """Check if window has been destroyed."""
        return self.window is None

    def save(self):
        """Update Settings object and pass it to parent. Close window."""
        self.settings.set('bgm_1', self.entry['bgm_1'].get())
        self.settings.set('bgm_2', self.entry['bgm_2'].get())
        self.settings.set('bgm_3', self.entry['bgm_3'].get())
        self.settings.set('bgm_4', self.entry['bgm_4'].get())
        self.settings.set('bgn_1', self.entry['bgn_1'].get())
        self.settings.set('bgn_2', self.entry['bgn_2'].get())
        self.settings.set('bgn_3', self.entry['bgn_3'].get())
        self.settings.set('bgn_4', self.entry['bgn_4'].get())
        self.settings.set('fgm_1', self.entry['fgm_1'].get())
        self.settings.set('fgm_2', self.entry['fgm_2'].get())
        self.settings.set('fgm_3', self.entry['fgm_3'].get())
        self.settings.set('fgm_4', self.entry['fgm_4'].get())
        self.settings.set('fgn_1', self.entry['fgn_1'].get())
        self.settings.set('fgn_2', self.entry['fgn_2'].get())
        self.settings.set('fgn_3', self.entry['fgn_3'].get())
        self.settings.set('fgn_4', self.entry['fgn_4'].get())
        self.settings.set('font_family', self.entry['font_family'].get())
        self.settings.set('font_size', int(self.entry['font_size'].get()) or 12)
        self.settings.set_font()
        self.settings.set('notes_1', self.entry['notes_1'].get())
        self.settings.set('notes_2', self.entry['notes_2'].get())
        self.settings.set('notes_3', self.entry['notes_3'].get())
        self.settings.set('notes_4', self.entry['notes_4'].get())
        self.settings.set('tab_chars', Settings.valid_tab_chars(self.entry['tab_chars'].get()))
        self.settings.set_tab_width()
        self.settings.set('title', self.entry['title'].get())
        self.parent.settings_set(self.settings)
        self.parent.status_unsaved()

        self.close()

    def close(self):
        """Close window."""
        self.window.destroy()
        self.parent.settings_close()
        self.parent.focus()