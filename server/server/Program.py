import socket
import sys
from threading import Thread
from tkinter import *
from tkinter import messagebox

class Program:
    server = None
    client = None
    ns = None
    nr = None
    nw = None