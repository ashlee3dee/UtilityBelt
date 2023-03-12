import argparse
import cv2
import numpy as np
import os

def main(input_image, output_dir, output_size):
    # Load the input image
    img = cv2.imread(input_image)

    # Get the list of contours from the input image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #_, contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate over each contour
    for i, contour in enumerate(contours):
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Crop the object from the image
        object_img = img[y:y+h, x:x+w]

        # Resize the object to a square shape
        size = max(object_img.shape[0], object_img.shape[1])
        object_img = cv2.resize(object_img, (size, size))
        object_img = cv2.resize(object_img, (output_size, output_size))

        # Save the object image
        output_path = os.path.join(output_dir, 'object_{}.jpg'.format(i))
        cv2.imwrite(output_path, object_img)

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input_image', type=str, help='Path to the input image')
    parser.add_argument('output_dir', type=str, help='Path to the output directory')
    parser.add_argument('output_size', type=int, help='Size of the output square images')
    args = parser.parse_args()

    # Call the main function
    main(args.input_image, args.output_dir, args.output_size)
