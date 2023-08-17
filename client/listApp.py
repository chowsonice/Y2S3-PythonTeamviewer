import tkinter as tk
from tkinter import messagebox
from Program import Program
from Start import Start
from Kill import Kill

class ListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("List App")

        self.button_kill = tk.Button(self, text="KILL", command=self.kill_application)
        self.button_kill.pack()

        self.button_view = tk.Button(self, text="VIEW", command=self.view_applications)
        self.button_view.pack()

        self.button_start = tk.Button(self, text="START", command=self.start_application)
        self.button_start.pack()

        self.button_clear = tk.Button(self, text="CLEAR", command=self.clear_list)
        self.button_clear.pack()

        self.list_view = tk.Listbox(self)
        self.list_view.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def kill_application(self):
        temp = "KILL"
        Program.nw.write(temp + "\n")
        Program.nw.flush()
        view_kill = Kill()
        view_kill.mainloop()

    def view_applications(self):
        temp = "XEM"
        Program.nw.write(temp + "\n")
        Program.nw.flush()
        s1 = "Name application"
        s2 = "ID"
        s3 = "Count"
        temp = Program.nr.readline().strip()
        print(temp)
        soprocess = int(temp)
        for _ in range(soprocess):
            s1 = Program.nr.readline().strip()
            s2 = Program.nr.readline().strip()
            s3 = Program.nr.readline().strip()
            one = [s1, s2, s3]
            print(one)
            self.list_view.insert(tk.END, one)

    def start_application(self):
        temp = "START"
        Program.nw.write(temp + "\n")
        Program.nw.flush()
        view_start = Start()
        view_start.mainloop()

    def on_close(self):
        s = "QUIT"
        Program.nw.write(s + "\n")
        Program.nw.flush()
        self.destroy()

    def clear_list(self):
        list_view.delete(0, tk.END)

if __name__ == '__main__':
    app = ListApp()
    app.mainloop()