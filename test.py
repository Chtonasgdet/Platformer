import os, pygame, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.count = 0
    def upd(self):
        self.mask = pygame.mask.from_surface(self.image)

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((900, 900))
size = window.get_size()

images = ['run_left3.png', 'run_left7.png']
object_surf = pygame.image.load(images[1]).convert_alpha()
obstacle_surf = pygame.image.load('wizzard_11.png').convert_alpha()

moving_object = SpriteObject(0, 0, object_surf)
obstacle = SpriteObject(size[0] // 2, size[1] // 2, obstacle_surf)
all_sprites = pygame.sprite.Group([moving_object, obstacle])

start = time.time()
flag = True
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    new = time.time()
    if new - start > 10 and flag:
        moving_object.image = pygame.image.load(images[0]).convert_alpha()
        flag = False
    moving_object.rect.center = pygame.mouse.get_pos()
    collide = pygame.sprite.collide_mask(moving_object, obstacle)
    moving_object.upd()
    window.fill((255, 0, 0) if collide else (0, 0, 64))
    all_sprites.draw(window)
    pygame.display.update()

pygame.quit()
exit()