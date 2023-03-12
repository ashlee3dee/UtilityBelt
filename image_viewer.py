import os
import glob
import tkinter as tk
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, search_dir, output_dir, recursive):
        self.photo = None
        self.image_width = 800
        self.image_height = 600
        self.image_list = []
        self.current_index = 0
        self.search_dir = search_dir
        self.output_dir = output_dir
        self.recursive = recursive

        self.window = tk.Tk()
        self.window.title("Image Viewer")

        self.canvas = tk.Canvas(self.window, width=800, height=600)
        self.canvas.pack()

        self.next_button = tk.Button(self.window, text="Next", command=self.show_next_image)
        self.next_button.pack(side=tk.RIGHT)

        self.prev_button = tk.Button(self.window, text="Previous", command=self.show_previous_image)
        self.prev_button.pack(side=tk.RIGHT)

        self.save_button = tk.Button(self.window, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.window, text="Delete", command=self.delete_image)
        self.delete_button.pack(side=tk.LEFT)

        self.load_images()
        self.show_image()

        self.window.mainloop()

    def load_images(self):
        search_path = os.path.join(self.search_dir, "**/*.jpg" if self.recursive else "*.jpg")
        for file_path in glob.glob(search_path, recursive=self.recursive):
            self.image_list.append(file_path)

    def show_image(self):
        self.canvas.delete("all")
        file_path = self.image_list[self.current_index]
        image = Image.open(file_path)
        image_width, image_height = image.size
        scale = min(self.image_width / image_width, self.image_height / image_height)
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image((self.image_width - new_width) // 2, (self.image_height - new_height) // 2, image=self.photo, anchor=tk.NW)
        self.window.title(f"Image Viewer - {file_path}")


    def show_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.image_list)
        self.show_image()

    def show_previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.image_list)
        self.show_image()

    def save_image(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        file_path = self.image_list[self.current_index]
        output_file = os.path.join(self.output_dir, os.path.basename(file_path))
        shutil.copyfile(file_path, output_file)
        self.delete_image()

    def delete_image(self):
        file_path = self.image_list[self.current_index]
        os.remove(file_path)
        self.image_list.pop(self.current_index)
        if self.current_index >= len(self.image_list):
            self.current_index = 0
        self.show_image()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Image Viewer')
    parser.add_argument('search_dir', type=str, help='The directory to search for images')
    parser.add_argument('output_dir', type=str, help='The directory to save images')
    parser.add_argument('--recursive', action='store_true', help='Recursively search for images')
    args = parser.parse_args()

    viewer = ImageViewer(args.search_dir, args.output_dir, args.recursive)
