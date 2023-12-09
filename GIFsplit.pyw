"""
########################################
#                                      #
#               GIFsplit               #
#                                      #
#   Author  : github.com/Nenotriple    #
#                                      #
########################################

Description:
-------------
This script allows you to convert GIF files into individual PNG frames.

You can use it in three ways:
     1. Drag and Drop: Simply drag and drop your GIF(s) onto the script.
     2. File Dialog: Just double-click the script and it will open a file dialog where you can choose your GIF(s).
     3. Command Line: Example: python GIFsplit.pyw "gif 1.gif" "gif 2.gif" "gif 3.gif"

The script will create a new folder for each GIF, named after the original file, where it will save the PNG frames.

Requirements: pillow
"""

VERSION = "v1.07"
WINDOW_WIDTH = 250
WINDOW_HEIGHT = 130

################################################################################################################################################
################################################################################################################################################
#         #
# Imports #
#         #

import os
import sys
import time
import argparse
import tkinter as tk
from tkinter import filedialog
from tkinter import TclError

##################
#                #
# Install Pillow #
#                #
##################


try:
    from PIL import Image
except ImportError:
    import subprocess, sys
    import threading
    from tkinter import Tk, Label, messagebox

    def download_pillow():
        cmd = ["pythonw", '-m', 'pip', 'install', 'pillow']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in iter(lambda: process.stdout.readline(), b''):
            pillow_label = Label(root, wraplength=450)
            pillow_label.pack(anchor="w")
            pillow_label.config(text=line.rstrip())
        process.stdout.close()
        process.wait()
        done_label = Label(root, text="\nAll done! This window will now close...", wraplength=450)
        done_label.pack(anchor="w")
        root.after(3000, root.destroy)

    root = Tk()
    root.title("Pillow Is Installing...")
    root.geometry('600x200')
    root.resizable(False, False)
    root.withdraw()
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    install_pillow = messagebox.askyesno("Pillow not installed!", "Pillow not found!\npypi.org/project/Pillow\n\nWould you like to install it? ~2.5MB \n\n It's required to process gif images.")
    if install_pillow:
        root.deiconify()
        pillow_label = Label(root, wraplength=450)
        pillow_label.pack(anchor="w")
        pillow_label.config(text="Beginning Pillow install now...\n")
        threading.Thread(target=download_pillow).start()
        root.mainloop()
        from PIL import Image
    else:
        sys.exit()

################################################################################################################################################
################################################################################################################################################
#                  #
# Global variables #
#                  #

stop = False
total_frames = 0
start_time = time.time()

################################################################################################################################################
################################################################################################################################################
#                   #
# Primary Functions #
#                   #

def select_gif():
    root.withdraw()
    gif_paths = sys.argv[1:] if len(sys.argv) > 1 else filedialog.askopenfilenames(filetypes=[("GIF files", "*.gif")])
    if not gif_paths:
        sys.exit()
    root.deiconify()
    return gif_paths

def convert_gif_to_png(gif_path, label, current_gif, total_gifs, stop_button):
    global stop, total_frames
    filename = os.path.splitext(os.path.basename(gif_path))[0]
    try:
        if not gif_path.lower().endswith('.gif'):
            raise IOError("\n Invalid file format. Please use a GIF image.")
        with Image.open(gif_path) as img:
            for i in range(img.n_frames):
                if stop: break
                output_folder = os.path.join(os.path.dirname(gif_path), filename)
                os.makedirs(output_folder, exist_ok=True)
                img.save(f'{output_folder}/frame_{i}.png')
                total_frames += 1
                print(f'Processing GIF {current_gif} of {total_gifs}: Frame {i+1} of {img.n_frames} (Total Frames Split: {total_frames})', end='\r')
                if label is not None:
                    label.config(text=f'GIF {current_gif} of {total_gifs} \n\n Frame: {i+1} of {img.n_frames}\nTotal Frames Split: {total_frames}')
                    label.update()
                if current_gif == total_gifs and i == img.n_frames - 1:
                    print(f"Done! - Total GIFs processed: {total_gifs} (Total Frames Split: {total_frames})")
                    if label is not None:
                        label.config(text=f"Done! - Total GIFs processed: {total_gifs} \n\n Total Frames Split: {total_frames}")
                        stop_button.config(text="Close Window")
                    stop = True
                    if label is not None:
                        label.update()
            print()
    except IOError as e:
        file_name = os.path.basename(gif_path)
        file_type = os.path.splitext(file_name)[1]
        print(f"Error opening file type: {file_type} \n {str(e)}")
        if label is not None:
            display_error(f"Error opening file type: {file_type} \n {str(e)}")

