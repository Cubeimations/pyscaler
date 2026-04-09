import pygame
import numpy as np
import os

# colours
BACKGROUND = (240, 240, 250)

# Game Setup
FPS = 60
clock = pygame.time.Clock()
window_width = 1200
window_height = 750
window_midpoint = (window_width/2,window_height/2)
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Scale Test')
script_dir = os.path.dirname(os.path.abspath(__file__))
programIcon = pygame.image.load(os.path.join(script_dir, 'assets/proton-icon.png'))
pygame.display.set_icon(programIcon)
sf = 0
ppm_sf0 = 100
bottom_slider_size =100
scale_min = -35
scale_max = 27
star_count = 550
bg_offset = 0
bg_rects = []

bg_count = 20
for i in range(1,bg_count):
    bg_rects.append(pygame.Rect(0,window_height-(bg_count-i)/bg_count * 100,window_width,100),)
desc_render = 'none'

scale_slider_colliding: bool = False
slider_friction = 0.14
smooth_sf = 0
volume = 0.5
space = False