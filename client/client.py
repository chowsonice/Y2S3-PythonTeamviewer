import sys
import io
import socket
import tkinter as tk
from tkinter import messagebox
from Program import Program

class ClientApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        Program.client = None
        Program.ns = None
        Program.nr = None
        Program.nw = None
        
        self.title("Client")

        self.lblIP = tk.Label(self, text="Server IP:")
        self.lblIP.pack()
        
        self.txtIP = tk.Entry(self)
        self.txtIP.pack()
        
        self.butApp = tk.Button(self, text="APPLICATION", command=self.openApp)
        self.butApp.pack()
        
        self.butConnect = tk.Button(self, text="CONNECT", command=self.connectServer)
        self.butConnect.pack()
        
        self.button1 = tk.Button(self, text="SHUTDOWN", command=self.shutdown)
        self.button1.pack()
        
        self.butReg = tk.Button(self, text="REGISTRY", command=self.openRegistry)
        self.butReg.pack()
        
        self.butExit = tk.Button(self, text="QUIT", command=self.exitApp)
        self.butExit.pack()
        
        self.butPic = tk.Button(self, text="TAKEPIC", command=self.takePicture)
        self.butPic.pack()
        
        self.butKeyLock = tk.Button(self, text="KEYLOG", command=self.keyLogger)
        self.butKeyLock.pack()
        
        self.butProcess = tk.Button(self, text="PROCESS", command=self.openProcess)
        self.butProcess.pack()
        
        self.protocol("WM_DELETE_WINDOW", self.closeApp)
        
    def connectServer(self):
        try:
            server_ip = self.txtIP.get()
            server_port = 5656
            Program.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Program.client.connect((server_ip, server_port))
            messagebox.showinfo("Success", "Connected to the server")
            
            Program.ns = Program.client.makefile("rw")
            Program.nr = io.TextIOWrapper(Program.ns, encoding="utf-8")
            Program.nw = io.TextIOWrapper(Program.ns, encoding="utf-8")
        except Exception as ex:
            messagebox.showinfo("Error", "Failed to connect to the server", ex)
            Program.client = None

    def openApp(self):
        if Program.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "APPLICATION\n"
        Program.nw.write(s.encode("utf-8"))
        Program.nw.flush()
        
        # Additional code to show the application list dialog
             
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
        
        # Additional code to show the registry dialog
        
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
        
        # Additional code to capture and display the picture
        
    def keyLogger(self):
        if Program.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "KEYLOG"
        Program.nw.write(s + "\n")
        Program.nw.flush()
        
        # Additional code to start the keylogger
        
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
        
        # Additional code to show the process list dialog

if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()