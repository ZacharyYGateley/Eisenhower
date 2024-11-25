import json
from Settings import *
import Styles as sty
import sys
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import scrolledtext as st

open_instances = []
root = None
g_mono_font = None

class Eisenhower:
    """Master Eisenhower Matrix."""
    def __init__(self, root, file_location=""):
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
        # All changes saved?
        self.saved = True
        # File location for saves
        self.file_location = file_location
        # Tab width for text boxes
        self.tab_width = self.settings.get('font').measure('  ')

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

        # Attempt to open file
        if self.file_location != "":
            self.open(file_location=self.file_location)
        
        # Keep track of all open instances
        open_instances.append(self)

        # Make sure self.root is erased on window destroy
        root.protocol("WM_DELETE_WINDOW", self.close)
    
    def build_menu(self):
        """Build tkinter menu of main window. Used only during __init__."""
        menubar = tk.Menu(self.root) 
  
        # Adding File Menu and commands 
        file = tk.Menu(menubar, tearoff = 0) 
        menubar.add_cascade(label = 'File', menu = file) 
        file.add_command(label = 'New Matrix', command = self.new)
        file.add_command(label = 'Open Matrix', command = self.open)
        file.add_command(label = 'Save', command = self.save)
        file.add_command(label = 'Save As', command = self.saveas)
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
        field_0 = st.ScrolledText(master, width=25, font=self.settings.get('font'))
        field_0.config(tabs=self.tab_width)
        label_1 = tk.Label(master, textvariable=label_1_text, font=sty.font['header2'], bg=sty.bg['header2'])
        field_1 = st.ScrolledText(master, width=25, height=10, font=self.settings.get('font'))
        field_1.config(tabs=self.tab_width)

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

        important_urgent = st.ScrolledText(master, bg=sty.bg['iu'], font=self.settings.get('font'), width=50, height=20)
        important_urgent.config(tabs=self.tab_width)
        important_not_urgent = st.ScrolledText(master, bg=sty.bg['inu'], font=self.settings.get('font'), width=50, height=20)
        important_not_urgent.config(tabs=self.tab_width)
        not_important_urgent = st.ScrolledText(master, bg=sty.bg['niu'], font=self.settings.get('font'), width=50, height=20)
        not_important_urgent.config(tabs=self.tab_width)
        not_important_not_urgent = st.ScrolledText(master, bg=sty.bg['ninu'], font=self.settings.get('font'), width=50, height=20)
        not_important_not_urgent.config(tabs=self.tab_width)

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
        field_0 = st.ScrolledText(master, width=25, height=10, font=self.settings.get('font'))
        field_0.config(tabs=self.tab_width)
        label_1 = tk.Label(master, textvariable=label_1_text, font=sty.font['header2'], bg=sty.bg['header2'])
        field_1 = st.ScrolledText(master, width=25, font=self.settings.get('font'))
        field_1.config(tabs=self.tab_width)

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
        open_instances.remove(self)

    def focus(self):
        self.root.focus_force()

    def new(self):
        """Open new Eisenhower instance."""
        main()
    
    def open(self, file_location=""):
        # Browse for file
        if file_location == "":
            file_location = fd.askopenfilename(
                initialdir = "", 
                title="Select an Eisenhower Matrix File", 
                filetypes = [('Eisenhower Files', '*.ei*')]
            )
        if file_location == None:
            return
        
        # Do not open multiple instances with same location
        overwrite = False
        for eis in open_instances:
            if eis.file_location == file_location:
                # Same instance, check to see if we want to overwrite unsaved changes
                if eis == self:
                    if self.saved:
                        # Nothing to do
                        return
                    else:
                        overwrite = mb.askokcancel("Discard changes?", "Re-open file and lose unsaved changes?")
                        if not overwrite:
                            return
                # Different instance: do not open multiple instances with same location
                else:
                    eis.focus()
                    return
        
        # Do not overwrite current matrix. Open a new instance if there are unsaved changes.
        if not overwrite and self.file_location != "" and self.file_location != file_location:
            main(file_location=file_location)
        self.file_location = file_location

        # JSON parses file
        with open(file_location, "r") as file:
            data = json.load(file)
        
        # Validate results
        if not 'type' in data or data['type'] != 'Eisenhower':
            raise Exception('File not in appropriate format!')

        # Update settings
        self.settings = Settings(data['settings'])
        self.settings_repaint()

        # Update text boxes
        for i in range(0, 4):
            text = self.notes_text[i]
            text.delete(1.0, tk.END)
            text.insert(tk.END, data['notes_' + str(i+1)])
            matrix = self.matrix[i]
            matrix.delete(1.0, tk.END)
            matrix.insert(tk.END, data['matrix_' + str(i+1)])
        
        self.saved = True

    def save(self):
        # Open dialog if not yet saved
        if self.file_location == "":
            self.saveas()
        
        # Convert to JSON
        data = {
            "type": "Eisenhower",
            "name": self.title,
            "settings": {
                "font_size": self.settings.get('font_size'),
                "notes_1": self.settings.get('notes_1'),
                "notes_2": self.settings.get('notes_2'),
                "notes_3": self.settings.get('notes_3'),
                "notes_4": self.settings.get('notes_4')
            },
            "notes_1": self.notes_text[0].get(1.0, tk.END+"-1c"),
            "notes_2": self.notes_text[1].get(1.0, tk.END+"-1c"),
            "notes_3": self.notes_text[2].get(1.0, tk.END+"-1c"),
            "notes_4": self.notes_text[3].get(1.0, tk.END+"-1c"),
            "matrix_1": self.matrix[0].get(1.0, tk.END+"-1c"),
            "matrix_2": self.matrix[1].get(1.0, tk.END+"-1c"),
            "matrix_3": self.matrix[2].get(1.0, tk.END+"-1c"),
            "matrix_4": self.matrix[3].get(1.0, tk.END+"-1c")
        }

        # Save to file
        with open(self.file_location, 'w') as file:
            json.dump(data, file)

    def saveas(self):
        file_location = fd.asksaveasfilename(
            initialdir = "", 
            title="Save Eisenhower Matrix as...", 
            filetypes = [('Eisenhower Files', '*.ei*')],
            defaultextension="ei"
        )
        if file_location is not None:
            self.file_location = file_location
            self.save()
        
    def settings_open(self):
        if self.settings_window is None or self.settings_window.is_closed():
            self.settings_window = SettingsWindow(self, self.settings)
        else:
            self.settings_window.focus()
    
    def settings_close(self):
        if self.settings_window != None and hasattr(self.settings_window, "destroy") and callable(getattr(self.settings_window, "destroy")):
            self.settings_window.destroy()
        self.settings_window = None

    def settings_repaint(self):
        """Update window with new settings."""
        for i in range(0, 4):
            self.notes_label[i].set(self.settings.get('notes_' + str(i+1)))
            #self.notes_label[i].update()
        for set in (self.notes_text, self.matrix):
            for text in set:
                # Change font size only. Assume font is tuple of family and size.
                text.configure(font=self.settings.get('font'))
                text.update()

    def settings_set(self, settings: Settings):
        # Only save valid settings. Ignore bad setting keys.
        if isinstance(settings, Settings):
            self.settings = settings
        
        self.settings_repaint()

def main(file_location=""): 
    """Open new Eisenhower instance."""
    if len(sys.argv) > 1:
        file_location = sys.argv[1]

    root = tk.Tk()
    Eisenhower(root, file_location=file_location)
    root.mainloop()

if __name__ == '__main__':
    main()