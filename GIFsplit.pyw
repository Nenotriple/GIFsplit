# This script extracts frames from a GIF file and saves them as PNG images in a new directory.
# To use this script, drag and drop your GIF file onto the script.

import sys, os, threading, time
from PIL import Image
import tkinter as tk

# Global variable to control the script execution
stop = False

# Function to stop the script execution
def stop_script():
    global stop
    stop = True

# Function to convert a GIF to PNG frames
def gif_to_png(gif_path, label, current_gif, total_gifs):
    global stop
    # Extracting the filename and creating an output folder for the frames
    filename = os.path.splitext(os.path.basename(gif_path))[0]
    output_folder = os.path.join(os.path.dirname(gif_path), filename)
    os.makedirs(output_folder, exist_ok=True)

    # Opening the GIF image using PIL
    img = Image.open(gif_path)

    # Looping through each frame in the GIF image
    for i in range(img.n_frames):
        if stop: break  # Stop if the global stop variable is True
        img.seek(i)  # Seeking to the ith frame
        img.save(f'{output_folder}/frame_{i}.png')  # Saving the ith frame as a PNG image
        label.config(text=f'Current GIF: {current_gif}, Total GIFs: {total_gifs}')  # Updating the label text
        label.update()  # Updating the label

# Function to process multiple GIFs
def process_gifs(gif_paths, label):
    total_gifs = len(gif_paths)  # Total number of GIFs to process
    for i, gif_path in enumerate(gif_paths, start=1):  # Looping through each GIF path
        if stop: break  # Stop if the global stop variable is True
        gif_to_png(gif_path, label, i, total_gifs)  # Converting the GIF to PNG frames

# Function to update a working label periodically
def update_working_label(label):
    global stop
    while not stop:  # Keep running until the global stop variable is True
        for _ in range(3):  # Loop three times
            if stop: return  # Stop if the global stop variable is True
            label.config(text="    working." + "."*_)  # Updating the label text with a varying number of dots
            time.sleep(0.3)  # Sleep for a short duration

# Main script execution starts here if command line arguments are provided
if len(sys.argv) > 1:
    root = tk.Tk()  # Creating a Tkinter root window
    root.geometry('225x150')  # Setting the window size
    root.title("GIFsplit")  # Setting the window title
    root.resizable(False, False)  # Making the window non-resizable

    separator1 = tk.Label(root, text="", height=1)
    separator1.pack()

    label = tk.Label(root)  # Creating a label widget
    label.pack()  # Packing the label

    separator2 = tk.Label(root, text="", height=1)
    separator2.pack()

    stop_button = tk.Button(root, text='Stop', command=stop_script)  # Creating a button widget to stop the script execution
    stop_button.pack(fill="x")  # Packing the button

    separator3 = tk.Label(root, text="", height=1)
    separator3.pack()

    working_label = tk.Label(root, text="    working...", width=10, anchor='w')  # Creating a working label widget
    working_label.pack()  # Packing the working label

    threading.Thread(target=process_gifs, args=(sys.argv[1:], label)).start()  # Starting a new thread to process GIFs
    threading.Thread(target=update_working_label, args=(working_label,)).start()  # Starting a new thread to update the working label

    root.mainloop()  # Starting the Tkinter event loop
