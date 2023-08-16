import sys
import tkinter as tk
from tkinter import messagebox
from Program import Program
class Process(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Process")
        self.create_widgets()

    def create_widgets(self):
        button1 = tk.Button(self, text="Kill", command=self.kill_button_click)
        button1.pack()

        button2 = tk.Button(self, text="XEM", command=self.xem_button_click)
        button2.pack()

        button3 = tk.Button(self, text="Start", command=self.start_button_click)
        button3.pack()

        button4 = tk.Button(self, text="Reset List", command=self.reset_list_button_click)
        button4.pack()

        self.listview = tk.Listbox(self)
        self.listview.pack()

        self.protocol("WM_DELETE_WINDOW", self.window_closing)

    def kill_button_click(self):
        temp = "KILL"
        Program.nw.WriteLine(temp)
        Program.nw.Flush()
        messagebox.showinfo("Kill", temp)
        viewkill = Kill()
        viewkill.mainloop()

    def xem_button_click(self):
        temp = "XEM"
        Program.nw.WriteLine(temp)
        Program.nw.Flush()
        s1 = "name process"
        s2 = "ID"
        s3 = "count"
        temp = Program.nr.ReadLine()
        soprocess = int(temp)
        # reset list?
        for i in range(soprocess):
            s1 = "process"
            s2 = "ID"
            s3 = "count"
            self.listview.insert(tk.END, f"{s1}, {s2}, {s3}")

    def start_button_click(self):
        temp = "START"
        # Program.nw.WriteLine(temp);Program.nw.Flush()
        messagebox.showinfo("Start", temp)
        viewstart = Start()
        viewstart.mainloop()

    def reset_list_button_click(self):
        self.listview.delete(0, tk.END)

    def window_closing(self):
        s = "QUIT"
        # Program.nw.WriteLine(s); Program.nw.Flush()
        self.destroy()


class Kill(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Kill")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Kill Window")
        label.pack()


class Start(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Start")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Start Window")
        label.pack()


if __name__ == '__main__':
    process = Process()
    process.mainloop()