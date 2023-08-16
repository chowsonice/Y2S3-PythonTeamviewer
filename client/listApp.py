import tkinter as tk
import socket
from tkinter import messagebox

class ListAppForm(tk.Tk):
    def __init__(self, server_address, server_port):
        super().__init__()

        self.title("List Applications")
        self.geometry("400x300")

        self.button_kill = tk.Button(self, text="Kill", command=self.open_kill_form)
        self.button_kill.pack()

        self.button_view = tk.Button(self, text="View", command=self.send_view)
        self.button_view.pack()

        self.button_start = tk.Button(self, text="Start", command=self.open_start_form)
        self.button_start.pack()

        self.button_clear = tk.Button(self, text="Clear", command=self.clear_list)
        self.button_clear.pack()

        self.list_view = tk.Listbox(self)
        self.list_view.pack()

        self.protocol("WM_DELETE_WINDOW", self.send_quit)

        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_address, self.server_port))

    def send_message(self, message):
        self.socket.sendall(message.encode())

    def receive_message(self):
        return self.socket.recv(1024).decode()

    def open_kill_form(self):
        self.send_message("KILL")
        kill_form = KillForm(self)
        kill_form.mainloop()

    def send_view(self):
        self.send_message("XEM")
        response = self.receive_message()
        process_count = int(response)

        self.list_view.delete(0, tk.END)
        for _ in range(process_count):
            response = self.receive_message()
            if response == "ok":
                name = self.receive_message()
                process_id = self.receive_message()
                count = self.receive_message()
                item = f"Name: {name}, ID: {process_id}, Count: {count}"
                self.list_view.insert(tk.END, item)

    def open_start_form(self):
        self.send_message("START")
        start_form = StartForm(self)
        start_form.mainloop()

    def send_quit(self):
        self.send_message("QUIT")
        self.socket.close()
        self.destroy()

    def clear_list(self):
        self.list_view.delete(0, tk.END)

class KillForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Kill Process")
        self.geometry("300x200")

        self.label_id = tk.Label(self, text="Enter Process ID:")
        self.label_id.pack()

        self.entry_id = tk.Entry(self)
        self.entry_id.pack()

        self.button_kill = tk.Button(self, text="Kill", command=self.send_kill)
        self.button_kill.pack()

    def send_kill(self):
        process_id = self.entry_id.get()
        self.master.send_message("KILLID")
        self.master.send_message(process_id)
        response = self.master.receive_message()
        messagebox.showinfo("Result", response)

class StartForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Start Process")
        self.geometry("300x200")

        self.label_name = tk.Label(self, text="Enter Process Name:")
        self.label_name.pack()

        self.entry_name = tk.Entry(self)
        self.entry_name.pack()

        self.button_start = tk.Button(self, text="Start", command=self.send_start)
        self.button_start.pack()

    def send_start(self):
        process_name = self.entry_name.get()
        self.master.send_message("STARTAPP")
        self.master.send_message(process_name)
        response = self.master.receive_message()
        messagebox.showinfo("Result", response)

if __name__ == "__main__":
    server_address = '127.0.0.1'  # Replace with your server address
    server_port = 1234  # Replace with your server port

    app = ListAppForm(server_address, server_port)
    app.mainloop()