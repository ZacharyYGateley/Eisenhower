import json
from Settings import *
import Styles as sty
import sys
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import scrolledtext as st

open_instances = []

class Eisenhower:
    """Master Eisenhower Matrix."""
    def __init__(self, root, file_location=""):
        self.root = root
        self.window = tk.Toplevel()
        self.window.iconbitmap('images/feather.ico')
        self.settings_window = None
        # Volatile matrix settings
        self.settings = Settings()
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

        # File menu
        self.build_menu()

        # Title and status bar
        self.title = self.settings.get('title')
        self.window.title(self.title)
        self.titlevar = tk.StringVar()
        self.titlevar.set(self.title)
        title = tk.Label(self.window, textvariable=self.titlevar)
        title.config(font=sty.font['header1'])
        title.grid(row=0, column=1)

        self.status_variable = tk.StringVar()
        self.status_timeout = None
        status = tk.Label(self.window, textvar=self.status_variable, fg="red")
        status.grid(row=0, column=0, sticky="W")

        # 1x3 column grid
        # Column 1: Embedded 2x1 grid
        # Column 2: Embedded 3x3 grid
        # Column 3: Embedded 2x1 grid
        left = tk.Frame(self.window)
        left.grid(column=0, row=1, sticky="NSEW")
        center = tk.Frame(self.window, padx=10)
        center.grid(column=1, row=1, sticky="NSEW")
        right = tk.Frame(self.window)
        right.grid(column=2, row=1, sticky="NSEW")

        # Configure grid
        # Title row does not expand
        self.window.rowconfigure(index=1, weight=1)
        # Only matrix column expands
        self.window.columnconfigure(index=1, weight=1)

        (label_0, field_0, label_1, field_1) = self.build_notes(left, True)
        self.matrix = self.build_center(center)
        (label_2, field_2, label_3, field_3) = self.build_notes(right, False)

        self.notes_label = [label_0, label_1, label_2, label_3]
        self.notes_text = [field_0, field_1, field_2, field_3]

        # Attempt to open file
        if self.file_location != "":
            self.open(file_location=self.file_location)
        
        # Keep track of all open instances
        open_instances.append(self)

        # Make sure self.window is erased on window destroy
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # Bind CTRL+S
        def key_press(event):
            key = event.char
            if len(key) > 0 and ord(key) == 19:
                self.save()
            else:
                self.status_unsaved()
        self.window.bind('<KeyPress>', key_press)

        self.settings_repaint()

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

        (frame_11, important_urgent) = self.build_scrolledtext(master, bg=sty.bg['iu'], width=50, height=20)
        (frame_12, important_not_urgent) = self.build_scrolledtext(master, bg=sty.bg['inu'], width=50, height=20)
        (frame_21, not_important_urgent) = self.build_scrolledtext(master, bg=sty.bg['niu'], width=50, height=20)
        (frame_22, not_important_not_urgent) = self.build_scrolledtext(master, bg=sty.bg['ninu'], width=50, height=20)

        frame_11.grid(row=1, column=1, sticky="NSEW")
        frame_12.grid(row=1, column=2, sticky="NSEW")
        frame_21.grid(row=2, column=1, sticky="NSEW")
        frame_22.grid(row=2, column=2, sticky="NSEW")

        # Expand text boxes only
        master.columnconfigure(index=1, weight=1, uniform="column")
        master.columnconfigure(index=2, weight=1, uniform="column")
        master.rowconfigure(index=1, weight=1, uniform="row")
        master.rowconfigure(index=2, weight=1, uniform="row")

        return (important_urgent, important_not_urgent, not_important_urgent, not_important_not_urgent)

    def build_menu(self):
        """Build tkinter menu of main window. Used only during __init__."""
        menubar = tk.Menu(self.window) 
  
        # Adding File Menu and commands 
        file = tk.Menu(menubar, tearoff = 0) 
        menubar.add_cascade(label = 'File', menu = file) 
        file.add_command(label = 'New Matrix', command = self.new)
        file.add_command(label = 'Open Matrix', command = self.open)
        file.add_command(label = 'Save', command = self.save)
        file.add_command(label = 'Save As', command = self.saveas)
        file.add_separator() 
        file.add_command(label = 'Close', command = self.close)

        edit = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = 'Edit', menu=edit)
        edit.add_command(label = 'Matrix Settings', command = self.settings_open)

        self.window.config(menu = menubar) 

    def build_notes(self, master, top_grow):
        """Build tkinter left column of main window. Used only during __init__."""

        # Titles as string variables
        label_0_text = tk.StringVar()
        label_1_text = tk.StringVar()

        # Build widgets
        label_0 = tk.Label(master, textvariable=label_0_text, font=sty.font['header2'], bg=sty.bg['header2'])
        (frame_0, field_0) = self.build_scrolledtext(master, width=25, font=self.settings.get('font'))
        label_1 = tk.Label(master, textvariable=label_1_text, font=sty.font['header2'], bg=sty.bg['header2'])
        (frame_1, field_1) = self.build_scrolledtext(master, width=25, font=self.settings.get('font'))

        # Configure
        #field_0.config(tabs=self.tab_width)
        #field_1.config(tabs=self.tab_width)

        # Add to window
        label_0.grid(row=0, column=0, sticky="EW")
        frame_0.grid(row=1, column=0, sticky="NSEW")
        label_1.grid(row=2, column=0, sticky="EW")
        frame_1.grid(row=3, column=0, sticky="NSEW")
        
        # Allow bottom text box to grow/shrink
        if top_grow:
            master.rowconfigure(index=1, weight=1)
            field_1.configure(height=10)
        else:
            master.rowconfigure(index=3, weight=1)
            field_0.configure(height=10)
        
        return (label_0_text, field_0, label_1_text, field_1)
    
    def build_scrolledtext(self, master, **kwargs):
        frame = tk.Frame(master)
        field = tk.Text(frame, kwargs, wrap="none")
        field_v = tk.Scrollbar(frame, orient="vertical", command=field.yview)
        field_h = tk.Scrollbar(frame, orient="horizontal", command=field.xview)
        field.grid(row=0, column=0, sticky="NSEW")
        field_v.grid(row=0, column=1, sticky="NS")
        field_h.grid(row=1, column=0, sticky="EW")
        field.configure(yscrollcommand=field_v.set, xscrollcommand=field_h.set)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        return (frame, field)

    def close(self):
        self.settings_close()
        self.window.destroy()
        open_instances.remove(self)

        if len(open_instances) == 0:
            self.root.destroy()

    def focus(self):
        self.window.focus_force()

    def new(self):
        """Open new Eisenhower instance."""
        main(self.root)
    
    def open(self, file_location=""):
        # Browse for file
        if file_location == "":
            file_location = fd.askopenfilename(
                initialdir = "", 
                title="Select an Eisenhower Matrix File", 
                filetypes = [('Eisenhower Files', '*.ei*')]
            )
        if file_location == None or file_location == "":
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
        if (not overwrite and self.file_location != "" and self.file_location != file_location) or (not self.saved and self.file_location == ""):
            main(self.root, file_location=file_location)
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
        
        self.status_saved()

    def save(self):
        # Open dialog if not yet saved
        if self.file_location == "":
            self.saveas()
        
        # Convert to JSON
        data = {
            "type": "Eisenhower",
            "name": self.title,
            "settings": self.settings.export(),
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
        
        self.status_saved()

    def saveas(self):
        file_location = fd.asksaveasfilename(
            initialdir = "", 
            title="Save Eisenhower Matrix as...", 
            filetypes = [('Eisenhower Files', '*.ei*')],
            defaultextension="ei"
        )
        if file_location is not None and file_location != "":
            self.file_location = file_location
            self.save()
        
    def settings_open(self):
        if self.settings_window is None or self.settings_window.is_closed():
            self.settings_window = SettingsWindow(self, self.settings)
        else:
            self.settings_window.focus()
    
    def settings_close(self):
        self.settings_window = None

    def settings_repaint(self):
        """Update window with new settings."""
        self.titlevar.set(self.settings.get('title'))
        # Loop Label titles
        for i in range(0, 4):
            self.notes_label[i].set(self.settings.get('notes_' + str(i+1)))
        
        f = self.settings.get('font')
        t = self.settings.get('tab_width')
        # Notes
        for i in range(0, 4):
            text = self.notes_text[i]
            text.configure(font=f, tabs=t, background=self.settings.get('bgn_' + str(i+1)), foreground=self.settings.get('fgn_' + str(i+1)))
            text.update()
        # Matrix
        for i in range(0, 4):
            text = self.matrix[i]
            text.configure(font=f, tabs=t, background=self.settings.get('bgm_' + str(i+1)), foreground=self.settings.get('fgm_' + str(i+1)))
            text.update()

    def settings_set(self, settings: Settings):
        # Only save valid settings. Ignore bad setting keys.
        if isinstance(settings, Settings):
            self.settings = settings
        
        self.settings_repaint()

    def status_unsaved(self):
        self.saved = False
        self.status_variable.set("CHANGES NOT SAVED")
    
    def status_saved(self):
        self.saved = True
        self.status_variable.set("")

def main(root, file_location=""): 
    """Open new Eisenhower instance."""
    if len(sys.argv) > 1:
        file_location = sys.argv[1]

    Eisenhower(root, file_location=file_location)

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    main(root)
    root.mainloop()