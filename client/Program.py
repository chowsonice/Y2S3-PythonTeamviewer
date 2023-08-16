import tkinter as tk
from tkinter import messagebox
import socket
import io

class Program:
    client = None
    ns = None
    nr = None
    nw = None

class Client(tk.Tk):
    def __init__(self, server_address, server_port):
        super().__init__()
        self.title("Client")
        self.server_address = server_address
        self.server_port = server_port
        self.create_widgets()

    def create_widgets(self):
        button = tk.Button(self, text="Send Data", command=self.send_data)
        button.pack()

        self.protocol("WM_DELETE_WINDOW", self.window_closing)

    def send_data(self):
        s = "Hello, Server!"  # Replace with your data to be sent
        data = s.encode("ascii")
        Program.client.send(data)

    def window_closing(self):
        s = "QUIT"  # Replace with your quit command
        data = s.encode("ascii")
        Program.client.send(data)
        self.destroy()

def run_client(server_address, server_port):
    Program.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Program.client.connect((server_address, server_port))

    Program.ns = Program.client.makefile("rb")
    Program.nr = io.TextIOWrapper(Program.ns, encoding="ascii")
    Program.nw = io.TextIOWrapper(Program.ns, encoding="ascii", write_through=True)

    app = Client(server_address, server_port)
    app.mainloop()

    Program.client.close()
    Program.ns.close()
    Program.nr.close()
    Program.nw.close()