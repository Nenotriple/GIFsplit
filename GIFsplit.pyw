# This script extracts frames from a GIF file and saves them as PNG images in a new directory.
# To use this script, drag and drop your GIF file(s) onto the script, or by commandline: python GIFsplit.py [gif_path1, gif_path2] ...

import sys, os
from PIL import Image
import tkinter as tk
import time

stop = False
start_time = time.time()
total_frames = 0

def timer(label, stop_button):
    if not stop and stop_button.cget("text") != "Close Window":
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        label.config(text="Time elapsed: {:0>2}:{:05.2f}".format(int(minutes), seconds))
        label.after(50, timer, label, stop_button)
    elif stop_button.cget("text") == "Close Window":
        label.config(text="Time elapsed: {:0>2}:{:05.2f}".format(int(minutes), seconds))

def stop_script(root, stop_button, total_gifs):
    global stop, total_frames
    if stop_button.cget("text") == "Close Window":
        root.destroy()
    else:
        stop = True
        stop_button.config(text="Close Window")
        label.config(text=f"Stopped - Total GIFs processed: {total_gifs} \n\n Total Frames processed: {total_frames}")
        label.update()

# Function to convert a GIF image into PNG frames
def gif_to_png(gif_path, label, current_gif, total_gifs, stop_button):
    global stop, total_frames
    # Extract the filename and create an output folder for the frames
    filename = os.path.splitext(os.path.basename(gif_path))[0]
    output_folder = os.path.join(os.path.dirname(gif_path), filename)
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Open the GIF image and save each frame as a PNG image
        img = Image.open(gif_path)
        for i in range(img.n_frames):
            if stop: break
            img.seek(i)
            img.save(f'{output_folder}/frame_{i}.png')
            total_frames += 1
            label.config(text=f'{current_gif} of {total_gifs} \n\n Frame: {i+1} of {img.n_frames}, Total Frames: {total_frames}')
            label.update()

            # Update the label text when all GIFs are processed
            if current_gif == total_gifs and i == img.n_frames - 1:
                label.config(text=f"Done! - Total GIFs processed: {total_gifs} \n\n Total Frames processed: {total_frames}")
                stop_button.config(text="Close Window")
                stop = True
                label.update()
    except IOError:
        print(f"Error opening file {gif_path}. Please check if the file exists and is a valid GIF image.")

# Function to process multiple GIF images
def process_gifs(gif_paths, label, stop_button):
    total_gifs = len(gif_paths)
    for i, gif_path in enumerate(gif_paths, start=1):
        if stop: break
        gif_to_png(gif_path, label, i, total_gifs, stop_button)

# Create a Tkinter window with a label and stop button
if len(sys.argv) > 1:
    root = tk.Tk()
    root.geometry('250x120')
    root.title("v1.03 - GIFsplit")
    root.resizable(False, False)

    label = tk.Label(root)
    label.pack()

    working_label = tk.Label(root)
    working_label.pack(pady=10)

    stop_button = tk.Button(root, text='Stop', command=lambda: stop_script(root, stop_button,len(sys.argv) - 1))
    stop_button.pack(side="bottom", fill="x")

    timer(working_label, stop_button)

    # Process the GIF images passed as arguments to the script
    process_gifs(sys.argv[1:], label, stop_button)

root.mainloop()
