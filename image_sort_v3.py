import os
import argparse
import tkinter as tk
from PIL import Image, ImageTk


class ImageViewer:
    def __init__(self, search_dir, output_dir, recursive):
        self.images = []
        self.current_index = 0
        self.search_dir = search_dir
        self.output_dir = output_dir
        self.recursive = recursive

        # create main window
        self.root = tk.Tk()
        self.root.title("Image Viewer")
        self.root.geometry("600x400")

        # create image label
        self.image_label = tk.Label(self.root)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # create button frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # create next button
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # create previous button
        self.prev_button = tk.Button(self.button_frame, text="Previous", command=self.prev_image)
        self.prev_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # create save button
        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        # create delete button
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_image)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        # search for images
        self.search_images(self.search_dir)

        # display first image
        self.display_image()

        # start main loop
        self.root.mainloop()

    def search_images(self, directory):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isdir(filepath):
                if self.recursive:
                    self.search_images(filepath)
            elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.images.append(filepath)

    def display_image(self):
        # load image
        image_path = self.images[self.current_index]
        pil_image = Image.open(image_path)

        # scale image to fit window
        window_width, window_height = self.root.winfo_width(), self.root.winfo_height()
        image_width, image_height = pil_image.size
        if image_width > window_width or image_height > window_height:
            scale_factor = min(window_width / image_width, window_height / image_height)
            new_size = (int(image_width * scale_factor), int(image_height * scale_factor))
            pil_image = pil_image.resize(new_size)

        # update label with new image
        tk_image = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.images)
        self.display_image()

    def prev_image(self):
        self.current_index = (self.current_index - 1) % len(self.images)
        self.display_image()

    def save_image(self):
        image_path = self.images[self.current_index]
        output_path = os.path.join(self.output_dir, os.path.basename(image_path))
        os.makedirs(self.output_dir, exist_ok=True)
        with open(output_path, 'wb') as f:
            with open(image_path, 'rb') as g:
                f.write(g.read())
        self.next_image()

    def delete_image(self):
        image_path = self.images[self.current_index]
        os.remove(image_path)
        self.images.remove(image_path)
        self.current_index = self.current_index % len(self.images)
        self.display_image()

if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Recursively search a directory for images and display them in a window')
        parser.add_argument('search_dir', nargs='?', default='.', help='Search directory (default: current directory)')
        parser.add_argument('-o', '--output-dir', default='saved', help='Output directory for saved images (default: "saved" subdirectory in current directory)')
        parser.add_argument('-r', '--recursive', action='store_true', help='Recursively search subdirectories for images')
        args = parser.parse_args()
