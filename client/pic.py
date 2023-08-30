import sys
import os
import socket
import base64
from io import BytesIO
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from Program import Program


class Pic(tk.Toplevel):
    image = PIL.Image.new("RGB", (1920, 1080))

    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Pic")
        self.picture = tk.Label(self)
        
        self.butTake = tk.Button(self, text="Take", command=self.lam)
        self.butTake.pack()
        self.button1 = tk.Button(self, text="Save", command=self.save_image)
        self.button1.pack()
        self.protocol("WM_DELETE_WINDOW", self.pic_closing)
        self.lam()
        self.picture.pack()


    def lam(self):
        s = "PIC";
        print(s)
        Program.nw.write(s + '\n')
        Program.nw.flush()
        while True:
            data = Program.client.recv(4096).strip()
            # txt = str(data)
            if data:
                # print(str(data))
                if data.startswith(b'SIZE'):
                    tmp = data.decode().split()
                    size = int(tmp[1])

                    print('got size')
                    print(size)

                    Program.nw.write("GOT SIZE\n")
                    Program.nw.flush()

                elif data.startswith(b'BYE BYE'):
                    return
                else:
                    count = 0
                    image_data = BytesIO()
                    image_data.write(data)
                    count += len(data)

                    while (count < size):
                        data = Program.client.recv(4096)
                        # image_data += data
                        image_data.write(data)
                        count += len(data)

                    print(count)

                    print("Got image")
                    image_data.seek(0)

                    Program.nw.write("GOT IMAGE\n")
                    Program.nw.flush()

                    data = Program.client.recv(4096)

                    Pic.image = PIL.Image.open(image_data)
                    photo = PIL.ImageTk.PhotoImage(Pic.image.resize((320, 180)))
                    # self.picture.image = PIL.ImageTk.PhotoImage(image)
                    self.picture.configure(image=photo)
                    self.picture.image = photo
                    break
            else:
                break

    def save_image(self):
        save = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Png files", "*.png"), ("Bmp files", "*.bmp"), ("All files", "*.*")]
        )
        if save:
            file_name, file_extension = os.path.splitext(save)
            file_extension = file_extension[1:].upper()  # Remove the dot from the file extension

            # Save the image
            Pic.image.save(save, file_extension)

    def pic_closing(self):
        s = "QUIT"
        print(s)
        Program.nw.write(s + '\n')
        Program.nw.flush()
        self.destroy()
