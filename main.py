from math import sqrt
from statistics import mean
from PIL import Image
import os
import numpy

INPUT_FOLDER = 'input'
TILE_FOLDER = 'Ney'
OUTPUT_FOLDER = 'output'
PACK_SIZE = 77

tiles_value = []
for i in range(PACK_SIZE):
    tile = Image.open(os.path.join( TILE_FOLDER, f'{i}.jpg'))
    tile_size = tile.size
    tile_value = [0, 0, 0]
    
    for x in range(tile_size[0]):
        for y in range(tile_size[1]):
            pixel = tile.getpixel((x, y))
            tile_value[0] += pixel[0]
            tile_value[1] += pixel[1]
            tile_value[2] += pixel[2]

    tile_value[0] //= tile_size[0]**2
    tile_value[1] //= tile_size[0]**2
    tile_value[2] //= tile_size[0]**2
    tiles_value.append(tile_value)

def in_path(filename, diretorio=INPUT_FOLDER):
    return os.path.join(diretorio, filename)

def color_dis(color1, color2):
    dis = sqrt((color1[0]-color2[0])**2+(color1[1]-color2[1])**2+(color1[2]-color2[2])**2)
    return dis

def resize(img, size):
    img_arr = numpy.asarray(img)
    new_img_arr = numpy.array(Image.fromarray(img_arr).resize((size[0], size[1]), Image.ANTIALIAS))
    resized_img = Image.fromarray(numpy.uint8(new_img_arr)).convert('RGB')
    return resized_img

def select_tile(color):
    selected_tile = [255, 0]
    for i in range(PACK_SIZE):
        tile_fit = color_dis(color, tiles_value[i])
        selected_tile = [tile_fit, i] if tile_fit < selected_tile[0] else selected_tile
        if selected_tile[0] == 0:
            return i
    return selected_tile[1]

def get_tunes(img, square_size=64):
    new_w, new_h = img.size

    resized_img = resize(img, (new_w//4, new_h//4))
    w, h = resized_img.size
    new_image = Image.new('RGB', (w*square_size, h*square_size))

    for xs in range(w):
        for ys in range(h):

            tile_i = select_tile(resized_img.getpixel((xs, ys)))
            tile = Image.open(in_path(f'{tile_i}.jpg', TILE_FOLDER))
            tile = resize(tile, (square_size, square_size))

            for x in range(tile.size[0]):
                for y in range(tile.size[1]):
                    new_image.putpixel((xs*square_size+x, ys*square_size+y), tile.getpixel((x, y)))

    return new_image

if __name__ == '__main__':
    input = 'beiço.jpeg'
    img = Image.open(in_path(input))
    new_img = get_tunes(img)
    new_img.save(in_path(f'{input}', OUTPUT_FOLDER))