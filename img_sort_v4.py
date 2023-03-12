import argparse
import os
import cv2

def main():
    parser = argparse.ArgumentParser(
        prog = 'PyImgSort',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=
'''
ABOUT:
Image viewer with save and delete options.
--------------------------------------------------------------
CONTROLS:
s: save current image to output_dir
d: delete current image from search_dir
n: display the next image
p: display the previous image
q: quit program
'''
)
    parser.add_argument('search_dir', type=str, help='the directory to search for images')
    parser.add_argument('output_dir', type=str, help='the directory to save images')
    args = parser.parse_args()

    # Get a list of image files in the search directory
    img_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    img_files = []
    for root, dirs, files in os.walk(args.search_dir):
        for file in files:
            if file.lower().endswith(img_exts):
                img_files.append(os.path.join(root, file))

    # Display images and allow save/delete options
    idx = 0
    while True:
        img = cv2.imread(img_files[idx])
        img_h, img_w, _ = img.shape
        scale = min(800/img_w, 600/img_h)
        img = cv2.resize(img, (int(scale*img_w), int(scale*img_h)))
        cv2.imshow('Image Viewer', img)
        key = cv2.waitKey(0)

        if key == ord('q'):
            break
        elif key == ord('s'):
            os.rename(img_files[idx], os.path.join(args.output_dir, os.path.basename(img_files[idx])))
            del img_files[idx]
            if idx >= len(img_files):
                idx = 0
        elif key == ord('d'):
            os.remove(img_files[idx])
            del img_files[idx]
            if idx >= len(img_files):
                idx = 0
        elif key == ord('n'):
            idx = (idx + 1) % len(img_files)
        elif key == ord('p'):
            idx = (idx - 1) % len(img_files)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
