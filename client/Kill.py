import tkinter as tk
from tkinter import messagebox
from Program import Program

class Kill(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Kill")
        self.geometry("284x45")

        self.txtID = tk.Entry(self)
        self.txtID.place(x=13, y=13, width=183, height=20)
        self.txtID.insert(tk.END, "Nhập ID")

        self.butNhap = tk.Button(self, text="Kill", command=self.kill_process)
        self.butNhap.place(x=202, y=13, width=75, height=23)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def kill_process(self):
        Program.nw.write("KILLID\n")
        Program.nw.flush()
        cmd = Program.nr.readline().strip()
        if (cmd == "ok"):
            Program.nw.write(self.txtID.get() + "\n")
            Program.nw.flush()
        else:
            return;
        
    def on_close(self):
        Program.nw.write("QUIT\n")
        Program.nw.flush()
        self.destroy()