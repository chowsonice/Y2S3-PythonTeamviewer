import tkinter as tk
from tkinter import messagebox
from Program import Program

class Start(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Start")
        self.create_widgets()

    def create_widgets(self):
        self.txtID = tk.Entry(self)
        self.txtID.pack()

        button = tk.Button(self, text="Start", command=self.start_button_click)
        button.pack()

        self.protocol("WM_DELETE_WINDOW", self.window_closing)

    def start_button_click(self):
        Program.nw.write("STARTID\n")
        Program.nw.flush()
        Program.nw.write(self.txtID.get() + "\n")
        Program.nw.flush()
        s = Program.nr.readline()
        messagebox.showinfo("Response", s)

    def window_closing(self):
        Program.nw.write("QUIT\n")
        Program.nw.flush()
        self.destroy()


