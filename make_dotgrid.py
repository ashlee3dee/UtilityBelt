"""
This script generates a black and white image with dots arranged in a grid or randomly scattered, and saves it to a file.

Author: Ashlee3dee
Version: 0.2a
License: Open source

Usage:
    Run the script and follow the prompts to specify the image dimensions, dot size, dot spacing, and dot pattern.
    You can either enter the values manually or choose a preset resolution and aspect ratio.
    
Arguments:
    - image_width: the width of the image in pixels (integer).
    - image_height: the height of the image in pixels (integer).
    - dot_radius: the radius of the dots in pixels (integer).
    - dot_spacing: the distance between the centers of adjacent dots in pixels (integer).
    - dot_pattern: the pattern to use when placing the dots (string).
        - 'grid' or 'g': places dots in a grid pattern.
        - 'random' or 'r': scatters dots randomly using Poisson disc sampling.

Returns:
    The function creates a black and white image with dots arranged in a grid or randomly scattered,
    based on the specified dimensions, dot size, dot spacing, and dot pattern.
    The image is displayed on the screen and saved to a file named "dotted_image_[width]x[height]_[radius]_[spacing]_[pattern].png",
    where [width], [height], [radius], [spacing], and [pattern] are replaced with the corresponding values specified by the user.

Functions:
    - generate_poisson_disc_samples: generates points randomly distributed with a minimum distance between them,
      using Poisson disc sampling algorithm.
    - create_dotted_image: creates a black and white image with dots arranged in a grid or randomly scattered,
      based on the specified dimensions, dot size, dot spacing, and dot pattern.
"""

import sys
from PIL import Image, ImageDraw
import math
import random

size_preset_list = {
    "hd": (1920, 1080),
    "2k": (2048, 1080), 
    "4k": (3840, 2160)
    }
aspect_preset_list = {
    "h": (0, 1),
    "v": (1, 0), 
    "s": (1, 1)
    }    

def generate_poisson_disc_samples(width, height, min_dist, max_attempts=30):
    # Set up grid
    cell_size = min_dist / math.sqrt(2)
    grid_width = math.ceil(width / cell_size)
    grid_height = math.ceil(height / cell_size)
    grid = [[None] * grid_width for _ in range(grid_height)]

    # Generate first sample
    samples = []
    first_sample = (random.uniform(0, width), random.uniform(0, height))
    samples.append(first_sample)
    grid[int(first_sample[1] / cell_size)][int(first_sample[0] / cell_size)] = first_sample

    # Generate additional samples using Poisson disc sampling
    active_samples = [first_sample]
    while active_samples:
        sample = random.choice(active_samples)
        found_valid_sample = False

        for i in range(max_attempts):
            angle = random.uniform(0, math.pi * 2)
            radius = random.uniform(min_dist, min_dist * 2)
            new_sample = (sample[0] + radius * math.cos(angle), sample[1] + radius * math.sin(angle))

            # Check if the new sample is within bounds
            if not (0 <= new_sample[0] < width and 0 <= new_sample[1] < height):
                continue

            # Check if the new sample is too close to any existing samples
            cell_x, cell_y = int(new_sample[0] / cell_size), int(new_sample[1] / cell_size)
            search_radius = min_dist / math.sqrt(2)
            for j in range(max(0, cell_x - 2), min(grid_width, cell_x + 3)):
                for k in range(max(0, cell_y - 2), min(grid_height, cell_y + 3)):
                    existing_sample = grid[k][j]
                    if existing_sample and math.dist(existing_sample, new_sample) < min_dist:
                        break
                else:
                    continue
                break
            else:
                found_valid_sample = True
                active_samples.append(new_sample)
                samples.append(new_sample)
                grid[cell_y][cell_x] = new_sample
                break

        if not found_valid_sample:
            active_samples.remove(sample)

    return samples

def create_dotted_image(width, height, dot_radius, dot_spacing, dot_pattern):
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    if dot_pattern.lower() in ('grid', 'g'):
        for i in range(int(dot_spacing/2), width, dot_spacing):
            for j in range(int(dot_spacing/2), height, dot_spacing):
                draw.ellipse((i - dot_radius, j - dot_radius, i + dot_radius, j + dot_radius), fill=(0, 0, 0))
    elif dot_pattern.lower() in ('random', 'r'):
        density = int(input("Enter dot density: "))
        for sample in generate_poisson_disc_samples(width, height, dot_spacing, density):
            x = sample[0]
            y = sample[1]
            draw.ellipse((x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius), fill=(0, 0, 0))
    else:
        print("Invalid dot pattern. Use 'grid' or 'hex'.")
        sys.exit(1)
    #image = image.resize((width, width), resample=Image.LANCZOS)
    image.show()
    image.save(f"dotted_image_{width}x{height}_{dot_radius}_{dot_spacing}_{dot_pattern}.png", 'PNG')
    
if __name__ == "__main__":
    while(True):
        if(input("Use presets? (y/n): ").lower() in ('y', 'yes')):
            print("Presets:")
            print(f"Sizes: {','.join(size_preset_list.keys())}")
            print(f"Aspects: {','.join(aspect_preset_list.keys())}")
            print("Example(s): 1080p Square: 'hd_s' | 4K Vertical: '4k_v'")
            preset_input = input("Enter preset: ").lower()
            preset_data = preset_input.split('_')
            size_preset = preset_data[0]
            aspect_preset = preset_data[1]
            if(size_preset in size_preset_list and aspect_preset in aspect_preset_list):
                image_width = size_preset_list[size_preset][aspect_preset_list[aspect_preset][0]]
                image_height = size_preset_list[size_preset][aspect_preset_list[aspect_preset][1]]
                print(f"Preset: {preset_input} | Resolution: {image_width}x{image_height}")
            else:
                print("ERROR: Invalid preset")
        else:
            image_width = int(input("Enter image width: "))
            image_height = int(input("Enter image height: "))
        dot_radius = int(input("Enter dot radius in px: "))
        dot_spacing = int(input("Enter dot spacing in px: "))
        dot_pattern = input("Enter dot pattern (grid or random): ")
        
        create_dotted_image(image_width, image_height, dot_radius, dot_spacing, dot_pattern)
        if(input("Generate another image? (y/n): ").lower() in ('n', 'no')):
            break;

