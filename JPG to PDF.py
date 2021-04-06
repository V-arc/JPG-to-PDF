import os
import re

from fpdf import FPDF
from PIL import Image


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


pdf = FPDF()
# Contains the list of all images to be converted to PDF.
imagelist = []


# --------------- USER INPUT -------------------- #

# Folder containing all the images.
folder = r""
# Name of the output PDF file.
name = r""


# ------------- ADD ALL THE IMAGES IN A LIST ------------- #

for dirpath, dirnames, filenames in os.walk(folder):
    # Sort the images by name.
    filenames.sort(key=natural_keys)
    for filename in [f for f in filenames if f.endswith(".jpg")]:
        full_path = os.path.join(dirpath, filename)
        imagelist.append(full_path)

for i in range(0, len(imagelist)):
    print(imagelist[i])

# --------------- ROTATE ANY LANDSCAPE MODE IMAGE IF PRESENT ----------------- #

for i in range(0, len(imagelist)):
    # Open the image.
    im1 = Image.open(imagelist[i])
    # Get the width and height of that image.
    width, height = im1.size
    if width > height:
        # If width > height, rotate the image.
        im2 = im1.transpose(Image.ROTATE_270)
        # Delete the previous image.
        os.remove(imagelist[i])
        # Save the rotated image.
        im2.save(imagelist[i])
        # im.save

print("\nFound " + str(len(imagelist)) +
      " image files. Converting to PDF....\n")


# -------------- CONVERT TO PDF ------------ #

for image in imagelist:
    pdf.add_page()
    # 210 and 297 are the dimensions of an A4 size sheet.
    pdf.image(image, 0, 0, 210, 297)

# Save the PDF.
pdf.output(folder + name, "F")

print("PDF generated successfully!")
