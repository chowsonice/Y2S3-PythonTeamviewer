import tkinter as tk
import socket
from tkinter import messagebox

class KillForm(tk.Tk):
    def __init__(self, server_address, server_port):
        super().__init__()

        self.title("Kill")
        self.geometry("300x200")

        self.label_id = tk.Label(self, text="Enter Process ID:")
        self.label_id.pack()

        self.entry_id = tk.Entry(self)
        self.entry_id.pack()

        self.button_kill = tk.Button(self, text="Kill", command=self.send_kill)
        self.button_kill.pack()

        self.protocol("WM_DELETE_WINDOW", self.send_quit)

        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_address, self.server_port))

    def send_message(self, message):
        self.socket.sendall(message.encode())

    def receive_message(self):
        return self.socket.recv(1024).decode()

    def send_kill(self):
        process_id = self.entry_id.get()
        self.send_message("KILLID")
        self.send_message(process_id)
        response = self.receive_message()
        messagebox.showinfo("Result", response)

    def send_quit(self):
        self.send_message("QUIT")
        self.socket.close()
        self.destroy()

if __name__ == "__main__":
    server_address = '127.0.0.1'  # Replace with your server address
    server_port = 1234  # Replace with your server port

    app = KillForm(server_address, server_port)
    app.mainloop()