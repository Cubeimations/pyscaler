from logging import exception
import csv
from PIL import Image as image
import pygame
import shutil
import os
pygame.init()

script_dir = os.path.dirname(os.path.abspath(__file__))

def clear_file(url):
    for filename in os.listdir(url):
        file_path = os.path.join(url, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('load failed because: ', (file_path, e))

def convert(url, name):
    with image.open(url) as img:
        for i in range(img.n_frames):
            img.seek(i)
            frame = img.convert('RGBA')
            frame.save(os.path.join(script_dir, f'gif_assets/{name}_frame_{i}.png'))

def return_frames(url):
    with image.open(url) as img:
        frames = img.n_frames
        return frames


# assets = csv_read('objects.csv')
#
# for asset in assets:
#     if asset['filetype'] == 'gif':
#         convert(f'assets/{asset['img']}.{asset['filetype']}', asset['name'])