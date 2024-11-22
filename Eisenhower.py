import tkinter as tk
from tkinter import scrolledtext as st
from Settings import *
import Styles as sty

class Eisenhower:
    """Master Eisenhower Matrix."""
    def __init__(self, root):
        self.root = root
        self.settings_window = None
        # Volatile matrix settings
        self.settings = Settings({
            'font_size': 12,
            'notes_1': 'Notes 1',
            'notes_2': 'Notes 2',
            'notes_3': 'Notes 3',
            'notes_4': 'Notes 4'
        })
        # Perimeter note labels (tkinter label objects)
        self.notes_label = [ None, None, None, None ]
        # Perimeter note boxes (tkinter text objects)
        self.notes_text = [ None, None, None, None ]
        # Main matrix text boxes (tkinter text objects)
        self.matrix = [ None, None, None, None ]
        
        # 1x3 column grid
        # Column 1: Embedded 2x1 grid
        # Column 2: Embedded 3x3 grid
        # Column 3: Embedded 2x1 grid

        self.title = 'Eisenhower To-Do Matrix'

        root.title(self.title)
        title = tk.Label(root, text=self.title)
        title.config(font=sty.font['header1'])
        title.grid(row=0, column=0, columnspan=3)

        self.build_menu()

        left = tk.Frame(root)
        left.grid(column=0, row=1, sticky="NSEW")
        center = tk.Frame(root, padx=10)
        center.grid(column=1, row=1, sticky="NSEW")
        right = tk.Frame(root)
        right.grid(column=2, row=1, sticky="NSEW")

        # Title row does not expand
        root.rowconfigure(index=1, weight=1)
        # Only matrix column expands
        root.columnconfigure(index=1, weight=1)

        self.build_left(left)
        self.build_center(center)
        self.build_right(right)
    
    def build_menu(self):
        """Build tkinter menu of main window. Used only during __init__."""
        menubar = tk.Menu(self.root) 
  
        # Adding File Menu and commands 
        file = tk.Menu(menubar, tearoff = 0) 
        menubar.add_cascade(label = 'File', menu = file) 
        file.add_command(label = 'New Matrix', command = None) 
        file.add_command(label = 'Open Matrix', command = None) 
        file.add_command(label = 'Save', command = None) 
        file.add_command(label = 'Save As', command = None)
        file.add_separator() 
        file.add_command(label = 'Exit', command = self.close)

        edit = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = 'Edit', menu=edit)
        edit.add_command(label = 'Matrix Settings', command = self.settings_open)

        self.root.config(menu = menubar) 

    def build_left(self, master):
        """Build tkinter left column of main window. Used only during __init__."""
        label_0_text = tk.StringVar()
        label_0_text.set(self.settings.get('notes_1'))
        label_1_text = tk.StringVar()
        label_1_text.set(self.settings.get('notes_2'))

        label_0 = tk.Label(master, textvariable=label_0_text, font=sty.font['header2'], bg=sty.bg['header2'])
        field_0 = st.ScrolledText(master, width=25)
        label_1 = tk.Label(master, textvariable=label_1_text, font=sty.font['header2'], bg=sty.bg['header2'])
        field_1 = st.ScrolledText(master, width=25, height=10)

        label_0.grid(row=0, column=0, sticky="EW")
        field_0.grid(row=1, column=0, sticky="NSEW")
        label_1.grid(row=2, column=0, sticky="EW")
        field_1.grid(row=3, column=0, sticky="NSEW")

        # Save for dynamic access
        self.notes_label[0] = label_0_text
        self.notes_label[1] = label_1_text
        self.notes_text[0] = field_0
        self.notes_text[1] = field_1
        
        master.rowconfigure(index=1, weight=1)

    def build_center(self, master):
        """Build tkinter central column of main window. Used only during __init__."""
        c10 = tk.Frame(master, bg=sty.bg['i'])
        c20 = tk.Frame(master, bg=sty.bg['ni'])

        urgent = tk.Label(master, text='Urgent', font=sty.font['header2'], bg=sty.bg['u'], fg=sty.fg['u'])
        not_urgent = tk.Label(master, text='Not Urgent', font=sty.font['header2'], bg=sty.bg['nu'])
        i_pos=96
        c_hgt=30
        important = tk.Canvas(c10, width = c_hgt, height = i_pos, bg=sty.bg['i'], highlightthickness=0)
        important.create_text(c_hgt/2, i_pos, text = 'Important', angle = 90, anchor = 'w', font=sty.font['header2'], fill=sty.fg['i'])
        important.pack(expand=True)
        ni_pos=136
        not_important = tk.Canvas(c20, width = c_hgt, height=ni_pos, bg=sty.bg['ni'], highlightthickness=0)
        not_important.create_text(c_hgt/2, ni_pos, text = 'Not Important', angle = 90, anchor = 'w', font=sty.font['header2'])
        not_important.pack(expand=True)
        
        urgent.grid(row=0, column=1, sticky="NSEW")
        not_urgent.grid(row=0, column=2, sticky="NSEW")
        c10.grid(row=1, column=0, sticky="NSEW")
        c20.grid(row=2, column=0, sticky="NSEW")

        important_urgent = st.ScrolledText(master, bg=sty.bg['iu'])
        important_not_urgent = st.ScrolledText(master, bg=sty.bg['inu'])
        not_important_urgent = st.ScrolledText(master, bg=sty.bg['niu'])
        not_important_not_urgent = st.ScrolledText(master, bg=sty.bg['ninu'])

        important_urgent.grid(row=1, column=1, sticky="NSEW")
        important_not_urgent.grid(row=1, column=2, sticky="NSEW")
        not_important_urgent.grid(row=2, column=1, sticky="NSEW")
        not_important_not_urgent.grid(row=2, column=2, sticky="NSEW")

        # Save for dynamic access
        self.matrix[0] = important_urgent
        self.matrix[1] = not_important_urgent
        self.matrix[2] = important_not_urgent
        self.matrix[3] = not_important_not_urgent

        # Expand text boxes only
        master.columnconfigure(index=1, weight=1, uniform="column")
        master.columnconfigure(index=2, weight=1, uniform="column")
        master.rowconfigure(index=1, weight=1, uniform="row")
        master.rowconfigure(index=2, weight=1, uniform="row")

        pass

    def build_right(self, master):
        """Build tkinter right column of main window. Used only during __init__."""
        label_0_text = tk.StringVar()
        label_0_text.set(self.settings.get('notes_3'))
        label_1_text = tk.StringVar()
        label_1_text.set(self.settings.get('notes_4'))

        label_0 = tk.Label(master, textvariable=label_0_text, font=sty.font['header2'], bg=sty.bg['header2'])
        field_0 = st.ScrolledText(master, width=25, height=10)
        label_1 = tk.Label(master, textvariable=label_1_text, font=sty.font['header2'], bg=sty.bg['header2'])
        field_1 = st.ScrolledText(master, width=25)

        label_0.grid(row=0, column=0, sticky="EW")
        field_0.grid(row=1, column=0, sticky="NSEW")
        label_1.grid(row=2, column=0, sticky="EW")
        field_1.grid(row=3, column=0, sticky="NSEW")

        # Save for dynamic access
        self.notes_label[2] = label_0_text
        self.notes_label[3] = label_1_text
        self.notes_text[2] = field_0
        self.notes_text[3] = field_1

        master.rowconfigure(index=3, weight=1)

    def close(self):
        self.settings_close()
        self.root.destroy()
        
    def settings_open(self):
        if self.settings_window is None or self.settings_window.is_closed():
            self.settings_window = SettingsWindow(self, self.settings)
            self.settings_window.mainloop()
        else:
            self.settings_window.focus()
    
    def settings_close(self):
        if self.settings_window != None and hasattr(self.settings_window, "destroy") and callable(getattr(self.settings_window, "destroy")):
            self.settings_window.destroy()
        self.settings_window = None

    def settings_set(self, settings: Settings):
        # Only save valid settings. Ignore bad setting keys.
        if isinstance(settings, Settings):
            self.settings = settings
        
        # Repaint window
        for i in range(0, 3):
            self.notes_label[i].set(self.settings.get('notes_' + str(i+1)))
            #self.notes_label[i].update()
        font_size = self.settings.get('font_size')
        for set in (self.notes_text, self.matrix):
            for text in set:
                # Change font size only. Assume font is tuple of family and size.
                text.configure(font=(sty.font['family'], font_size))
                text.update()

def main(): 
    root = tk.Tk()
    app = Eisenhower(root)
    root.mainloop()

if __name__ == '__main__':
    main()