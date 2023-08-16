import sys
import os
import socket
from io import BytesIO
from PIL import Image
from tkinter import *
from tkinter import filedialog

class PicForm:
    def __init__(self, root):
        self.root = root
        self.initialize_components()

    def initialize_components(self):
        self.root.title("Pic")
        self.butTake = Button(self.root, text="Take", command=self.lam)
        self.butTake.pack()
        self.button1 = Button(self.root, text="Save", command=self.save_image)
        self.button1.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.pic_closing)

    def lam(self):
        s = "TAKE"
        Program.nw.sendall(s.encode())
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
        Program.nw.sendall(s.encode())
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    pic_form = PicForm(root)
    root.mainloop()