def process_all_gifs(gif_paths, label, stop_button):
    total_gifs = len(gif_paths)
    for i, gif_path in enumerate(gif_paths, start=1):
        if stop: break
        convert_gif_to_png(gif_path, label, i, total_gifs, stop_button)

################################################################################################################################################
################################################################################################################################################
#                     #
# Secondary Functions #
#                     #

def update_timer(label, stop_button):
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    if not stop and stop_button.cget("text") != "Close Window":
        label.config(text="Time elapsed: {:0>2}:{:05.2f}".format(int(minutes), seconds))
        label.after(50, update_timer, label, stop_button)
    elif stop_button.cget("text") == "Close Window":
        label.config(text="Time elapsed: {:0>2}:{:05.2f}".format(int(minutes), seconds))

def terminate_script(root, stop_button, total_gifs):
    global stop, total_frames
    if stop_button.cget("text") == "Close Window":
        root.destroy()
    else:
        stop = True
        stop_button.config(text="Close Window")
        label.config(text=f"Stopped - Total GIFs processed: {total_gifs} \n\n Total Frames Split: {total_frames}")
        label.update()

################################################################################################################################################
################################################################################################################################################
#           #
# Interface #
#           #

def create_label(root):
    label = tk.Label(root, height=4)
    label.pack(side="top")
    return label

def create_timer_label(root):
    timer_label = tk.Label(root)
    timer_label.pack(side="top")
    return timer_label

def create_stop_button(root, gif_paths):
    stop_button = tk.Button(root, text='Stop', overrelief="groove", command=lambda: terminate_script(root, stop_button, len(gif_paths)))
    stop_button.pack(side="top", fill="x", anchor="s", expand="true", padx=2, pady=2)
    return stop_button

def display_error(message):
    label.config(text=message)
    stop_button.config(text="Close Window")

################################################################################################################################################
################################################################################################################################################
#           #
# Framework #
#           #

def create_root():
    root = tk.Tk()
    root.title(f"{VERSION} - GIFsplit")
    root.resizable(False, False)
    position_window(root)
    return root

def position_window(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (WINDOW_WIDTH / 2)
    y = (screen_height / 2) - (WINDOW_HEIGHT / 2)
    root.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))

def set_window_close_protocol(root, stop_button, gif_paths):
    root.protocol("WM_DELETE_WINDOW", lambda: [terminate_script(root, stop_button, len(gif_paths)) for _ in range(2)])

def set_icon(root):
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)
    icon_path = os.path.join(application_path, "icon.ico")
    try:
        root.iconbitmap(icon_path)
    except TclError:
        pass

parser = argparse.ArgumentParser()
parser.add_argument("--noui", help="disable the interface", action="store_true")
parser.add_argument("paths", nargs='*', help="paths to the GIF files")
args = parser.parse_args()

if not args.noui:
    root = create_root()
    gif_paths = select_gif()
    label = create_label(root)
    timer_label = create_timer_label(root)
    stop_button = create_stop_button(root, gif_paths)
    set_window_close_protocol(root, stop_button, gif_paths)
    set_icon(root)
    update_timer(timer_label, stop_button)
    process_all_gifs(gif_paths, label, stop_button)
    root.mainloop()
else:
    gif_paths = args.paths
    process_all_gifs(gif_paths, None, None)

################################################################################################################################################
################################################################################################################################################
#           #
# Changelog #
#           #

'''

- v1.07 changes:
  - New:
    -

  - Fixed:
    - Fix processing multiple files.
    - The app window now closes immediately.

'''
