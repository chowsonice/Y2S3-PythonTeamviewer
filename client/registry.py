import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from Program import Program
import os


class Registry(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registry")
        self.create_widgets()

    def create_widgets(self):
        self.opApp = tk.OptionMenu(self, tk.StringVar(), "Get value", "Set value", "Delete value", "Create key", "Delete key")
        self.opApp.pack()

        self.txtLink = tk.Entry(self)
        self.txtLink.pack()

        self.txtNameValue = tk.Entry(self)
        self.txtNameValue.pack()

        self.txtValue = tk.Entry(self)
        self.txtValue.pack()

        self.opTypeValue = tk.OptionMenu(self, tk.StringVar(), "String", "DWORD", "QWORD", "Binary", "ExpandString", "MultiString")
        self.opTypeValue.pack()

        button1 = tk.Button(self, text="Send", command=self.send_button_click)
        button1.pack()

        button2 = tk.Button(self, text="Browse", command=self.browse_button_click)
        button2.pack()

        button3 = tk.Button(self, text="Clear", command=self.clear_button_click)
        button3.pack()

        self.protocol("WM_DELETE_WINDOW", self.window_closing)

    def send_button_click(self):
        Program.nw.write("SEND\n")
        Program.nw.flush()
        Program.nw.write(self.opApp.cget("text") + "\n")
        Program.nw.flush()
        Program.nw.write(self.txtLink.get() + "\n")
        Program.nw.flush()
        Program.nw.write(self.txtNameValue.get() + "\n")
        Program.nw.flush()
        Program.nw.write(self.txtValue.get() + "\n")
        Program.nw.flush()
        Program.nw.write(self.opTypeValue.cget("text") + "\n")
        Program.nw.flush()
        s = Program.nr.readline()
        self.txtKQ.insert(tk.END, s + "\n")

    def browse_button_click(self):
        file_path = askopenfilename(filetypes=[("Registry Files", "*.reg")])
        if file_path:
            self.txtLink.delete(0, tk.END)
            self.txtLink.insert(tk.END, file_path)
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.txtNameValue.delete(0, tk.END)
                    self.txtNameValue.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def clear_button_click(self):
        self.txtKQ.delete("1.0", tk.END)

    def window_closing(self):
        Program.nw.write("QUIT\n")
        Program.nw.flush()
        self.destroy()


if __name__ == '__main__':
    Program.nw = None
    Program.nr = None

    app = Registry()
    app.mainloop()