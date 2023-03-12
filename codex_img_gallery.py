
import os
import sys
import argparse
import tkinter as tk
import cv2

# parse user arguments
parser = argparse.ArgumentParser(description='Sort images into two directories')
parser.add_argument('input_dir', help='input directory')
parser.add_argument('output_dir', help='output directory')
parser.add_argument('-r', '--recursive', action='store_true', help='recursively search input directory')
args = parser.parse_args()

# create a list of all the images in the input directory
image_list = []
for root, dirs, files in os.walk(args.input_dir):
    for file in files:
        if file.endswith('.jpg') or file.endswith('.png'):
            image_list.append(os.path.join(root, file))

# create a graphical window using tkinter and cv2
window = tk.Tk()
window.title('Image Sorter')
window.geometry('800x600')

# display the images in a slideshow gallery with forward/back buttons
image_index = 0
image_label = tk.Label(window)
image_label.pack()

def show_image():
    global image_index
    image_label.config(image=tk.PhotoImage(file=image_list[image_index]))

def next_image():
    global image_index
    image_index += 1
    if image_index >= len(image_list):
        image_index = 0
    show_image()

def prev_image():
    global image_index
    image_index -= 1
    if image_index < 0:
        image_index = len(image_list) - 1
    show_image()

# add a button to save the current image to the output directory and display the next image
def save_image():
    global image_index
    os.rename(image_list[image_index], os.path.join(args.output_dir, os.path.basename(image_list[image_index])))
    del image_list[image_index]
    next_image()

# add a button to delete the current image and display the next image
def delete_image():
    global image_index
    os.remove(image_list[image_index])
    del image_list[image_index]
    next_image()

# create buttons
prev_button = tk.Button(window, text='Previous', command=prev_image)
prev_button.pack(side='left')
save_button = tk.Button(window, text='Save', command=save_image)
save_button.pack(side='left')
delete_button = tk.Button(window, text='Delete', command=delete_image)
delete_button.pack(side='left')
next_button = tk.Button(window, text='Next', command=next_image)
next_button.pack(side='left')

# display the first image
show_image()

# start the GUI
window.mainloop()
