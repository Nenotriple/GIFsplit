import sys
import os
from PIL import Image

# This script extracts frames from a GIF file and saves them as PNG images in a new directory.
# To use this script, drag and drop your GIF file onto the script.

def gif_to_png(gif_path):
    # Extract the filename without the extension from the provided path
    filename = os.path.splitext(os.path.basename(gif_path))[0]
    
    # Create a new directory with the same name as the GIF file in the same location
    output_folder = os.path.join(os.path.dirname(gif_path), filename)
    
    # If the directory does not exist, create it
    os.makedirs(output_folder, exist_ok=True)

    # Open the GIF file using PIL's Image module
    img = Image.open(gif_path)
    
    # Loop over each frame in the GIF file
    for i in range(img.n_frames):
        # Set the current frame of the GIF file
        img.seek(i)
        
        # Save the current frame as a PNG image in the output directory
        img.save(f'{output_folder}/frame_{i}.png')

# Check if a GIF file path was provided as a command line argument
if len(sys.argv) > 1:
    # If a GIF file path was provided, extract its frames and save them as PNG images
    gif_to_png(sys.argv[1])
else:
    # If no GIF file path was provided, print a usage message
    print("Please drag a GIF file onto this script.")
