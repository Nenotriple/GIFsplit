#   This script allows you to convert GIF files into individual PNG frames. You can use it in three ways:
#   
#   1. Drag and Drop: Simply drag and drop your GIF(s) onto the script with .pyw extension.
#   2. File Dialog: Just run the script and it will open a file dialog where you can choose your GIF(s)
#   3. Command Line: Use the command line to run the script with your GIF(s) as arguments. For example: python GIFsplit.pyw "gif 1.gif" "gif 2.gif" "gif 3.gif"...
#   
#   The script will create a new folder for each GIF, named after the original file, where it will save the PNG frames.

import os
import sys
import time
import tkinter as tk
from PIL import Image
from tkinter import filedialog

stop = False
total_frames = 0

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
        label.config(text=f"Stopped - Total GIFs processed: {total_gifs} \n\n Total Frames processed: {total_frames}")
        label.update()

def display_error(message):
    label.config(text=message)
    stop_button.config(text="Close Window")

def convert_gif_to_png(gif_path, label, current_gif, total_gifs, stop_button):
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

            label.config(text=f'{current_gif} of {total_gifs} \n\n Frame: {i+1} of {img.n_frames}, Total Frames: {total_frames}')
            label.update()

            if current_gif == total_gifs and i == img.n_frames - 1:
                label.config(text=f"Done! - Total GIFs processed: {total_gifs} \n\n Total Frames processed: {total_frames}")
                stop_button.config(text="Close Window")
                stop = True
                label.update()
    except IOError as e:
        file_name = os.path.basename(gif_path)
        file_type = os.path.splitext(file_name)[1]
        display_error(f"Error opening file type: {file_type} \n {str(e)}")

def process_all_gifs(gif_paths, label, stop_button):
    total_gifs = len(gif_paths)
    for i, gif_path in enumerate(gif_paths, start=1):
        if stop: break
        convert_gif_to_png(gif_path, label, i, total_gifs, stop_button)

root = tk.Tk()
root.geometry('250x120')
root.title("v1.04 - GIFsplit")
root.resizable(False, False)

label = tk.Label(root)
label.pack()

timer_label = tk.Label(root)
timer_label.pack(pady=10)

root.withdraw()
gif_paths = sys.argv[1:] if len(sys.argv) > 1 else filedialog.askopenfilenames(filetypes=[("GIF files", "*.gif")])
root.deiconify()

if not gif_paths:
    sys.exit()

stop_button = tk.Button(root, text='Stop', command=lambda: terminate_script(root, stop_button, len(gif_paths)))
stop_button.pack(side="bottom", fill="x")

start_time = time.time()
update_timer(timer_label, stop_button)

process_all_gifs(gif_paths, label, stop_button)

root.mainloop()
