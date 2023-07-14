# Разработай свою игру в этом файле!
from pygame import *
import time as tm

class Wall(sprite.Sprite):
    def __init__(self, picture, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(Wall):
    def __init__(self, picture, x, y, width, height, x_speed, y_speed):
        Wall.__init__(self, picture, x, y, width, height)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.is_run = False
        self.right = True
        self.count = 0
        self.on_ground = False
        self.gravity = GRAVITY
        self.jump = 2
        self.rect_upr = self.rect.clip(Rect(self.rect.x, self.rect.y, width-30, height))
        self.rect_upl = self.rect.clip(Rect(self.rect.x+30, self.rect.y, width, height))
        self.image_runL = [
            transform.scale(image.load('run_left1.png'), (width, height)),
            transform.scale(image.load('run_left2.png'), (width, height)),
            transform.scale(image.load('run_left3.png'), (width, height)),
            transform.scale(image.load('run_left4.png'), (width, height)),
            transform.scale(image.load('run_left5.png'), (width, height)),
            transform.scale(image.load('run_left6.png'), (width, height)),
            transform.scale(image.load('run_left7.png'), (width, height)),
            transform.scale(image.load('run_left8.png'), (width, height)),
            transform.scale(image.load('run_left9.png'), (width, height)),
            transform.scale(image.load('run_left10.png'), (width, height)),
            transform.scale(image.load('run_left11.png'), (width, height)),
            transform.scale(image.load('run_left12.png'), (width, height)),
            transform.scale(image.load('run_left13.png'), (width, height)),
            transform.scale(image.load('run_left14.png'), (width, height)),
            transform.scale(image.load('run_left15.png'), (width, height)),
            transform.scale(image.load('run_left16.png'), (width, height))
        ]
        self.image_runR = [
            transform.scale(image.load('run_right1.png'), (width, height)),
            transform.scale(image.load('run_right2.png'), (width, height)),
            transform.scale(image.load('run_right3.png'), (width, height)),
            transform.scale(image.load('run_right4.png'), (width, height)),
            transform.scale(image.load('run_right5.png'), (width, height)),
            transform.scale(image.load('run_right6.png'), (width, height)),
            transform.scale(image.load('run_right7.png'), (width, height)),
            transform.scale(image.load('run_right8.png'), (width, height)),
            transform.scale(image.load('run_right9.png'), (width, height)),
            transform.scale(image.load('run_right10.png'), (width, height)),
            transform.scale(image.load('run_right11.png'), (width, height)),
            transform.scale(image.load('run_right12.png'), (width, height)),
            transform.scale(image.load('run_right13.png'), (width, height)),
            transform.scale(image.load('run_right14.png'), (width, height)),
            transform.scale(image.load('run_right15.png'), (width, height)),
            transform.scale(image.load('run_right16.png'), (width, height))
        ]
    
    def collides_up(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        for p in platforms_touched:
            if self.x_speed > 0 and p.rect.collidepoint(self.rect.midright):
                self.rect.right = min(self.rect.right, p.rect.left)
            if self.x_speed < 0 and p.rect.collidepoint(self.rect.midleft):
                self.rect.left = max(self.rect.left, p.rect.right)
        if self.y_speed > 10:
            self.y_speed = 10
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        self.rect_upr = self.rect.clip(Rect(self.rect.x, self.rect.y, width-30, height))
        self.rect_upl = self.rect.clip(Rect(self.rect.x+30, self.rect.y, width, height))
        for p in platforms_touched:
            if p.rect.collidepoint(self.rect.midtop):
                self.y_speed = 10
            if ((p.rect.collidepoint(self.rect_upr.bottomleft) or p.rect.collidepoint(self.rect_upr.midbottom) or p.rect.collidepoint(self.rect_upr.bottomright)) and self.right) or ((p.rect.collidepoint(self.rect_upl.bottomleft) or p.rect.collidepoint(self.rect_upl.midbottom) or p.rect.collidepoint(self.rect_upl.bottomright)) and self.right == False):
                self.y_speed = 0
                self.gravity = 0
                self.on_ground = True
                self.jump = 2
                print(True)
            else:
                self.on_ground = False
                self.gravity = GRAVITY
                print(False)
    
            if self.y_speed > 0  and p.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
            if self.y_speed < 0  and p.rect.collidepoint(self.rect.midtop):
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def update(self):
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
                self.image = transform.scale(image.load('stay_right.png'), (width, height))
                self.count = 0
            elif self.x_speed == 0 and self.right == False:
                self.image = transform.scale(image.load('stay_left.png'), (width, height))
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

class Enemy(Wall):
    def __init__(self, picture, x, y, width, height, x_speed, y_speed, direction_x, direction_y):
        Wall.__init__(self, picture, x, y, width, height)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        platforms_touched = tuple(sprite.spritecollide(self, barriers, False))
        if sprite.spritecollideany(self, platforms_touched):
            for p in platforms_touched:
                if self.rect.bottom < p.rect.top:
                    self.up = True
                if self.rect.top > p.rect.bottom:
                    self.down = True
                if self.rect.left < p.rect.right:
                    self.right = True
                if self.rect.right > p.rect.left:
                    self.left = True
        if self.up or self.rect.y > 760:
            self.direction_y = 'up'
        elif self.down or self.rect.y < 0:
            self.direction_y = 'down'
        elif self.right or self.rect.x > 1160:
            self.direction_x = 'left'
        elif self.right or self.rect.x < 0:
            self.direction_x = 'right'
        if self.direction_y == 'down':
            self.rect.y += self.y_speed
        else:
            self.rect.y -= self.y_speed
        if self.direction_x == 'right':
            self.rect.x += self.x_speed
        else:
            self.rect.x -= self.x_speed


screen = display.set_mode((1200, 800))
display.set_caption('Лабиринт')

win = transform.scale(image.load('winn.jpg'), (1200, 800))
lose = transform.scale(image.load('lose.jpg'), (1200, 800))
background = transform.scale(image.load('stone-texture.jpg'), (1200, 800))

barriers = sprite.Group()
platforms = []
wall_1 = Wall('icon_w.png', 0, 100, 190, 50)
barriers.add(wall_1)
platforms.append(wall_1)
#wall_2 = Wall('icon_w_v.png', 144, 144, 50, 200)
#barriers.add(wall_2)
#wall_3 = Wall('icon_w_v.png', 144, 344, 50, 200)
#barriers.add(wall_3)
wall_4 = Wall('icon_w.png', 0, 755, 200, 50)
barriers.add(wall_4)
platforms.append(wall_4)
wall_5 = Wall('icon_w.png', 200, 755, 200, 50)
barriers.add(wall_5)
platforms.append(wall_5)
#wall_6 = Wall('icon_w_v.png', 355, 582, 50, 180)
#barriers.add(wall_6)
#wall_7 = Wall('icon_w_v.png', 361, 0, 50, 200)
#barriers.add(wall_7)
#wall_8 = Wall('icon_w_v.png', 361, 200, 50, 200)
#barriers.add(wall_8)
wall_9 = Wall('icon_w.png', 361, 539, 200, 50)
barriers.add(wall_9)
platforms.append(wall_9)
wall_10 = Wall('icon_w.png', 561, 539, 200, 50)
barriers.add(wall_10)
platforms.append(wall_10)
wall_11 = Wall('icon_w.png', 761, 539, 200, 50)
barriers.add(wall_11)
platforms.append(wall_11)
#wall_12 = Wall('icon_w_v.png', 916, 335, 50, 210)
#barriers.add(wall_12)
#wall_13 = Wall('icon_w_v.png', 916, 125, 50, 210)
#barriers.add(wall_13)
wall_14 = Wall('icon_w.png', 761, 119, 200, 50)
barriers.add(wall_14)
platforms.append(wall_14)
wall_15 = Wall('icon_w.png', 611, 119, 150, 50)
barriers.add(wall_15)
platforms.append(wall_15)
#wall_16 = Wall('icon_w_v.png', 605, 163, 50, 200)
#barriers.add(wall_16)
wall_17 = Wall('icon_w.png', 527, 356, 200, 50)
barriers.add(wall_17)
platforms.append(wall_17)
#wall_18 = Wall('icon_w_v.png', 483, 260, 50, 200)
#barriers.add(wall_18)
#wall_19 = Wall('icon_w_v.png', 721, 260, 50, 200)
#barriers.add(wall_19)
#wall_20 = Wall('icon_w_v.png', 483, 0, 50, 160)
#barriers.add(wall_20)
#wall_21 = Wall('icon_w_v.png', 255, 144, 50, 200)
#barriers.add(wall_21)
#wall_22 = Wall('icon_w_v.png', 255, 344, 50, 202)
#barriers.add(wall_22)
wall_23 = Wall('icon_w.png', 261, 539, 100, 50)
barriers.add(wall_23)
platforms.append(wall_23)
wall_24 = Wall('icon_w.png', 400, 755, 200, 50)
barriers.add(wall_24)
platforms.append(wall_24)
wall_25 = Wall('icon_w.png', 600, 755, 200, 50)
barriers.add(wall_25)
platforms.append(wall_25)
wall_26 = Wall('icon_w.png', 800, 755, 200, 50)
barriers.add(wall_26)
platforms.append(wall_26)
wall_27 = Wall('icon_w.png', 1000, 755, 200, 50)
barriers.add(wall_27)
platforms.append(wall_27)
#wall_28 = Wall('icon_w_v.png', 1056, 335, 50, 210)
#barriers.add(wall_28)
#wall_29 = Wall('icon_w_v.png', 1056, 125, 50, 210)
#barriers.add(wall_29)
#wall_30 = Wall('icon_w_v.png', 1056, 545, 50, 218)
#barriers.add(wall_30)


dangerous = sprite.Group()
#enemy_1 = Enemy('wolf_1.png', 400, 470, 50, 60, 5, 5, 'left', 'up')

final_sprite = Wall('ancient_artifact.png', 410, 600, 50, 50)

width = 70
height = 70
SPEED = 10
GRAVITY = 0.5
player = Player('stay_right.png', 10, 650, width, height, 0, 0)

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
        print(player.rect_upr)
        print(player.rect_upl)
        print(player.on_ground, player.gravity)
        screen.blit(background, (0, 0))
        barriers.draw(screen)
        player.reset()
        player.update()
        final_sprite.reset()
        #enemy_1.reset()
        #enemy_1.update()
        display.update()
        '''if sprite.collide_rect(player, final_sprite):
            finish = True
            screen.blit(win, (0, 0))
            display.update()
            tm.sleep(3)
            finish = False'''