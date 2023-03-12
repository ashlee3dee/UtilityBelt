import os
import sys
import hashlib

def find_images(directory):
    """Recursively find all image files in a directory."""
    image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                images.append(os.path.join(root, file))
    return images

def delete_duplicates(dir1, dir2, test_mode):
    """Find and delete duplicate images in dir2."""
    dir1_images = set([hashlib.md5(open(img, 'rb').read()).hexdigest() for img in find_images(dir1)])
    dir2_images = find_images(dir2)
    for img in dir2_images:
        md5_hash = hashlib.md5(open(img, 'rb').read()).hexdigest()
        if md5_hash in dir1_images:
            if test_mode:
                print(f"Found duplicate: {img}")
            else:
                os.remove(img)

if __name__ == "__main__":
    dir1 = sys.argv[1]
    dir2 = sys.argv[2]
    test_mode = sys.argv[3].lower() == "true"
    delete_duplicates(dir1, dir2, test_mode)
