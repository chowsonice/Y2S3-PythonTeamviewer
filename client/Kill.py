import tkinter as tk
from tkinter import messagebox
from Program import Program

class Kill(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kill")

        self.txtID = tk.Entry(self)
        self.txtID.pack()

        self.butNhap = tk.Button(self, text="Kill", command=self.kill_process)
        self.butNhap.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def kill_process(self):
        # Program.nw.write("KILLID\n")
        # Program.nw.flush()
        Program.nw.write(self.txtID.get() + "\n")
        Program.nw.flush()
        s = Program.nr.readline().strip()

    def on_close(self):
        Program.nw.write("QUIT\n")
        Program.nw.flush()
        self.destroy()

if __name__ == '__main__':
    kill = Kill()
    kill.mainloop()