import tkinter as tk

class Eisenhower:
    def __init__(self, root):
        self.root = root
        
        # 1x3 column grid
        # Column 1: Embedded 2x1 grid
        # Column 2: Embedded 3x3 grid
        # Column 3: Embedded 2x1 grid

        root.title="Eisenhower To-Do"

        title = tk.Label(root, text="Eisenhower To-Do")
        #title.pack()

        left = tk.Frame(root, width=200)
        left.grid(column=0, row=0)
        center = tk.Frame(root)
        center.grid(column=1, row=0)
        right = tk.Frame(root)
        right.grid(column=2, row=0)

        self.build_left(left)
        self.build_center(center)
        self.build_right(right)
    
    def build_left(self, master):
        label_0_0 = tk.Label(master, text="Notes 1")
        field_0_0 = tk.Text(master, width=20)
        label_1_0 = tk.Label(master, text="Notes 2")
        field_1_0 = tk.Text(master, width=20)

        label_0_0.grid(row=0, column=0)
        field_0_0.grid(row=1, column=0)
        label_1_0.grid(row=2, column=0)
        field_1_0.grid(row=3, column=0)
        pass

    def build_center(self, master):
        urgent = tk.Label(master, text="Urgent")
        not_urgent = tk.Label(master, text="Not Urgent")
        important = tk.Canvas(master, width = 12, height = 50)
        important.create_text(6, 50, text = "Important", angle = 90, anchor = "w")
        not_important = tk.Canvas(master, width = 12, height = 50)
        not_important.create_text(6, 50, text = "Not Important", angle = 90, anchor = "w")
        
        urgent.grid(row=0, column=1)
        not_urgent.grid(row=0, column=2)
        important.grid(row=1, column=0)
        not_important.grid(row=2, column=0)

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
        label_0_2 = tk.Label(master, text="Notes 1")
        field_0_2 = tk.Text(master, width=20)
        label_1_2 = tk.Label(master, text="Notes 2")
        field_1_2 = tk.Text(master, width=20)

        label_0_2.grid(row=0, column=0)
        field_0_2.grid(row=1, column=0)
        label_1_2.grid(row=2, column=0)
        field_1_2.grid(row=3, column=0)
        pass

def main(): 
    root = tk.Tk()
    app = Eisenhower(root)
    root.mainloop()

if __name__ == '__main__':
    main()