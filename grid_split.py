import os
import cv2
import argparse

def split_image_into_tiles(image_path, rows, cols, output_dir):
    """
    This function splits an input image into a grid of tiles and saves each tile into a subdirectory.
    
    Parameters:
        image_path (str): The path to the input image.
        rows (int): The number of rows in the grid.
        cols (int): The number of columns in the grid.
        output_dir (str): The path to the directory where the tiles will be saved.
    """
    # Load the image
    image = cv2.imread(image_path)
    
    # Get the dimensions of the image
    height, width, _ = image.shape
    
    # Calculate the size of each tile
    tile_height = height // rows
    tile_width = width // cols
    
    # Loop over the rows and columns in the grid
    for row in range(rows):
        for col in range(cols):
            # Calculate the starting and ending row and column indices for the current tile
            start_row = row * tile_height
            end_row = start_row + tile_height
            start_col = col * tile_width
            end_col = start_col + tile_width
            
            # Extract the current tile from the image
            tile = image[start_row:end_row, start_col:end_col]
            
            # Save the current tile to disk
            tile_path = os.path.join(output_dir, f"tile_{row}_{col}.jpg")
            cv2.imwrite(tile_path, tile)

if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="Split an image into a grid of tiles")
    parser.add_argument("image_path", help="The path to the input image.")
    parser.add_argument("rows", type=int, help="The number of rows in the grid.")
    parser.add_argument("cols", type=int, help="The number of columns in the grid.")
    parser.add_argument("output_dir", help="The path to the directory where the tiles will be saved.")
    args = parser.parse_args()
    
    # Call the split_image_into_tiles function with the parsed arguments
    split_image_into_tiles(args.image_path, args.rows, args.cols, args.output_dir)
