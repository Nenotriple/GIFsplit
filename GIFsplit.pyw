##################      github.com/Nenotriple
#                #
#    GIFsplit    # This script allows you to convert GIF files into individual PNG frames. You can use it in three ways:
#                #      1. Drag and Drop: Simply drag and drop your GIF(s) onto the script.
##################      2. File Dialog: Just double-click the script and it will open a file dialog where you can choose your GIF(s).
# Requirements:  #      3. Command Line: Example: python GIFsplit.pyw "gif 1.gif" "gif 2.gif" "gif 3.gif"
# pillow         #
#                # The script will create a new folder for each GIF, named after the original file, where it will save the PNG frames.
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

def select_gif(noui):
    if noui:
        gif_paths = sys.argv[2:] if len(sys.argv) > 2 else input("Enter the path of your GIF files: ").split()
    else:
        root.withdraw()
        gif_paths = sys.argv[1:] if len(sys.argv) > 1 else filedialog.askopenfilenames(filetypes=[("GIF files", "*.gif")])
        root.deiconify()
    if not gif_paths:
        sys.exit()
    return gif_paths
# Alter the "Processing GIF" print statements to be made on a single line in the command-line, replacing the previous line.
def convert_gif_to_png(gif_path, label, current_gif, total_gifs, stop_button, noui):
    global stop, total_frames
    filename = os.path.splitext(os.path.basename(gif_path))[0]
    output_folder = os.path.join(os.path.dirname(gif_path), filename)
    os.makedirs(output_folder, exist_ok=True)
    try:
        if not gif_path.lower().endswith('.gif'):
            raise IOError("\n Invalid file format. Please use a GIF image.")
        img = Image.open(gif_path)
        for i in range(img.n_frames):
            if stop: break
            img.seek(i)
            img.save(f'{output_folder}/frame_{i}.png')
            total_frames += 1
            if noui:
                print(f'\rProcessing GIF {current_gif} of {total_gifs} | Frame: {str(i+1).zfill(4)} of {str(img.n_frames).zfill(4)} | Total Frames Split: {str(total_frames).zfill(5)}', end='')
            else:
                label.config(text=f'GIF {current_gif} of {total_gifs} \n\n Frame: {i+1} of {img.n_frames}\nTotal Frames Split: {total_frames}')
                label.update()
        if noui and current_gif == total_gifs:
            print(f"\n\nDone! - Total GIFs processed: {total_gifs}, Total Frames Split: {str(total_frames).zfill(5)}\n")
        elif not noui:
            stop_button.config(text="Close Window")
            stop = True
            label.update()
    except IOError as e:
        file_name = os.path.basename(gif_path)
        file_type = os.path.splitext(file_name)[1]
        display_error(f"Error opening file type: {file_type} \n {str(e)}")


def process_all_gifs(gif_paths, label, stop_button, noui):
    total_gifs = len(gif_paths)
    for i, gif_path in enumerate(gif_paths, start=1):
        if stop: break
        convert_gif_to_png(gif_path, label, i, total_gifs, stop_button, noui)

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
    label = tk.Label(root)
    label.pack()
    return label

def create_timer_label(root):
    timer_label = tk.Label(root)
    timer_label.pack(pady=10)
    return timer_label

def create_stop_button(root, gif_paths):
    stop_button = tk.Button(root, text='Stop', command=lambda: terminate_script(root, stop_button, len(gif_paths)))
    stop_button.pack(side="bottom", fill="x", anchor="s")
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
    root.title("v1.06 - GIFsplit")
    root.geometry('250x130')
    root.resizable(False, False)
    return root

def set_window_close_protocol(root, stop_button, gif_paths):
    root.protocol("WM_DELETE_WINDOW", lambda: terminate_script(root, stop_button, len(gif_paths)))

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

# Argument Parser
parser = argparse.ArgumentParser(description= "--- github.com/Nenotriple --- This app allows you to convert GIF files into individual PNG frames. The app will create a new folder for each GIF, named after the original file, where it will save the PNG frames.", add_help=False)
parser.add_argument('path', nargs='*', help='The path to your gif files.')
parser.add_argument('--noui', action='store_true', help='Run the app without launching the interface (ui)')

if any(arg in sys.argv for arg in ['help', 'Help', '?', 'h', 'H', 'info', 'commands']):
    parser.print_help()
    sys.exit()

args = parser.parse_args()

root = create_root() if not args.noui else None
gif_paths = select_gif(args.noui)
label = create_label(root) if not args.noui else None
timer_label = create_timer_label(root) if not args.noui else None
stop_button = create_stop_button(root, gif_paths) if not args.noui else None
set_window_close_protocol(root, stop_button, gif_paths) if not args.noui else None
set_icon(root) if not args.noui else None
update_timer(timer_label, stop_button) if not args.noui else None
process_all_gifs(gif_paths, label, stop_button, args.noui)

root.mainloop() if not args.noui else None

################################################################################################################################################
################################################################################################################################################
#           #
# Changelog #
#           #

'''

- v1.06 changes:
  - New:
    - You can now use the argument `--noui` when running by command-line to disable the interface.
      - Also you can use `help` to get some related info.

  - Fixed:
    -

'''

# Typing an incorrect argument/file creates an empty folder.
