import sys
import socket
import tkinter as tk
from tkinter import messagebox

class ClientApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.client = None
        self.ns = None
        self.nr = None
        self.nw = None
        
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
        
    def openApp(self):
        if self.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "APPLICATION"
        self.nw.write(s + "\n")
        self.nw.flush()
        
        # Additional code to show the application list dialog
        
    def connectServer(self):
        try:
            server_ip = self.txtIP.get()
            server_port = 5656
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((server_ip, server_port))
            messagebox.showinfo("Success", "Connected to the server")
            
            self.ns = self.client.makefile("rwb")
            self.nr = self.ns.makefile("r")
            self.nw = self.ns.makefile("w")
        except Exception as ex:
            messagebox.showinfo("Error", "Failed to connect to the server")
            self.client = None
        
    def shutdown(self):
        if self.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "SHUTDOWN"
        self.nw.write(s + "\n")
        self.nw.flush()
        self.client.close()
        self.client = None
        
    def openRegistry(self):
        if self.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "REGISTRY"
        self.nw.write(s + "\n")
        self.nw.flush()
        
        # Additional code to show the registry dialog
        
    def exitApp(self):
        s = "QUIT"
        if self.client is not None:
            self.nw.write(s + "\n")
            self.nw.flush()
        self.destroy()
        
    def takePicture(self):
        if self.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "TAKEPIC"
        self.nw.write(s + "\n")
        self.nw.flush()
        
        # Additional code to capture and display the picture
        
    def keyLogger(self):
        if self.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "KEYLOG"
        self.nw.write(s + "\n")
        self.nw.flush()
        
        # Additional code to start the keylogger
        
    def closeApp(self):
        s = "QUIT"
        if self.client is not None:
            self.nw.write(s + "\n")
            self.nw.flush()
        self.destroy()
        
    def openProcess(self):
        if self.client is None:
            messagebox.showinfo("Error", "Not connected to the server")
            return
        
        s = "PROCESS"
        self.nw.write(s + "\n")
        self.nw.flush()
        
        # Additional code to show the process list dialog

if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()