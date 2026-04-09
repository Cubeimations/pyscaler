import csv
import pygame
import numpy as np
import random
import os
from formatter import *
from sigfig import round as siground
from constants import *
import pygame.freetype
import gifconvert as convert

script_dir = os.path.dirname(os.path.abspath(__file__))
convert.clear_file(os.path.join(script_dir, 'gif_assets'))
pygame.init()

rockwell_font = pygame.freetype.Font(os.path.join(script_dir, 'fonts/RockwellNova.ttf'), 20)

#slider i stole from one of my previous projects lol
class slider:
    def __init__(self, pos: tuple, size:tuple, initial_val: float, min_x, max_x, slider_width, max_speed):
        self.pos = pos
        self.size = size
        self.slider_width = slider_width

        self.slider_left = int(self.pos[0] - (size[0]//2))
        self.slider_right = int(self.pos[0] + (size[0]//2))
        self.slider_top = self.pos[1] - (size[1]//2)
        self.min = min_x
        self.max = max_x
        self.initial_val = (self.slider_right-self.slider_left)*initial_val # percentage
        self.max_speed = max_speed

        self.container_rect = pygame.Rect(self.slider_left, self.slider_top, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left + self.initial_val - 20, self.slider_top, self.slider_width, self.size[1])
    def move_slider(self, mouse_pos):
        target = mouse_pos[0]

        target = max(self.slider_left, min(target, self.slider_right))

        current = self.button_rect.centerx
        diff = target - current # calculate rate of change

        if diff < self.max_speed *-1:
            diff = self.max_speed *-1
        elif diff > self.max_speed:
            diff = self.max_speed

        self.button_rect.centerx += diff

    def render(self, screen, front_col, back_col):
        pygame.draw.rect(screen, back_col, self.container_rect, width = 0, border_radius = 5)
        pygame.draw.rect(screen, front_col, self.button_rect)
    def get_value(self):
        val_range = self.slider_right - self.slider_left - 2
        button_val = self.button_rect.centerx - self.slider_left
        return_val = (button_val/val_range)*(self.max-self.min)+self.min
        
        if return_val < self.max:
            return return_val
        else:
            return self.max

    def set_value(self, value):
        value = max(self.min, min(value, self.max))
        val_range = self.slider_right - self.slider_left - 2
        percent = (value - self.min) / (self.max - self.min)
        self.button_rect.centerx = self.slider_left + percent * val_range
        


def font(font, size, pos, contents, colour):
    my_font = pygame.font.SysFont(font, size)
    text_surface = my_font.render(contents, True, colour)

    text_rect = text_surface.get_rect()
    text_rect.midtop = pos
    window.blit(text_surface, text_rect)

class Circle:
    radius = 200
    line_density = 25
    font_divide = 7
    
    def __init__(self, color, scale, text: str, unit:str):
        self.x = window_width / 2 
        self.y = window_height / 2
        self.color = color
        self.scale = scale
        self.text = text
        self.unit = unit

    def draw(self, surface, sf):
        radius = int(Circle.radius * (10**(self.scale-sf)))
        if 2 < radius < 2000:   # keep drawable range

            pygame.draw.circle(surface, self.color, (self.x, self.y), radius, round(radius/Circle.line_density)+1)

            # scale to metre text
            text_size = round(radius / (Circle.font_divide + 3)+1)
            len_scale = f'10^{self.scale} metres'
            text_rect = rockwell_font.get_rect(len_scale, size=text_size)
            centered_x = self.x - (text_rect.width / 2)
            centred_y = self.y - radius - (radius/7)
            rockwell_font.render_to(window, (centered_x,centred_y), len_scale, fgcolor=self.color, size=text_size)

            # unit text
            text_size = round(radius / (Circle.font_divide - 2) + 1)
            len_scale = self.unit
            text_rect = rockwell_font.get_rect(len_scale, size=text_size)
            centered_x = self.x - (text_rect.width / 2)
            centred_y = self.y + radius*1.05
            rockwell_font.render_to(window, (centered_x, centred_y), len_scale, fgcolor=self.color, size=text_size)

            # top text
            text_size = round(radius/Circle.font_divide)+1
            len_scale = self.text
            text_rect = rockwell_font.get_rect(len_scale, size=text_size)
            centered_x = self.x - (text_rect.width / 2)
            centred_y = self.y - radius - (radius/3)
            rockwell_font.render_to(window, (centered_x, centred_y), len_scale, fgcolor=self.color, size=text_size)

circles = [
        Circle((80,100,120),0,f'1 metre','1m'),
        Circle((80,100,120),3,f'1 kilometre','1km'),
        Circle((80,100,120),6,f'1 megametre','1Mm'),
        Circle((80,100,120),9,f'1 gigametre','1Gm'),
        Circle((80,100,120),12,f'1 terametre','1Tm'),
        Circle((80,100,120),15,f'1 petametre','1Pm'),
        Circle((80,100,120),18,f'1 exametre','1Em'),
        Circle((80,100,120),21,f'1 zettametre','1Zm'),
        Circle((80,100,120),24,f'1 yottametre','1Ym'),
        Circle((80,100,120),-1,f'1 decimetre','1dm'),
        Circle((80,100,120),-2,f'1 centimetre','1cm'),
        Circle((80,100,120),-3,f'1 millimetre','1mm'),
        Circle((80,100,120),-6,f'1 micrometre','1μm'),
        Circle((80,100,120),-9,f'1 nanometre','1nm'),
        Circle((80,100,120),-12,f'1 picometre','1pm'),
        Circle((80,100,120),-15,f'1 femtometre','1fm'),
        Circle((80,100,120),-18,f'1 attometre','1am'),
        Circle((80,100,120),-21,f'1 zeptometre','1zm'),
        Circle((80,100,120),-24,f'1 yoctometre','1ym'),
        Circle((80,100,120),-27,f'1 rontometre','1rm'),
        Circle((80,100,120),-30,f'1 quectometre','1qm'),
        Circle((80,100,120),-31,f'0.1 quectometres','0.1qm'),
        Circle((80,100,120),-32,f'0.01 quectometres','0.01qm'),
        Circle((80,100,120),-33,f'0.001 quectometres','0.001qm'),
        Circle((80,100,120),-34,f'0.0001 quectometres','0.0001qm'),
    ]

#for i in range(scale_min,scale_max+1):
#    new_circle = Circle((80,100-i*3,100-i*4),i,f'10^{i} metres')
#    circles.append(new_circle)

class Object:
    default_size = 400
    def __init__(self, name, size, angle, img, title, desc, filetype, gif_speed):
        self.name = name
        self.size = float(size)
        self.scale = np.log10(self.size) #convert from metres to 10^x
        self.angle = float(angle)
        self.x = np.sin(np.radians(self.angle)) *window_width/window_height
        self.y = np.cos(np.radians(self.angle))
        self.offsetx = window_width / 2 
        self.offsety = window_height / 2
        self.img = img
        self.filetype = filetype
        real_size_m = 10 ** self.scale
        pixels_per_metre = ppm_sf0 * (10 ** -sf)
        self.length = int(real_size_m * pixels_per_metre)
        self.title = title
        self.desc = desc
        self.gif_speed = float(gif_speed)
        if self.filetype == 'gif':
            self.frames = convert.return_frames(os.path.join(script_dir, f'assets/{self.img}.gif'))
        elif self.filetype == 'png':
            self.frames = 1

        self.rect =  pygame.Rect(0,0,0,0)
        self.images = []

        if filetype == 'png':
            try:
                self.image = pygame.image.load(os.path.join(script_dir, f'assets/{self.img}.png')).convert_alpha()
            except:
                self.image = pygame.image.load(os.path.join(script_dir, f'assets/texture.png')).convert_alpha()

        elif filetype == 'gif':
            for i in range(0,self.frames):
                self.images.append(pygame.image.load(os.path.join(script_dir, f'gif_assets/{self.img}_frame_{i}.png')).convert_alpha())

    def draw(self, surface, sf, gif_frame, space):
        
        self.length = int(Object.default_size * (10**(self.scale-sf)))

        if self.length < 1000 and self.length > 1:
            
            if space:
                text_color = (250,250,250)
            else:
                text_color = (0,0,0)
            self.rect = pygame.Rect(0,0,self.length,self.length)
            self.rect.center = (self.x*self.length + self.offsetx,self.y*self.length + self.offsety)

            # font text
            my_font = pygame.font.SysFont('Rockwell', round(self.length/(6+len(self.name)/4)))
            text_surface = my_font.render(self.name, True, text_color)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (self.rect.centerx,self.rect.centery+self.length/2)

            if self.filetype == 'png':
                scaled_image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
                surface.blit(scaled_image,self.rect)
            elif self.filetype == 'gif':
                scaled_image = pygame.transform.scale(self.images[round(gif_frame/self.gif_speed)%self.frames], (self.rect.width, self.rect.height))
                surface.blit(scaled_image, self.rect)
            surface.blit(text_surface, text_rect)

    def print(self):
        print(self.title)
        print(self.desc)

def wrapping_text(surface, content, title, pos, scale, font, wrap):
    content_font = pygame.font.SysFont(font, 56-round(np.sqrt((len(str(title*3)))))) # bruh 5 ()s
    title_words = str(title).split()
    if len(title_words) > 2:
        title_surface1 = content_font.render(f'{title_words[0]} {title_words[1]}', True, (0, 0, 0))
        surface.blit(title_surface1, (pos[0] + 10, pos[1] + 30))
        try:
            title_surface2 = content_font.render(f'{title_words[2]} {title_words[3]}' + ':', True, (0, 0, 0))
            surface.blit(title_surface2, (pos[0] + 10, pos[1] + 80))
        except:
            title_surface2 = content_font.render(f'{title_words[2]}' + ':', True, (0, 0, 0))
            surface.blit(title_surface2, (pos[0] + 10, pos[1] + 80))
    else:
        title_surface = content_font.render(str(title)+':', True, (0,0,0))
        surface.blit(title_surface, (pos[0]+10,pos[1]+40))

    content_font = pygame.font.SysFont(font, 21)

    formatted_size = format(scale,'metre')
    title_surface = content_font.render(f'Size: {formatted_size}: (10^{round(np.log10(scale),3)}m)', True, (0, 0, 0))

    surface.blit(title_surface, (pos[0] + 10, pos[1] + 140))

    content_font = pygame.font.SysFont(font, 18)
    words = content.split()
    space = content_font.size(' ')[0]
    x,y = pos
    x += 10
    y += 200

    for lines in words:
        if lines != '/br':
            word_surface = content_font.render(lines, True, (0,0,0))
            word_width, word_height = word_surface.get_size()
            if x + word_width > wrap:
                x = pos[0] + 10
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        else:
            x = pos[0] + 10
            y += word_height


def csv_read(filename):
    mylist = []
    filepath = os.path.join(script_dir, filename)
    with open(filepath, 'r') as strings:
        csv_reader = csv.DictReader(strings, delimiter=',')

        for row in csv_reader:
            mylist.append(row)

        return(mylist)
scale_slider = slider((window_width/2,window_height/20*19), (window_width-40,50), abs(scale_min)/(scale_max-scale_min), scale_min, scale_max, 30, 3.5)
volume_slider = slider((window_width/5*4,window_height-bottom_slider_size-12), (window_width/4,20), volume, 0, 1, 15, 15)

objects = []

object_data = csv_read('objects.csv')

for item in object_data:
    if item['filetype'] == 'gif':
        convert.convert(os.path.join(script_dir, f'assets/{item['img']}.{item['filetype']}'), item['img'])
    obj = Object(**item)
    objects.append(obj)

pygame.mixer.music.load(os.path.join(script_dir, 'audio/music1.mp3'))
pygame.mixer.music.set_volume(volume)

stars = []
class Stars:
    def __init__(self,radius,scale,x,y,speed, intensity):
        self.radius = radius
        self.scale = scale
        self.x = x
        self.y = y
        self.grow = True
        self.speed = speed
        self.random = random.randint(1,25)
        self.intensity = intensity
        if self.radius > 20 and self.random <= 4: # coloured stars, negative colour mixing
            self.blue = 0
            self.green = 1
            self.red = 1
            self.speed /= 5
            self.intensity = min(self.intensity*2,1)
        elif self.radius > 20 and self.random <= 9:
            self.red = 0
            self.green = 1
            self.blue = 1
            self.speed /= 5
            self.intensity = min(self.intensity * 2, 1)
        elif self.radius > 20 and self.random == 10:
            self.red = 0
            self.green = 0
            self.blue = 1
            self.speed /= 5
            self.intensity = min(self.intensity * 2, 1)
        else:
            self.green = 0
            self.blue = 0
            self.red = 0

    def update(self):
        if self.scale < 1 and self.grow:
            self.scale += self.speed/FPS
        elif self.scale > 1:
            self.grow = False
            self.scale = 1
        elif self.scale <= 1:
            self.scale -= self.speed/FPS

        if self.scale < 0:
            self.scale = 0
            self.x = random.randint(0,window_width)
            self.y = random.randint(0,window_width)
            self.grow = True
            self.speed = random.random() * 2
            self.radius = random.randint(1,25)
            self.random = random.randint(1, 25)
            self.intensity = max(random.random(),0.2)
            if self.radius > 20 and self.random <= 4:  # coloured stars, negative colour mixing
                self.blue = 0
                self.green = 1
                self.red = 1
                self.speed /= 5
                self.intensity = min(self.intensity * 2, 1)
            elif self.radius > 20 and self.random <= 9:
                self.red = 0
                self.green = 1
                self.blue = 1
                self.speed /= 5
                self.intensity = min(self.intensity * 2, 1)
            elif self.radius > 20 and self.random == 10:
                self.red = 0
                self.green = 0
                self.blue = 1
                self.speed /= 5
                self.intensity = min(self.intensity * 2, 1)
            else:
                self.green = 0
                self.blue = 0
                self.red = 0

    def draw(self,surface,space):
        if space:
            for i in range(0,5):
                color_thing = 15+i*20
                red_star = max(round(max(color_thing - self.red*250,0)*self.intensity),20)
                green_star = max(round(max(color_thing - self.green *250, 0)*self.intensity),20)
                blue_star = max(round(max(color_thing - self.blue *250, 0)*self.intensity),20)
                if i != 0 or (self.intensity > 0.2 and i < 5):
                    pygame.draw.circle(surface, (red_star, green_star, blue_star), (self.x, self.y), round(self.radius * self.scale/(i+1)))
        else:
            pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), round(self.radius * self.scale))

for i in range(star_count):
    star_obj = Stars(random.randint(1,25), random.random(), random.randint(0,window_width),random.randint(0,window_height),random.random()*2,max(random.random(),0.2))
    stars.append(star_obj)
def main ():
    button_brightness = 0
    gif_frame = 0
    bg_offset = 0
    global desc_render
    global sf
    global smooth_sf
    global scale_slider_colliding
    looping = True
    zoom_target = None
    is_clicking = False
    menu_button = pygame.Rect(0,0,0,0)
    desc_rect = pygame.Rect(0,0,0,0)
    selected_scale = ''
    selected_title = ''
    selected_desc = ''
    was_clicking = False
    volume_changing = False
    volume_slider_colliding = False
    pygame.mixer.music.play(-1)
    while looping:
        gif_frame += 1 # gif animation speed
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        
        if mouse[0]:
            if not was_clicking:
                is_clicking = True
                was_clicking = True
            else:
                is_clicking = False
        else:
            was_clicking = False
            is_clicking = False
            
        # SMOOTH sf

        if zoom_target is not None:
                target_sf = zoom_target
                if abs(smooth_sf - zoom_target) < 0.01:
                    zoom_target = None
        else:
             target_sf = scale_slider.get_value()
        volume = volume_slider.get_value()
        for obj in objects:
            if obj.rect.collidepoint(mouse_pos) and mouse[0] and is_clicking and not scale_slider_colliding:
                 zoom_target = obj.scale + 0.35
                 scale_slider.set_value(obj.scale + 0.35)
                 selected_desc = obj.desc
                 selected_title = obj.title
                 selected_scale = obj.size
                 if obj.angle < 360 and obj.angle > 180:
                    desc_render = 'right'
                 elif obj.angle < 180:
                    desc_render = 'left'
        
        smooth_sf += (target_sf - smooth_sf) * slider_friction
        sf = smooth_sf

        if menu_button.collidepoint(mouse_pos):
            button_brightness = 30
            if mouse[0]:
                desc_render = 'none'
        else:
            button_brightness = 0

        if sf > 6:
            space = True
        else:
            space = False

        if space:
            if bg_offset < 230:
                bg_offset += 3
        else:
            if bg_offset > 0:
                bg_offset -= 3

        #render
        window.fill((BACKGROUND[0]-bg_offset,BACKGROUND[1]-bg_offset,BACKGROUND[2]-bg_offset))

        #render stars
        for star in stars:
            star.update()
            star.draw(window,space)

        # render circles
        for circ in circles:
            circ.draw(window, sf)

        # render objects
        for obj in objects:
            obj.draw(window, sf, gif_frame, space)

        # render descriptions

        if desc_render == 'left':
            menu_button = pygame.Rect(430,30,80,80)
            desc_rect = pygame.Rect(0,0,round(window_width/5*2),window_height)

            pygame.draw.rect(window, (120, 110, 120), (0, 0, round(window_width / 5 * 2)+5, window_height))
            pygame.draw.rect(window, (220,220,190), desc_rect)
            pygame.draw.rect(window, (255, 120+button_brightness, 90+button_brightness), menu_button, border_radius=12)

            padding = 18
            pygame.draw.line(window, (255, 255, 255),
                             (menu_button.left + padding, menu_button.top + padding),
                             (menu_button.right - padding, menu_button.bottom - padding), 10)
            pygame.draw.line(window, (255, 255, 255),
                             (menu_button.right - padding, menu_button.top + padding),
                             (menu_button.left + padding, menu_button.bottom - padding), 10)

            wrapping_text(window, selected_desc, selected_title, (12,10), selected_scale, "Aller", 470)
        elif desc_render == 'right':
            menu_button = pygame.Rect(window_width-550, 30, 80, 80)
            desc_rect = pygame.Rect(window_width-round(window_width/5*2), 0, round(window_width/5*2), window_height)

            pygame.draw.rect(window, (120, 110, 120),
                             (window_width - round(window_width / 5 * 2)-5, 0, round(window_width / 5 * 2),window_height))
            pygame.draw.rect(window, (220, 220, 190), desc_rect)
            wrapping_text(window, selected_desc, selected_title, (round(window_width / 5 * 3)+17, 10), selected_scale, "Aller", window_width-15)
            pygame.draw.rect(window, (255, 120+button_brightness, 90+button_brightness), menu_button, border_radius=12)

            padding = 18
            pygame.draw.line(window, (255, 255, 255),
                             (menu_button.left + padding, menu_button.top + padding),
                             (menu_button.right - padding, menu_button.bottom - padding), 10)
            pygame.draw.line(window, (255, 255, 255),
                             (menu_button.right - padding, menu_button.top + padding),
                             (menu_button.left + padding, menu_button.bottom - padding), 10)

        # if this works, it works, not touching it.
        obj_colliding = False
        if is_clicking and not desc_rect.collidepoint(mouse_pos) and zoom_target is None:
            for obj in objects:
                if obj.rect.collidepoint(mouse_pos):
                    obj_colliding = True
            if obj_colliding == False:
                desc_render = 'None'

        # render boxes
        pygame.draw.rect(window, (210, 200, 210), (0,0,window_width,10))
        pygame.draw.rect(window, (210, 200, 210), (window_width-10, 0, 10, window_height))
        pygame.draw.rect(window, (210, 200, 210), (0, 0, 10, window_height))
        pygame.draw.rect(window, (210, 200, 210), (0, window_height-100, window_width,10))

        rect_count = 0
        for rect in bg_rects:
            rect_count += bottom_slider_size/bg_count
            round_rect_count = round(rect_count)
            pygame.draw.rect(window,(240-round_rect_count,190-round_rect_count,220-round_rect_count), rect)


        # render sliders
        if scale_slider.container_rect.collidepoint(mouse_pos) and mouse[0]:
            scale_slider.move_slider(mouse_pos) 
            scale_slider_colliding = True 
        elif scale_slider_colliding and mouse[0]:
            scale_slider.move_slider(mouse_pos) 
        else:
            scale_slider_colliding = False

        if volume_slider.container_rect.collidepoint(mouse_pos) and mouse[0] and not scale_slider_colliding:
            volume_slider.move_slider(mouse_pos)
            volume_slider_colliding = True
        elif volume_slider_colliding and mouse[0]:
            volume_slider.move_slider(mouse_pos)
        else:
            volume_slider_colliding = False

        if volume_slider_colliding:
            pygame.mixer.music.set_volume(volume)
        scale_slider.render(window,'red','black')
        volume_slider.render(window, 'blue', 'grey')

        # font
        font( 'Rockwell', 20, (220,window_height/8*7), f'Scale: 10^{round(sf,2)} metres', (255,0,0))
        font('Rockwell', 16, (window_width-220, window_height / 5 * 4), f'Volume: {round(volume*100)}%', (5, 5, 200))
        # events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.MOUSEWHEEL:
                if scale_slider.button_rect.centerx <= scale_slider.slider_right:
                    target_sf = event.y * 0.2
                    scale_slider.set_value(sf+target_sf)
                else:
                    scale_slider.button_rect.centerx = scale_slider.slider_right

                if scale_slider.button_rect.centerx >= scale_slider.slider_left:
                    target_sf = event.y * 0.2
                    scale_slider.set_value(sf+target_sf)
                else:
                    scale_slider.button_rect.centerx = scale_slider.slider_left

        # fps
        fps = clock.get_fps()
        font('Rockwell', 12, (window_width-60, window_height-140), f'fps: {round(fps)}',(5, 5, 200))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    convert.clear_file(os.path.join(script_dir, 'gif_assets'))

 
main()
