import tkinter as tk
from Settings import Settings
from Styles import *

class Eisenhower:
    def __init__(self, root):
        self.root = root
        
        # 1x3 column grid
        # Column 1: Embedded 2x1 grid
        # Column 2: Embedded 3x3 grid
        # Column 3: Embedded 2x1 grid

        self.title = 'Eisenhower To-Do Matrix'

        root.title(self.title)
        title = tk.Label(root, text=self.title)
        title.config(font=font['header1'])
        title.grid(row=0, column=0, columnspan=3)

        self.build_menu()

        left = tk.Frame(root, width=200)
        left.grid(column=0, row=1)
        center = tk.Frame(root)
        center.grid(column=1, row=1)
        right = tk.Frame(root)
        right.grid(column=2, row=1)

        # Title row does not expand
        root.rowconfigure(index=1, weight=1)
        # Only matrix column expands
        root.columnconfigure(index=1, weight=1)

        self.build_left(left)
        self.build_center(center)
        self.build_right(right)
    
    def build_menu(self):
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
        edit.add_command(label = 'Matrix Settings', command = self.settings)

        self.root.config(menu = menubar) 

    def build_left(self, master):
        label_0_0 = tk.Label(master, text='Notes 1', font=font['header2'])
        field_0_0 = tk.Text(master, width=20)
        label_1_0 = tk.Label(master, text='Notes 2', font=font['header2'])
        field_1_0 = tk.Text(master, width=20)

        label_0_0.grid(row=0, column=0)
        field_0_0.grid(row=1, column=0)
        label_1_0.grid(row=2, column=0)
        field_1_0.grid(row=3, column=0)
        pass

    def build_center(self, master):
        c10 = tk.Frame(master, bg=bg['i'])
        c20 = tk.Frame(master, bg=bg['ni'])

        urgent = tk.Label(master, text='Urgent', font=font['header2'], bg=bg['u'])
        not_urgent = tk.Label(master, text='Not Urgent', font=font['header2'], bg=bg['nu'])
        i_pos=96
        important = tk.Canvas(c10, width = 24, height = i_pos, bg=bg['i'], highlightthickness=0)
        important.create_text(12, i_pos, text = 'Important', angle = 90, anchor = 'w', font=font['header2'])
        important.pack(expand=True)
        ni_pos=136
        not_important = tk.Canvas(c20, width = 24, height=ni_pos, bg=bg['ni'], highlightthickness=0)
        not_important.create_text(12, ni_pos, text = 'Not Important', angle = 90, anchor = 'w', font=font['header2'])
        not_important.pack(expand=True)
        
        urgent.grid(row=0, column=1, sticky="NSEW")
        not_urgent.grid(row=0, column=2, sticky="NSEW")
        c10.grid(row=1, column=0, sticky="NSEW")
        c20.grid(row=2, column=0, sticky="NSEW")

        urgent_important = tk.Text(master)
        urgent_not_important = tk.Text(master)
        not_urgent_important = tk.Text(master)
        not_urgent_not_important = tk.Text(master)

        urgent_important.grid(row=1, column=1)
        urgent_not_important.grid(row=1, column=2)
        not_urgent_important.grid(row=2, column=1)
        not_urgent_not_important.grid(row=2, column=2)

        pass

    def build_right(self, master):
        label_0_2 = tk.Label(master, text='Notes 3', font=font['header2'])
        field_0_2 = tk.Text(master, width=20)
        label_1_2 = tk.Label(master, text='Notes 4', font=font['header2'])
        field_1_2 = tk.Text(master, width=20)
        label_0_2.grid(row=0, column=0)

        field_0_2.grid(row=1, column=0)
        label_1_2.grid(row=2, column=0)
        field_1_2.grid(row=3, column=0)
        pass

    def close(self): 
        self.root.destroy()
    
    def settings(self):
        self.settings = Settings(self)

def main(): 
    root = tk.Tk()
    app = Eisenhower(root)
    root.mainloop()

if __name__ == '__main__':
    main()