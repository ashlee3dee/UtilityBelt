import cv2
import numpy as np
import os

def extract_icons(input_image, output_dir, icon_size, padding):
    # Load the input image
    image = cv2.imread(input_image)
    if image is None:
        raise Exception("Error: input image not found")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to create a binary image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        raise Exception("Error: no objects found in the input image")

    # Iterate over the contours and extract each icon
    for i, c in enumerate(contours):
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(c)

        # Extract the icon from the image
        icon = image[y:y + h, x:x + w]

        # Add padding to the icon
        icon = cv2.copyMakeBorder(icon, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=[0, 0, 0, 0])

        # Resize the icon to fit within the desired size
        icon = cv2.resize(icon, (icon_size, icon_size), interpolation=cv2.INTER_CUBIC)

        # Turn black pixels to transparency
        #alpha_channel = np.zeros((icon_size, icon_size), dtype=np.uint8)
        #alpha_channel[np.where((icon == [0, 0, 0]).all(axis=1))] = 255
        #icon = cv2.merge((icon, alpha_channel))

        # Save the icon as a separate image
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, f"icon_{i}.png")
        cv2.imwrite(output_path, icon)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_image", help="path to the input image")
    parser.add_argument("output_dir", help="path to the output directory")
    parser.add_argument("icon_size", type=int, help="desired size of the output icons")
    parser.add_argument("--padding", type=int, default=0, help="amount of padding to add around the icons")
    args = parser.parse_args()

    try:
        extract_icons(args.input_image, args.output_dir, args.icon_size, args.padding)
    except Exception as e:
        print(f"Error: {str(e)}")
