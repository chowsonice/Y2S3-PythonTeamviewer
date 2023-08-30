import tkinter as tk
from tkinter import messagebox
from Program import Program
from Start import Start
from Kill import Kill

class ListProcess(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("List Process")
        self.geometry("320x277")

        self.button_kill = tk.Button(self, text="KILL", command=self.kill_process)
        self.button_kill.place(x=24, y=12, width=66, height=47)

        self.button_view = tk.Button(self, text="XEM", command=self.view_processes)
        self.button_view.place(x=96, y=12, width=59, height=47)

        self.button_start = tk.Button(self, text="START", command=self.start_process)
        self.button_start.place(x=231, y=12, width=59, height=47)

        self.list_view = tk.Listbox(self)
        self.list_view.place(x=24, y=74, width=266, height=162)
        self.list_view.insert(tk.END, "Name Process\tID Process\tCount Thread")

        self.button_clear = tk.Button(self, text="XÓA", command=self.clear_list)
        self.button_clear.place(x=161, y=12, width=64, height=47)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def kill_process(self):
        temp = "KILL"
        Program.nw.write(temp + "\n")
        Program.nw.flush()
        view_kill = Kill(self)
        view_kill.grab_set()

    def view_processes(self):
        temp = "XEM"
        Program.nw.write(temp + "\n")
        Program.nw.flush()
        s1 = "Name process"
        s2 = "ID"
        s3 = "Count"
        cmd = Program.nr.readline().strip()
        if (cmd != "SOPROCESS"):
            Program.nw.write("no\n")
            Program.nw.flush()
            return;
        else:
            Program.nw.write("ok\n")
            Program.nw.flush()
        temp = Program.nr.readline().strip()
        print("So process " + temp)
        soprocess = int(temp)
        for _ in range(soprocess):
            s1 = Program.nr.readline().strip()
            s2 = Program.nr.readline().strip()
            s3 = Program.nr.readline().strip()
            one = [s1, s2, s3]
            print(one)
            self.list_view.insert(tk.END, one)

    def start_process(self):
        temp = "START"
        Program.nw.write(temp + "\n")
        Program.nw.flush()
        view_start = Start(self)
        view_start.grab_set()

    def on_close(self):
        s = "QUIT"
        Program.nw.write(s + "\n")
        Program.nw.flush()
        self.destroy()

    def clear_list(self):
        self.list_view.delete(0, tk.END)