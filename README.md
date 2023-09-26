# GIFsplit: GIF to PNG Frame Extractor

![GIFsplit](https://github.com/Nenotriple/GIFsplit/assets/70049990/c33f0c41-d597-450c-b686-6d49d5e45f03)

**Functionality**

The script accepts a GIF file as input, traverses through each frame in the GIF, and saves each frame as a separate PNG image. The output images are stored in a newly created directory that shares the name of the input GIF file.

**Usage Instructions**

1. Install the Pillow library via pip using the command: `pip install pillow`
2. Execute the script in one of 3 ways:
- **Drag and Drop**: Simply drag and drop your GIF(s) onto the script with .pyw extension.
- **File Dialog**: Just run the script and it will open a file dialog where you can choose your GIF(s)
- **Command Line**: Example: ```python GIFsplit.pyw "gif 1.gif" "gif 2.gif" "gif 3.gif"...```

The script will create a new directory in the same location as your GIF file.

Each frame of the GIF will be saved as an individual .png image within this directory.
