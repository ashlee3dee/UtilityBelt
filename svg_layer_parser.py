import os
import argparse
from svglib.svglib import SvgRenderer
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Line
from reportlab.lib import colors
from PIL import Image


def render_image(input_file, output_dir, width, height):
    # Load SVG file and convert to reportlab Group object
    renderer = SvgRenderer(input_file)
    drawing = Group(*renderer.render(svg_node=input_file))

    # Iterate over groups and render bounding box as image
    for i, group in enumerate(drawing.findall(lambda obj: isinstance(obj, Group))):
        x, y, w, h = group.getBounds()
        padding = min(w, h) * 0.1  # Add 10% padding
        bbox = Line(x - padding, y - padding, x + w + padding, y - padding, x + w + padding, y + h + padding,
                    x - padding, y + h + padding, x - padding, y - padding, strokeColor=colors.red)

        # Create temporary image file and scale to fixed size
        img_path = os.path.join(output_dir, f"image_{i}.png")
        renderPM.drawToFile(bbox, img_path, fmt="PNG")
        img = Image.open(img_path)
        img.thumbnail((width, height))
        img.save(img_path)


def main():
    parser = argparse.ArgumentParser(description="Render each group in an SVG file as a fixed size image.")
    parser.add_argument("input_file", help="Path to the input SVG file.")
    parser.add_argument("output_dir", help="Path to the output directory for the images.")
    parser.add_argument("--width", type=int, default=500, help="Width of the output images.")
    parser.add_argument("--height", type=int, default=500, help="Height of the output images.")
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    render_image(args.input_file, args.output_dir, args.width, args.height)


if __name__ == "__main__":
    main()
