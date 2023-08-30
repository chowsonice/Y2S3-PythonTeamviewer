import sys
import io
import socket
import tkinter as tk
from tkinter import messagebox
from Program import Program
from listApp import ListApp
from pic import Pic
from process import ListProcess
from keylog import KeylogForm
from registry import RegistryForm


class ClientApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        Program.client = None
        Program.ns = None
        Program.nr = None
        Program.nw = None

        self.title("Client")
        self.geometry("372x302")

        self.butApp = tk.Button(self, text="App Running", command=self.openApp)
        self.butApp.place(x=93, y=64, width=145, height=63)

        self.butConnect = tk.Button(self, text="Kết nối", command=self.connectServer)
        self.butConnect.place(x=244, y=27, width=100, height=23)

        self.txtIP = tk.Entry(self)
        self.txtIP.place(x=12, y=29, width=226, height=20)
        self.txtIP.insert(tk.END, "Nhập IP")

        self.butTat = tk.Button(self, text="Tắt máy", command=self.shutdown)
        self.butTat.place(x=93, y=133, width=48, height=57)

        self.butReg = tk.Button(self, text="Sửa registry", command=self.openRegistry)
        self.butReg.place(x=93, y=196, width=198, height=65)

        self.butExit = tk.Button(self, text="Thoát", command=self.exitApp)
        self.butExit.place(x=297, y=196, width=47, height=65)

        self.butPic = tk.Button(self, text="Chụp màn hình", command=self.takePicture)
        self.butPic.place(x=147, y=133, width=91, height=57)

        self.butKeyLock = tk.Button(self, text="Keystroke", command=self.keyLogger)
        self.butKeyLock.place(x=244, y=64, width=100, height=126)

        self.butProcess = tk.Button(self, text="Process \nRunning", command=self.openProcess)
        self.butProcess.place(x=12, y=64, width=75, height=197)

        self.protocol("WM_DELETE_WINDOW", self.closeApp)
        self.mainloop()

        
    def connectServer(self):
        try:
            server_ip = self.txtIP.get()
            server_port = 5656
            Program.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Program.client.connect((server_ip, server_port))
            messagebox.showinfo("Success", "Connected to the server")
            
            Program.ns = Program.client.makefile("rwb")
            Program.nr = io.TextIOWrapper(Program.ns, encoding="utf-8")
            Program.nw = io.TextIOWrapper(Program.ns, encoding="utf-8")
        except Exception as ex:
            messagebox.showinfo("Error", f"Failed to connect to the server: {ex}")
            Program.client = None

    def openApp(self):
        if Program.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = 'APPLICATION'
        print(s)
        Program.nw.write(s+'\n')
        Program.nw.flush()
        list_app = ListApp(self)
        list_app.grab_set()

    def shutdown(self):
        if Program.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "SHUTDOWN"
        Program.nw.write(s + "\n")
        Program.nw.flush()

        Program.client.close()
        Program.client = None
        
    def openRegistry(self):
        if Program.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "REGISTRY"
        Program.nw.write(s + "\n")
        Program.nw.flush()
        
        registry = RegistryForm(self)
        registry.grab_set()
        
    def exitApp(self):
        s = "QUIT"
        if Program.client is not None:
            Program.nw.write(s + "\n")
            Program.nw.flush()
        self.destroy()
        
    def takePicture(self):
        if Program.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "TAKEPIC"
        Program.nw.write(s + "\n")
        Program.nw.flush()

        take_pic = Pic(self)
        take_pic.grab_set()
        
        
    def keyLogger(self):
        if Program.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "KEYLOG"
        Program.nw.write(s + "\n")
        Program.nw.flush()

        keylogger = KeylogForm(self)
        keylogger.grab_set()
        
        
    def closeApp(self):
        s = "QUIT"
        if Program.client is not None:
            Program.nw.write(s + "\n")
            Program.nw.flush()
        self.destroy()
        
    def openProcess(self):
        if Program.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "PROCESS"
        Program.nw.write(s + "\n")
        Program.nw.flush()
        list_process = ListProcess(self)
        list_process.grab_set()
        

if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()