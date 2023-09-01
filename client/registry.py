import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from Program import Program 
from tkinter import ttk

class RegistryForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registry")
        
        self.txtBro = tk.Entry(self, width=40)
        self.txtBro.insert(tk.END, "Đường dẫn ...")
        self.txtBro.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        self.butSend = tk.Button(self, text="Gởi nội dung", command=self.send_content)
        self.butSend.grid(row=1, column=2, padx=5, pady=5)
        
        self.butBro = tk.Button(self, text="Browser...", command=self.browse_file)
        self.butBro.grid(row=0, column=2, padx=5, pady=5)
        
        self.txtReg = tk.Text(self, width=40, height=10)
        self.txtReg.insert(tk.END, "Nội dung")
        self.txtReg.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.groupBox1 = tk.LabelFrame(self, text="Sửa giá trị trực tiếp")
        self.groupBox1.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        
        self.opApp = tk.StringVar()
        self.opApp.set("Chọn chức năng")
        
        self.opAppMenu = ttk.OptionMenu(self.groupBox1, self.opApp, "Chọn chức năng", "Get value", "Set value", "Delete value", "Create key", "Delete key", command=self.app_selection)
        self.opAppMenu.config(width=15)
        self.opAppMenu.grid(row=0, column=0, padx=5, pady=5)
        
        self.txtKQ = tk.Text(self.groupBox1, height=5, width=40)
        self.txtKQ.config(state=tk.DISABLED)
        self.txtKQ.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        self.txtLink = tk.Entry(self.groupBox1, width=40)
        self.txtLink.insert(tk.END, "Đường dẫn")
        self.txtLink.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        self.txtNameValue = tk.Entry(self.groupBox1, width=30)
        self.txtNameValue.insert(tk.END, "Name value")
        self.txtNameValue.grid(row=3, column=0, padx=5, pady=5)

        self.button1 = tk.Button(self.groupBox1, text="Gởi", command=self.send_value)
        self.button1.grid(row=3, column=1, columnspan=1, padx=5, pady=5)
        
        self.txtValue = tk.Entry(self.groupBox1, width=40)
        self.txtValue.insert(tk.END, "Value")
        self.txtValue.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        self.opTypeValue = tk.StringVar()
        self.opTypeValue.set("Kiểu dữ liệu")
        
        self.opTypeValueMenu = ttk.OptionMenu(self.groupBox1, self.opTypeValue, "Kiểu dữ liệu", "String", "Binary", "DWORD", "QWORD", "Multi-String", "Expandable String")
        self.opTypeValueMenu.config(width=15)
        self.opTypeValueMenu.grid(row=4, column=1, padx=5, pady=5)
        
        self.butXoa = tk.Button(self.groupBox1, text="Xóa", command=self.clear_result)
        self.butXoa.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def clear_result(self):
        self.txtKQ.config(state=tk.NORMAL)
        self.txtKQ.delete("1.0", END)
        self.txtKQ.config(state=tk.DISABLED)

    def send_content(self):
        s = "REG"
        Program.nw.write(s + '\n');Program.nw.flush();
        s = self.txtReg.get("1.0","end-1c").strip();
        Program.nw.write(s + '\n');Program.nw.flush();
        s = Program.nr.readline().strip();
        messagebox.showinfo("Thông báo", s);
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Registry Files", "*.reg")])
        self.txtBro.delete(0, tk.END)
        self.txtBro.insert(tk.END, file_path)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-16') as fin:
                content = fin.read()
                print(content)
                self.txtReg.delete('1.0', tk.END)
                self.txtReg.insert(tk.END, content)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy file")
    
    def app_selection(self, event):
        selected_app = self.opApp.get()
        
        if selected_app == "Get value":
            self.txtNameValue.config(state=tk.NORMAL)
            self.txtValue.config(state=tk.DISABLED)
            self.opTypeValueMenu.config(state=tk.DISABLED)
        elif selected_app == "Set value":
            self.txtNameValue.config(state=tk.NORMAL)
            self.txtValue.config(state=tk.NORMAL)
            self.opTypeValueMenu.config(state=tk.NORMAL)
        else:
            self.txtNameValue.config(state=tk.NORMAL)
            self.txtValue.config(state=tk.DISABLED)
            self.opTypeValueMenu.config(state=tk.DISABLED)
    
    def send_value(self):
        s = "SEND"
        Program.nw.write(s + '\n');Program.nw.flush();

        option = self.opApp.get()
        link = self.txtLink.get()
        valueName = self.txtNameValue.get()
        value = self.txtValue.get()
        typeValue = self.opTypeValue.get()

        Program.nw.write(option + '\n');Program.nw.flush();
        Program.nw.write(link + '\n');Program.nw.flush();
        Program.nw.write(valueName + '\n');Program.nw.flush();
        Program.nw.write(value + '\n');Program.nw.flush();
        Program.nw.write(typeValue + '\n');Program.nw.flush();

        s = Program.nr.readline().strip();
        print(s)
        if option == "Get value":
            self.txtValue.config(state=tk.NORMAL)
            self.txtValue.delete(0,tk.END)
            self.txtValue.insert(tk.END, s)
            self.txtValue.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Thông báo", s);
    
    def on_closing(self):
        s = "QUIT"
        Program.nw.write(s + '\n');Program.nw.flush();
        self.destroy()
