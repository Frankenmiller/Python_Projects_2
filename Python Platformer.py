## Platformer SuperNES type game created from YouTube tutorial
## November 2021

import pygame
from pygame import image
from pygame.locals import *
import pickle
from os import path

pygame.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer created by dr_FRANKENMILLER©2021")
font_score = pygame.font.SysFont('Bauhaus 93', 30)
tile_size = 50
game_over = 0
main_menu = True
level = 1
max_levels = 3
score = 0
WHITE = (255,255,255)

background_image = pygame.image.load("images/game_functions/mountain_background.gif")
restart_image = pygame.image.load("images/game_functions/restart_button.gif")
start_image = pygame.image.load("images/game_functions/start_button.gif")
exit_image = pygame.image.load("images/game_functions/exit_button.gif")

##def draw_grid():
##    for line in range(16):
##        pygame.draw.line(screen, (255,255,255), (0, line*tile_size), (screen_width, line*tile_size))
##        pygame.draw.line(screen, (255,255,255), (line*tile_size,0), (line*tile_size, screen_height))

def draw_text(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))

def reset_level(level):
    Johnny.reset(50, 50) ##(40, 650)
    wolfpack_group.empty()
    water_pit_group.empty()
    exit_group.empty()
    if path.exists(f'levels/level{level}_data'):
        pickle_in = open(f'levels/level{level}_data', "rb")
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    return world

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0: ## one means clicked zero means released
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action
class Player():
    def __init__(self, x, y):
        self.reset(x,y)
    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        if game_over == 0:   
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -20
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:## == True:
                dx -= 2
                self.counter += 1
                self.direction = -1
            if key[pygame.K_LEFT] and key[pygame.K_LSHIFT]:
                dx -= 3
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 2
                self.counter += 1
                self.direction = 1
            if key[pygame.K_RIGHT] and key[pygame.K_LSHIFT]:
                dx += 3
                self.counter += 1
                self.direction = 1
            if key[pygame.K_RIGHT] == False and self.direction == 1:
                self.counter = 0
                self.index = 0
                self.image = self.images_right[self.index]
            if key[pygame.K_LEFT] == False and self.direction == -1:
                self.counter = 0
                self.index = 0
                self.image = self.images_left[self.index]
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            self.vel_y += 1
            if self.vel_y > 10: 
                self.vel_y = 10
            dy += self.vel_y
            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y+dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
            if pygame.sprite.spritecollide(self, wolfpack_group, False):
                game_over = -1 
                self.status = "mauled" 
            if pygame.sprite.spritecollide(self, water_pit_group, False):
                game_over = -1
                self.status = "drowned"
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1
## 3rd arguement here asks if want delete item that sprite has collided with      
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            if self.status == "mauled" and self.direction == 1:
                self.image = self.mauled_image
                self.rect.y = Johnny.rect.y
            elif self.status == "mauled" and self.direction == -1:
                self.image = pygame.transform.flip(self.mauled_image, True, False)
                self.rect.y = Johnny.rect.y
            elif self.status == "drowned" and self.direction == 1:
                self.image = self.drowned_image
                self.rect.y = Johnny.rect.y
            elif self.status == "drowned" and self.direction == -1:
                self.image = pygame.transform.flip(self.drowned_image, True, False)
        
        screen.blit(self.image, self.rect)
        ## pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            image_right = pygame.image.load(f"images/characters/miner_walk_right{num}.gif")
            image_right = pygame.transform.scale(image_right, (40, 80))
            image_left = pygame.transform.flip(image_right, True, False)
            ## flip() method parameters: image, x-axis T/F, y-axis T/F
            self.images_right.append(image_right)
            self.images_left.append(image_left)
        self.image = self.images_right[self.index]
        self.mauled_image = pygame.image.load("images/characters/mauled_miner.gif")
        self.drowned_image = pygame.image.load("images/characters/drowned_miner.gif")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.status = 'alive'
        self.in_air = True
    
class World():
    def __init__(self, data):
        self.tile_list = []
        dirt_image = pygame.image.load("images/blocks/dirt_block.gif")
        grass_on_dirt = pygame.image.load("images/blocks/dirt_grass_block.gif")
        dark_wood = pygame.image.load("images/blocks/dark_wooden_block.gif")
        light_wood = pygame.image.load("images/blocks/wooden_block.gif")
        water = pygame.image.load("images/blocks/water_block.gif")
        water_surface = pygame.image.load("images/blocks/water_surface.gif")
        miners_block = pygame.image.load("images/blocks/miner_stone.gif")
        coin = pygame.image.load("images/blocks/bitcoin_image.gif")
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    image = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    image = pygame.transform.scale(grass_on_dirt, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    wolf = Enemy(col_count * tile_size, row_count * tile_size+10)
                    wolfpack_group.add(wolf)
                if tile == 4: ### still needs be correctly assigned
                    image = pygame.transform.scale(light_wood, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 5: ### still needs be correctly assigned
                    image = pygame.transform.scale(dark_wood, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 6: 
                    image = pygame.transform.scale(water_surface, (tile_size, tile_size))
                    water_pit = Water(col_count * tile_size, row_count * tile_size)
                    water_pit_group.add(water_pit)
                if tile == 7: 
                    image = pygame.transform.scale(water, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 8:
                    image = pygame.transform.scale(miners_block, (tile_size, tile_size))
                    exit = Exit(col_count * tile_size, row_count * tile_size)
                    exit_group.add(exit)
                if tile == 24: 
                    coin = Coin(col_count*tile_size+tile_size//2, row_count*tile_size+tile_size//2)
                    coin_wallet_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            ## pygame.draw.rect(screen, (255,255,255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):##------------------------- Enemy Class --->
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/characters/hungry_wolf_left.gif")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = -1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        
class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("images/blocks/water_surface.gif")
        self.image = pygame.transform.scale(image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("images/blocks/bitcoin_image.gif")
        self.image = pygame.transform.scale(image, (tile_size//2, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("images/blocks/miner_stone.gif")
        self.image = pygame.transform.scale(image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

Johnny = Player(150, 650) ##------------------------------ Instantiations --->
wolfpack_group = pygame.sprite.Group()
water_pit_group = pygame.sprite.Group()
coin_wallet_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

score_coin = Coin(25, 775)
coin_wallet_group.add(score_coin)

if path.exists(f'levels/level{level}_data'):
    pickle_in = open(f'levels/level{level}_data', "rb")
    world_data = pickle.load(pickle_in)##-----------------------------Pickles--->
world = World(world_data)

restart_button = Button(screen_width -200, 25, restart_image)
start_button = Button(screen_width//2-350, screen_height//2, start_image)
exit_button = Button(screen_width//2-150, screen_height//2, exit_image)

run = True ##--------------------------------------------------Main Loop--->
while run == True:
    clock.tick(fps)
    
    screen.blit(background_image, (0,0))

    if main_menu == True:
        if exit_button.draw() == True:
            run =False
        if start_button.draw() == True:
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            wolfpack_group.update()
            if pygame.sprite.spritecollide(Johnny, coin_wallet_group, True):
                score += 1
            draw_text('X ' + str(score),font_score, WHITE, tile_size, 765)
    
        wolfpack_group.draw(screen)
        water_pit_group.draw(screen)
        exit_group.draw(screen)
        coin_wallet_group.draw(screen)
        ##draw_grid()
        game_over = Johnny.update(game_over)

        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                ## Johnny.reset(150,175) ##(40, 650)
                game_over = 0
                score = 0
        if game_over == 1:
            level += 1
            if level <= max_levels:
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()        

pygame.quit()
