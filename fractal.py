from PIL import Image
from numpy import array
import colorsys

# setting the width, height and zoom
WIDTH, HEIGHT = 512, 512
ZOOM = 4

# creating the new image in RGB mode
im = Image.new("RGB", (WIDTH, HEIGHT))

# some color constants to use
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# a function to calculate the color of a pixel based on its complex value
def mandelbrot(c, max_iter=100):
    z = complex(0, 0)
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > 2:
            return i
    return max_iter

# creating the Mandelbrot set
for x in range(WIDTH):
    for y in range(HEIGHT):
        c = complex(x / WIDTH - 0.5, y / HEIGHT - 0.5) * ZOOM
        color = mandelbrot(c)
        r, g, b = colorsys.hsv_to_rgb(color / 255, 1, 0.5)
        im.putpixel((x, y), (int(r * 255), int(g * 255), int(b * 255)))

# showing the created fractal
im.show()



