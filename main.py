import pygame, sys, os
from pygame.locals import *

#Game Initialization
pygame.init()

#Center the Game Application
os.environ['SDL_VIDEO_CENTERED']='1'

# Game Resolution
screen_width=800
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))

# Color
black=(0, 0, 0)
white=(255, 255, 255)

# Fonts
font="Gamer.ttf"

# Framerate
clock=pygame.time.Clock()
fps=30


# Image Files
image=pygame.image.load("sheet1.png")
imageSize=image.get_size()
horiz_cell=5
vert_cell=4
cell_width=imageSize[0]/horiz_cell
cell_height=imageSize[1]/vert_cell

cell_list=[]

cell_position=0

for y in range(0, imageSize[1], int(cell_height)):
    for x in range(0, imageSize[0], int(cell_width)):
        surface = pygame.Surface((cell_width, cell_height))
        surface.blit(image, (0, 0),
                     (x, y, cell_width, cell_height))
        cell_list.append(surface)
# Methods
def text_format(text, textFont, textSize, textColor):
    font=pygame.font.Font(textFont, textSize)
    newText=font.render(text, 0, textColor)
    return newText

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    if cell_position < len(cell_list)-5:
        cell_position+=1
    else:
        cell_position=0
    title=text_format("Python - Pygame Simple SpriteSheet Animation", font, 40, white)
    titleRect=title.get_rect()
    screen.blit(title, (screen_width/2 - (titleRect[2]/2), 50))
    screen.blit(pygame.transform.scale(cell_list[cell_position], (100, 100)), (300, 200))
    pygame.display.update()
    pygame.display.set_caption("Python - Pygame Simple SpriteSheet Animation")
    clock.tick(fps)

