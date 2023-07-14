import time as tm
from pygame import *

class Static_objects(sprite.Sprite):
    def __init__(self, picture, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(picture).convert_alpha(), (width, height))
        self.rect = self.image.get_rect(center = (x, y))
        self.mask = mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Moving_objects(Static_objects):
    def __init__(self, picture, x, y, width, height, x_speed, y_speed):
        Static_objects.__init__(self, picture, x, y, width, height)
        self.x_speed = x_speed
        self.y_speed = y_speed

class Player(Moving_objects):
    def __init__(self, picture, x, y, width, height, x_speed, y_speed):
        Moving_objects.__init__(self, picture, x, y, width, height, x_speed, y_speed)
        self.is_run = False
        self.right = True
        self.count = 0
        self.on_ground = False
        self.gravity = GRAVITY
        self.jump = 2
        self.col = False
        self.image_runL = [
            transform.scale(image.load('run_left1.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left2.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left3.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left4.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left5.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left6.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left7.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left8.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left9.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left10.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left11.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left12.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left13.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left14.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left15.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_left16.png').convert_alpha(), (width, height))
        ]
        self.image_runR = [
            transform.scale(image.load('run_right1.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right2.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right3.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right4.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right5.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right6.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right7.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right8.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right9.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right10.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right11.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right12.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right13.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right14.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right15.png').convert_alpha(), (width, height)),
            transform.scale(image.load('run_right16.png').convert_alpha(), (width, height))
        ]
    
    def collides_up(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if platforms_touched != []:
            for p in platforms_touched:
                if sprite.collide_mask(self, p):
                    self.col = True
                    if self.x_speed > 0 and p.rect.collidepoint(self.rect.midright):
                        self.rect.right = min(self.rect.right, p.rect.left)
                    if self.x_speed < 0 and p.rect.collidepoint(self.rect.midleft):
                        self.rect.left = max(self.rect.left, p.rect.right)
        if self.y_speed > 10:
            self.y_speed = 10
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if platforms_touched != []:
            for p in platforms_touched:
                if sprite.collide_mask(self, p):
                    self.col = True
                    if p.rect.collidepoint(self.rect.topleft) or p.rect.collidepoint(self.rect.midtop) or p.rect.collidepoint(self.rect.topright):
                        self.y_speed = 10
                #if ((p.rect.collidepoint(self.rect_upr.bottomleft) or p.rect.collidepoint(self.rect_upr.midbottom) or p.rect.collidepoint(self.rect_upr.bottomright)) and self.right) or ((p.rect.collidepoint(self.rect_upl.bottomleft) or p.rect.collidepoint(self.rect_upl.midbottom) or p.rect.collidepoint(self.rect_upl.bottomright)) and self.right == False):
                    if p.rect.collidepoint(self.rect.bottomleft) or p.rect.collidepoint(self.rect.midbottom) or p.rect.collidepoint(self.rect.bottomright):
                        self.y_speed = 0
                        self.gravity = 0
                        self.on_ground = True
                        self.jump = 2
            
                    if self.y_speed > 0  and p.rect.collidepoint(self.rect.midbottom):
                        self.rect.bottom = min(self.rect.bottom, p.rect.top)+30
                    if self.y_speed < 0  and p.rect.collidepoint(self.rect.midtop):
                        self.rect.top = max(self.rect.top, p.rect.bottom)
        else:
            self.col = False
            self.on_ground = False
            self.gravity = GRAVITY

    def update(self):
        self.mask = mask.from_surface(self.image)
        self.collides_up()
        self.screen_borders()
        if self.on_ground == False:
            self.y_speed += self.gravity
        else:
            if self.x_speed != 0 and self.right:
                self.image = self.image_runR[self.count]
                self.count += 1
                if self.count == len(self.image_runR):
                    self.count = 0
            elif self.x_speed != 0 and self.right == False:
                self.image = self.image_runL[self.count]
                self.count += 1
                if self.count == len(self.image_runL):
                    self.count = 0
            elif self.x_speed == 0 and self.right:
                self.image = transform.scale(image.load('stay_right.png').convert_alpha(), (width, height))
                self.count = 0
            elif self.x_speed == 0 and self.right == False:
                self.image = transform.scale(image.load('stay_left.png').convert_alpha(), (width, height))
                self.count = 0

    def screen_borders(self):
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 1160:
            self.rect.x = 1160
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > 730:
            self.rect.y = 730

init()
screen = display.set_mode((1200, 800))
display.set_caption('Лабиринт')

win = transform.scale(image.load('winn.jpg'), (1200, 800))
lose = transform.scale(image.load('lose.jpg'), (1200, 800))
background = transform.scale(image.load('stone-texture.jpg'), (1200, 800))

barriers = sprite.Group()
platforms = []
wall_1 = Static_objects('icon_w.png', 0, 100, 190, 50)
barriers.add(wall_1)
platforms.append(wall_1)
wall_4 = Static_objects('icon_w.png', 0, 755, 200, 50)
barriers.add(wall_4)
platforms.append(wall_4)
wall_5 = Static_objects('icon_w.png', 200, 755, 200, 50)
barriers.add(wall_5)
platforms.append(wall_5)
wall_9 = Static_objects('icon_w.png', 361, 539, 200, 50)
barriers.add(wall_9)
platforms.append(wall_9)
wall_10 = Static_objects('icon_w.png', 561, 539, 200, 50)
barriers.add(wall_10)
platforms.append(wall_10)
wall_11 = Static_objects('icon_w.png', 761, 539, 200, 50)
barriers.add(wall_11)
platforms.append(wall_11)
wall_14 = Static_objects('icon_w.png', 761, 119, 200, 50)
barriers.add(wall_14)
platforms.append(wall_14)
wall_15 = Static_objects('icon_w.png', 611, 119, 150, 50)
barriers.add(wall_15)
platforms.append(wall_15)
wall_17 = Static_objects('icon_w.png', 527, 356, 200, 50)
barriers.add(wall_17)
platforms.append(wall_17)
wall_23 = Static_objects('icon_w.png', 261, 539, 100, 50)
barriers.add(wall_23)
platforms.append(wall_23)
wall_24 = Static_objects('icon_w.png', 400, 755, 200, 50)
barriers.add(wall_24)
platforms.append(wall_24)
wall_25 = Static_objects('icon_w.png', 600, 755, 200, 50)
barriers.add(wall_25)
platforms.append(wall_25)
wall_26 = Static_objects('icon_w.png', 800, 755, 200, 50)
barriers.add(wall_26)
platforms.append(wall_26)
wall_27 = Static_objects('icon_w.png', 1000, 755, 200, 50)
barriers.add(wall_27)
platforms.append(wall_27)

#final_sprite = Wall('ancient_artifact.png', 410, 600, 50, 50)

width = 70
height = 70
SPEED = 10
GRAVITY = 0.5
player = Player('stay_right.png', 10, 690, width, height, 0, 0)

all_sprites = sprite.Group([platforms, player])
timer = time.Clock()
finish = False
play = True

while play:
    time.delay(60)
    for events in event.get():
        if events.type == QUIT:
            play = False
        if events.type == KEYDOWN:
            if events.key == K_UP and player.jump > 0:
                player.y_speed = -12
                player.on_ground = False
                player.gravity = GRAVITY
                player.jump -= 1
            if events.key == K_RIGHT:
                player.right = True
                player.x_speed = SPEED
            if events.key == K_LEFT:
                player.right = False
                player.x_speed = -SPEED
        elif events.type == KEYUP:
            if events.key == K_RIGHT:
                player.x_speed = 0
            if events.key == K_LEFT:
                player.x_speed = 0

    if finish != True:
        print(player.y_speed)
        print(player.rect)
        print(player.on_ground, player.gravity)
        #screen.blit(background, (0, 0))
        if player.col:
            screen.fill((255, 0, 0))
        else:
            screen.fill((0, 0, 64))
    
        all_sprites.draw(screen)
        player.update()
        #final_sprite.reset()
        display.update()
