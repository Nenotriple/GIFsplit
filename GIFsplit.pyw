import sys
import os
from PIL import Image

# Simply drag your gif onto the .pyw script and it will extract the frames and save them as .png in a new directory.

def gif_to_png(gif_path):
    # Get the filename without the extension
    filename = os.path.splitext(os.path.basename(gif_path))[0]
    # Create a new directory with the filename
    output_folder = os.path.join(os.path.dirname(gif_path), filename)
    os.makedirs(output_folder, exist_ok=True)

    img = Image.open(gif_path)
    for i in range(img.n_frames):
        img.seek(i)
        img.save(f'{output_folder}/frame_{i}.png')

# Usage
if len(sys.argv) > 1:
    gif_to_png(sys.argv[1])
else:
    print("Please drag a GIF file onto this script.")