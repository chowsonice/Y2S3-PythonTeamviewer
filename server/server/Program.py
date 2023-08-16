import sys
import socket
import io
from threading import Thread
import tkinter as tk
from tkinter import messagebox

class Program:
    server = None
    client = None
    ns = None
    nr = None
    nw = None
