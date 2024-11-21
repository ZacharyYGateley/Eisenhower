import tkinter as tk
from Styles import *

class Settings:
    def __init__(self, parent):
        self.parent = parent

        root = tk.Tk()
        self.root = root

        root.title(parent.title)
        title = tk.Label(root, text='Matrix Settings')
        title.config(font=font['header3'])
        title.pack(expand=True)

        center = tk.Frame(root)

        # Numerical entry only
        dcmd = (root.register(self.numeric_callback))
        
        label_fs = tk.Label(center, text='Font Size').grid(row=0, column=0, sticky="E")
        label_1 = tk.Label(center, text='Custom Notes 1').grid(row=1, column=0, sticky="E")
        label_2 = tk.Label(center, text='Custom Notes 2').grid(row=2, column=0, sticky="E")
        label_3 = tk.Label(center, text='Custom Notes 3').grid(row=3, column=0, sticky="E")
        label_4 = tk.Label(center, text='Custom Notes 4').grid(row=4, column=0, sticky="E")
        
        entryfs = tk.Entry(center, validate='all', validatecommand=(dcmd, '%P'), width=3).grid(row=0, column=1, sticky="W")
        entry1 = tk.Entry(center).grid(row=1, column=1, sticky="W")
        entry2 = tk.Entry(center).grid(row=2, column=1, sticky="W")
        entry3 = tk.Entry(center).grid(row=3, column=1, sticky="W")
        entry4 = tk.Entry(center).grid(row=4, column=1, sticky="W")

        center.pack(fill="both", expand=True, padx=10, pady=10)

        submit = tk.Frame(root, bg="red")
        tk.Button(submit, text="Update").grid(row=0, column=0)
        tk.Button(submit, text="Cancel", command=self.root.destroy).grid(row=0, column=1)
        submit.pack(padx=20, pady=10)

        root.mainloop()

    def numeric_callback(self, entry):
        if str.isdigit(entry) or entry == "":
            return True
        else:
            return False

    def load(self):
        pass

    def save(self):
        pass
