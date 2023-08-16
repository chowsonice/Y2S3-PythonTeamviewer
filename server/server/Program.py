import sys
import socket
import io
from threading import Thread
import tkinter as tk
from tkinter import messagebox

class Program(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.server_socket = None
        self.client_socket = None
        self.network_stream = None
        self.reader = None
        self.writer = None

        self.title("Server")
        self.geometry("300x200")

        self.start_button = tk.Button(self, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(self, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_server(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(100)

        print("Server started, waiting for client...")
    
    
        self.client_socket, addr = self.server_socket.accept()
        self.network_stream = self.client_socket.makefile('rw')

        print("Client connected at: ", addr)

        self.reader = self.network_stream.make_reader()
        self.writer = self.network_stream.make_writer()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.receive_data()

    def stop_server(self):
        self.reader.close()
        self.writer.close()
        self.network_stream.close()
        self.client_socket.close()
        self.server_socket.close()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def receive_data(self):
        while True:
            try:
                data = self.reader.readline()
                if not data:
                    break
                # Process received data
                self.handle_data(data)
            except:
                break

    def handle_data(self, data):
        # Process the received data
        pass

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop_server()
            self.destroy()

    if __name__ == "__main__":
        start_server()

