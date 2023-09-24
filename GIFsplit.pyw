# This script extracts frames from a GIF file and saves them as PNG images in a new directory.
# To use this script, drag and drop your GIF file(s) onto the script, or by commandline: python gifsplit.py [gif_path1, gif_path2] ...

import sys, os
from PIL import Image
import tkinter as tk
import time

stop = False
start_time = time.time()

def timer(label, stop_button):
    if not stop and stop_button.cget("text") != "Close Window":
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        label.config(text="Time elapsed: {:0>2}:{:05.2f}".format(int(minutes), seconds))
        label.after(250, timer, label, stop_button)

def stop_script(root, stop_button):
    global stop
    if stop_button.cget("text") == "Close Window":
        root.destroy()
    else:
        stop = True
        label.config(text="Stopped")
        label.update()

# Function to convert a GIF image into PNG frames
def gif_to_png(gif_path, label, current_gif, total_gifs, stop_button):
    global stop
    # Extract the filename and create an output folder for the frames
    filename = os.path.splitext(os.path.basename(gif_path))[0]
    output_folder = os.path.join(os.path.dirname(gif_path), filename)
    os.makedirs(output_folder, exist_ok=True)

    # Open the GIF image and save each frame as a PNG image
    img = Image.open(gif_path)
    for i in range(img.n_frames):
        if stop: break
        img.seek(i)
        img.save(f'{output_folder}/frame_{i}.png')
        label.config(text=f'Current GIF: {current_gif}, Total GIFs: {total_gifs}')
        label.update()

        # Update the label text when all GIFs are processed
        if current_gif == total_gifs and i == img.n_frames - 1:
            label.config(text=f"Done! - Total GIFs processed: {total_gifs}")
            stop_button.config(text="Close Window")
            label.update()

# Function to process multiple GIF images
def process_gifs(gif_paths, label, stop_button):
    total_gifs = len(gif_paths)
    for i, gif_path in enumerate(gif_paths, start=1):
        if stop: break
        gif_to_png(gif_path, label, i, total_gifs, stop_button)

# Create a simple Tkinter window with a label and a stop button
if len(sys.argv) > 1:
    root = tk.Tk()
    root.geometry('225x110')
    root.title("GIFsplit")
    root.resizable(False, False)

    separator1 = tk.Label(root, text="", height=1)
    separator1.pack()

    label = tk.Label(root)
    label.pack()

    working_label = tk.Label(root)
    working_label.pack(pady=10)

    stop_button = tk.Button(root, text='Stop', command=lambda: stop_script(root, stop_button))
    stop_button.pack(fill="x")

    timer(working_label, stop_button)  # Start the timer

    separator3 = tk.Label(root, text="", height=1)
    separator3.pack()

    # Process the GIF images passed as arguments to the script
    process_gifs(sys.argv[1:], label, stop_button)

    root.mainloop()

