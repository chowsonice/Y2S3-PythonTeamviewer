import tkinter as tk
from tkinter import messagebox
from Program import Program

class Start(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Start")

        self.txtID = tk.Entry(self)
        self.txtID.pack()

        self.butStart = tk.Button(self, text="Start", command=self.start_application)
        self.butStart.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_application(self):
        Program.nw.write(self.txtID.get() + "\n")
        Program.nw.flush()
        s = Program.nr.readline().strip()
        messagebox.showinfo("Message", s)

    def on_close(self):
        Program.nw.write("QUIT\n")
        Program.nw.flush()
        self.destroy()