import tkinter as tk
from tkinter import messagebox
from Program import Program

class Start(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Start")
        self.geometry("284x51")

        self.txtID = tk.Entry(self)
        self.txtID.place(x=25, y=13, width=155, height=20)
        self.txtID.insert(tk.END, "Nhập tên")

        self.butStart = tk.Button(self, text="Start", command=self.start_application)
        self.butStart.place(x=197, y=10, width=75, height=23)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_application(self):
        Program.nw.write("TENPROCESS\n")
        Program.nw.flush()
        Program.nw.write(self.txtID.get() + "\n")
        Program.nw.flush()

    def on_close(self):
        Program.nw.write("QUIT\n")
        Program.nw.flush()
        self.destroy()