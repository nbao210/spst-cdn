import customtkinter as ctk
from PIL import Image, ImageTk
import os
import subprocess
import time
import configparser
import sys
import platform
from assets.Codebox import *
from tkinter import messagebox, filedialog
import shutil
import tempfile

version = sys.version.split("\n")[0] 
bit_arch = platform.architecture()[0]
machine = platform.machine()
system = sys.platform  

tl = ctk.CTk()
tl.geometry("800x400")
tl.title("Chấm điểm tự luận")
tl.minsize(600,300)

tl.grid_rowconfigure(0,1)
tl.grid_rowconfigure(1,3)
tl.grid_rowconfigure(2,6)
