import sys
import os
import socket
import tkinter as tk
from io import BytesIO
from PIL import Image
from tkinter import filedialog
from Program import Program

class Pic(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pic")
        self.butTake = tk.Button(self, text="Take", command=self.lam)
        self.butTake.pack()
        self.button1 = tk.Button(self, text="Save", command=self.save_image)
        self.button1.pack()
        self.protocol("WM_DELETE_WINDOW", self.pic_closing)

    def lam(self):
        s = "TAKE"
        Program.nw.write(s + '\n')
        Program.nw.flush()
        s = Program.nr.readline().strip()
        data = bytearray(int(s))
        rec = Program.client.recv_into(data)
        ms = BytesIO(data)
        self.picture = Image.open(ms)
        self.picture.show()

    def save_image(self):
        save_file = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=(("Bmp files", "*.Bmp"), ("All files", "*.*"))
        )
        if save_file:
            self.picture.save(save_file, "PNG")

    def pic_closing(self):
        s = "QUIT"
        Program.nw.write(s+'\n')
        Program.nw.flush()
        self.destroy()
