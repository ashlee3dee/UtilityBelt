import os
from PIL import ImageTk, Image
import tkinter as tk

# Function to search for image files in a directory and its subdirectories
def search_images(directory):
    image_files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isdir(filepath):
            image_files += search_images(filepath)
        elif filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            image_files.append(filepath)
    return image_files

# Function to display an image in a slideshow window
def show_image(filepath, root):
    root.title(filepath)
    img = Image.open(filepath)
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=photo)
    label.pack()
    
    # Bind left and right arrow keys to move to previous and next images
    root.bind("<Left>", lambda event: show_previous_image())
    root.bind("<Right>", lambda event: show_next_image())
    # Bind mouse click to move to next image
    label.bind("<Button-1>", lambda event: show_next_image())

    # Function to move to previous image
    def show_previous_image():
        label.pack_forget()
        root.unbind("<Left>")
        root.unbind("<Right>")
        label.unbind("<Button-1>")
        index = image_files.index(filepath)
        if index == 0:
            index = len(image_files) - 1
        else:
            index -= 1
        show_image(image_files[index], root)

    # Function to move to next image
    def show_next_image():
        label.pack_forget()
        root.unbind("<Left>")
        root.unbind("<Right>")
        label.unbind("<Button-1>")
        index = image_files.index(filepath)
        if index == len(image_files) - 1:
            index = 0
        else:
            index += 1
        show_image(image_files[index], root)

    root.mainloop()

# Get a list of image files and display them in a slideshow
image_files = search_images('.')
root = tk.Tk()
for filepath in image_files:
    show_image(filepath, root)
