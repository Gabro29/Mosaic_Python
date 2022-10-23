from PIL import Image
from scipy import spatial
import numpy as np
import os

# Source and settings
main_photo_to_pixelate = "image.jpg"
photos_to_compose = r"tiles_path"
photos_size = (40, 20)
output_photo = r"output_dir_path"


# Get all the photos to compose the mosaic
tiles = list()
colors = list()
for file_name in sorted(os.listdir(photos_to_compose)):
    if file_name.endswith('.png'):
        file_path = os.path.join(photos_to_compose, file_name)
        tile = Image.open(file_path)
        tile = tile.resize(photos_size)
        tiles.append(tile)
        mean_color = np.array(tile).mean(axis=0).mean(axis=0)
        colors.append(mean_color)

# Pixelate main photo
main_photo = Image.open(main_photo_to_pixelate)
width = int(np.round(main_photo.size[0]) / photos_size[0])
height = int(np.round(main_photo.size[1]) / photos_size[1])
resized_photo = main_photo.resize((width, height))

# Find the nearest photos for every pixel of the main_photo_to_pixelate
# base on the color
tree = spatial.KDTree(colors)
nearest_photos = np.zeros((width, height), dtype=np.uint32)

for i in range(width):
    for j in range(height):
        nearest = tree.query(resized_photo.getpixel((i, j)))
        nearest_photos[i, j] = nearest[1]

# Create an output image
output = Image.new('RGB', main_photo.size)

# Draw every little photos to make the mosaic
for i in range(width):
    for j in range(height):
        x, y = i * photos_size[0], j * photos_size[1]
        index = nearest_photos[i, j]
        output.paste(tiles[index], (x, y))

# Save Mosaic
output.save(fr'{output_photo}\mosaic.png')
