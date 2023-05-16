# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
# Art from Kenney
import pygame
import random
from os import path
import time

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

largura = 480
altura = 600
fps = 90
powerup_time = 3000
# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Shmup')

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img_rot, (50,38))
        self.image.set_colorkey(black)
        self.radius = 19
        self.rect = self.image.get_rect()
        self.rect.centerx = largura / 2
        self.rect.bottom = altura - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 180
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = largura / 2
            self.rect.bottom = altura - 20
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.image = pygame.transform.scale(player_img_left, (50,38))
            self.image.set_colorkey(black)
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.image = pygame.transform.scale(player_img_right, (50, 38))
            self.image.set_colorkey(black)
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_KP_0]:
            self.shoot(score)
        if self.speedx == 0:
            self.image = pygame.transform.scale(player_img_rot, (50, 38))
            self.image.set_colorkey(black)
        self.rect.x +=self.speedx
        self.rect.y += self.speedy
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 50:
            self.rect.top = 50
        if self.rect.bottom > altura and self.rect.bottom < altura + 200:
            self.rect.bottom = altura
    def shoot(self, score):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                self.shoot_delay = 180
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                self.shoot_delay = 160
                bullet1 = Bullet(self.rect.left, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power == 3:
                self.shoot_delay = 140
                bullet1 = Bullet(self.rect.left, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet3)
                bullets.add(bullet3)
                shoot_sound.play()
            if self.power >= 4:
                self.shoot_delay = 100
                bullet1 = Bullet(self.rect.left, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet3)
                bullets.add(bullet3)
                shoot_sound.play()




    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.centerx = largura / 2
        self.rect.bottom = altura + 2000

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(largura - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center



    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > altura + 100 or self.rect.left < -100 or self.rect.right > largura + 250:
            self.rect.x = random.randrange(largura - self.rect.width)
            self.rect.y = random.randrange(-100, -90)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 22))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 20
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'gun', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > altura:
            self.kill()
font_name = pygame.font.match_font('arial')

def draw_ui():
    ui_bar = pygame.Rect(0, 0, largura, 30)
    pygame.draw.rect(screen, black, ui_bar)

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def newmob():
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

def draw_shield_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 13
    fill = (pct/100) * bar_length
    ouline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    if pct > 30:
        pygame.draw.rect(surface, green, fill_rect)
        pygame.draw.rect(surface, white, ouline_rect, 1)
    if pct <= 30:
        pygame.draw.rect(surface, red, fill_rect)
        pygame.draw.rect(surface, white, ouline_rect, 1)

def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)

def show_go_screen(score):
    screen.blit(background, background_rect)
    draw_text(screen, 'GAME OVER', 64, largura / 2, altura / 4)
    draw_text(screen, f'Your Final Score   {score}', 22, largura / 2, altura / 2)
    draw_text(screen, 'Press any key to Continue', 18, largura / 2, altura * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_start_screen():
    screen.blit(background_start, background_start_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_level_screen():
    screen.blit(background_levels, background_levels_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                    waiting = False

def show_level(level):
    screen.blit(background, background_rect)
    draw_text(screen, f'LEVEL {level}', 64, largura / 2, altura / 2)
    pygame.display.flip()
    time.sleep(2)

# load all game graphics
background = pygame.image.load(path.join(img_dir + '/bg.png')).convert()
background_rect = background.get_rect()
background_start = pygame.image.load(path.join(img_dir + '/bg_start.png')).convert()
background_start_rect = background_start.get_rect()
background_levels = pygame.image.load(path.join(img_dir + '/levels00.png')).convert()
background_levels_rect = background_levels.get_rect()


player_img = pygame.image.load(path.join(img_dir + '/player.png')).convert()
player_img_rot = pygame.transform.rotate(player_img, 0)
player_mini_img = pygame.transform.scale(player_img_rot, (25, 19))
player_img_right = pygame.image.load(path.join(img_dir + '/playerRight.png')).convert()
player_img_left = pygame.image.load(path.join(img_dir + '/playerLeft.png')).convert()
player_rect = player_img_rot.get_rect()

# creating a list of enermies images
meteor_img = pygame.image.load(path.join(img_dir, 'spaceMeteors_001.png')).convert()
meteor_small = pygame.transform.scale(meteor_img, (15, 15))
meteor_medium = pygame.transform.scale(meteor_img, (50, 50))
meteor_big = pygame.transform.scale(meteor_img, (80, 80))

meteor_images = [meteor_small, meteor_medium, meteor_big]

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(9):
    filename = f'regularExplosion0{i}.png'
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

for i in range(9):
    file_name = f'sonicExplosion0{i}.png'
    img = pygame.image.load(path.join(img_dir, file_name)).convert()
    img.set_colorkey(black)
    explosion_anim['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

bullet_img = pygame.image.load(path.join(img_dir + '/spaceMissiles_016.png')).convert()
bullet_rect = player_img.get_rect()


# load game sound
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot5.wav'))
expl_sound = pygame.mixer.Sound(path.join(snd_dir, 'Explosion.wav'))
points_sound = pygame.mixer.Sound(path.join(snd_dir, 'points.wav'))
hit_ship_sound = pygame.mixer.Sound(path.join(snd_dir, 'hit_ship.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'shield.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'power.wav'))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))

bg_music_list = {'level1': 'high-energy-loop-69158.mp3', 'level2': 'tgfcoder-FrozenJam-SeamlessLoop.mp3'}
value = random.choice(list(bg_music_list.values()))
pygame.mixer.music.load(path.join(snd_dir, value))
pygame.mixer.music.set_volume(0.8)
shoot_sound.set_volume(0.4)
expl_sound.set_volume(0.5)
hit_ship_sound.set_volume(0.6)
'''
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)'''


level = 1

pygame.mixer.music.play(loops=-1)

# game loop
count = 0
inicio = 0
game_over = True
running = True

while running:
    if count == 0:
        power = 1
        show_start_screen()
        level = show_level_screen()
        show_level(level)
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(level * 4):
            newmob()
        score = 0
        count = 2

    if count == 1:
        if game_over:
            show_go_screen(score)
            show_level(level)
            game_over = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            player = Player()
            player.power = 1
            all_sprites.add(player)
            for i in range(level * 4):
                newmob()
            score = 0
    if count == 3:
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        player.power = power
        for i in range(level * 4):
            newmob()
        count = 2
    if score >= level * 5000:
        power = player.power
        level += 1
        show_level(level)
        count = 3
        if level == 2:
            player.lives += 1
    # keep it running at the right speed
    clock.tick(fps)
    # input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_0:
                player.shoot(score)

    # update
    all_sprites.update()
    # CHECK IF BULLET HITS MOBS
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        if random.random() > 0.96:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        score += 50 - hit.radius
        hit_ship_sound.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
    # check to see if a mob hits a player
    # false means if the mobs are deleted after collision
    # it returns a list
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        player.shield -= hit.radius * 2
        expl_sound.play()
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player_die_sound.play()
            player.hide()
            player.lives -= 1
            player.shield = 100

    # if player hits power ups
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            power_sound.play()
            player.powerup()


            # running = False
    if player.lives == 0 and not death_explosion.alive():
        count = 1
        game_over = True

    # draw / render
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_ui()
    draw_text(screen, 'Points  ' + str(score), 18, largura / 2, 5)
    draw_text(screen, 'Shield', 18, 30, 5)
    draw_shield_bar(screen, 60, 9, player.shield)
    draw_lives(screen, largura - 100, 8, player.lives, player_mini_img)
    # do it after drawing everything
    pygame.display.flip()



pygame.quit()