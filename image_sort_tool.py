import os
import sys
import glob
import tkinter as tk
from PIL import Image, ImageTk

# Command line arguments
search_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.getcwd(), 'saved')
recursive = True if len(sys.argv) > 3 and sys.argv[3] == '-r' else False

# Find all image files in the search directory
if recursive:
    search_pattern = os.path.join(search_dir, '**', '*.*')
else:
    search_pattern = os.path.join(search_dir, '*.*')
image_files = sorted(glob.glob(search_pattern, recursive=recursive))
image_index = 0

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Create the main window
root = tk.Tk()
root.title('Image Viewer')

# Create the image canvas
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Load the first image
current_image = Image.open(image_files[image_index])
current_image.thumbnail((800, 600))
tk_image = ImageTk.PhotoImage(current_image)
image_item = canvas.create_image(0, 0, anchor='nw', image=tk_image)

# Define the button actions
def next_image():
    global image_index, current_image, tk_image, image_item
    image_index = (image_index + 1) % len(image_files)
    current_image = Image.open(image_files[image_index])
    current_image.thumbnail((800, 600))
    tk_image = ImageTk.PhotoImage(current_image)
    canvas.itemconfig(image_item, image=tk_image)

def prev_image():
    global image_index, current_image, tk_image, image_item
    image_index = (image_index - 1) % len(image_files)
    current_image = Image.open(image_files[image_index])
    current_image.thumbnail((800, 600))
    tk_image = ImageTk.PhotoImage(current_image)
    canvas.itemconfig(image_item, image=tk_image)

def save_image():
    global image_index, current_image
    output_file = os.path.join(output_dir, os.path.basename(image_files[image_index]))
    current_image.save(output_file)
    next_image()

def delete_image():
    global image_index, current_image
    os.remove(image_files[image_index])
    image_files.pop(image_index)
    if image_index >= len(image_files):
        image_index = 0
    current_image = Image.open(image_files[image_index])
    current_image.thumbnail((800, 600))
    tk_image = ImageTk.PhotoImage(current_image)
    canvas.itemconfig(image_item, image=tk_image)

# Create the button frame
button_frame = tk.Frame(root)
button_frame.pack()

# Create the buttons
next_button = tk.Button(button_frame, text='Next', command=next_image)
next_button.pack(side='left')
prev_button = tk.Button(button_frame, text='Prev', command=prev_image)
prev_button.pack(side='left')
save_button = tk.Button(button_frame, text='Save', command=save_image)
save_button.pack(side='left')
delete_button = tk.Button(button_frame, text='Delete', command=delete_image)
delete_button.pack(side='left')

# Start the main event loop
root.mainloop()
