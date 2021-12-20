import pygame
import os
import random
import sys
import math
import neat

pygame.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("images/coyote", "coyoteRun1.png")),
           pygame.image.load(os.path.join("images/coyote", "coyoteRun2.png"))]
JUMPING = pygame.image.load(os.path.join("images/coyote", "coyoteJump.png"))
RATTLESNAKE = [pygame.image.load(os.path.join("images/obstacles", "rattlesnake1.png")),
                pygame.image.load(os.path.join("images/obstacles", "rattlesnake2.png"))]
BISON = [pygame.image.load(os.path.join("images/obstacles", "bison.png")),
         pygame.image.load(os.path.join("images/obstacles", "bison2.png"))]
TRACK = pygame.image.load(os.path.join("images/Mojave", "track.png"))
FOREGROUND = pygame.image.load(os.path.join("images/Mojave", "foreground.png"))
LAYER = pygame.image.load(os.path.join("images/Mojave", "layer.png"))
DUNES = pygame.image.load(os.path.join("images/Mojave", "dunes.png"))
SKIES = pygame.image.load(os.path.join("images/Mojave", "skies.png"))


FONT = pygame.font.Font('freesansbold.ttf', 20)

class Coyote:
    posX = 80
    posY = 450
    JUMP_VEL = 8.5

    def __init__(self, image=RUNNING[0]):
        self.image = image
        self.coyote_run = True
        self.coyote_jump = False
        self.jump_vel = self.JUMP_VEL
        self.step_index = 0
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.rect = pygame.Rect(self.posX+50, self.posY,
                                image.get_width()-80, image.get_height()-25)
    def update(self):
        if self.coyote_run:
            self.run()
        if self.coyote_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0
    def jump(self):
        self.image = JUMPING
        if self.coyote_jump:
            self.rect.y -= self.jump_vel * 5
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.coyote_jump = False
            self.coyote_run = True
            self.jump_vel = self.JUMP_VEL
    def run(self):
        self.image = RUNNING[self.step_index//5]
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.step_index += 1
    def draw(self, SCREEN):
        SCREEN.blit(self.image,(self.rect.x,self.rect.y))
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height),2)
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x+175, self.rect.y+25), obstacle.rect.center, 2)
class Obstacle:
    def __init__(self, image, num_of_animals):
        self.image = image
        self.type = num_of_animals
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
    def update(self):
        self.rect.x -= (game_speed)
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    def draw(self, screen):
        SCREEN.blit(self.image[self.type], self.rect)
        
class Rattlesnake(Obstacle):
    def __init__(self, image, num_of_animals):
        super().__init__(image, num_of_animals)
        self.rect.y = 500
class Bison(Obstacle):
    def __init__(self, image, num_of_animals):
        super().__init__(image, num_of_animals)
        self.rect.y = 450
def remove(index):
    coyotes.pop(index)
    ge.pop(index)
    nets.pop(index)
def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

def eval_genomes(genomes, config):
    global game_speed, x_pos_bg,ge,nets,y_pos_bg,posX_foreground,posX_layer,posX_dunes,posX_skies,obstacles, coyotes, points
    clock = pygame.time.Clock()
    points = 0
    obstacles = []
    coyotes = []
    ge = []
    nets = []
    x_pos_bg = 0
    y_pos_bg = -45
    posX_foreground = 0
    posX_layer= 0
    posX_dunes = 0
    posX_skies = 0
    game_speed = 30

    for genome_id, genome in genomes:
        coyotes.append(Coyote())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    def statistics():
        global coyotes, game_speed, ge
        text_1 = FONT.render(f'Coyotes Alive: {str(len(coyotes))}', True, (0,0,0))
        text_2 = FONT.render(f'Generation: {pop.generation+1}', True, (0,0,0))
        text_3 = FONT.render(f'Game Speed: {str(game_speed)}', True, (0,0,0))
        SCREEN.blit(text_1, (10, 580))
        SCREEN.blit(text_2, (185, 580))
        SCREEN.blit(text_3, (340, 580))

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f'Distance Traveled: {str(points)}m', True, (0,0,0))
        SCREEN.blit(text,(510, 580))                           
    def background():
        global x_pos_bg, y_pos_bg, posX_foreground, posX_layer, posX_dunes, posX_skies
        image_width = TRACK.get_width()
##        SCREEN.blit(SKIES, (posX_skies, y_pos_bg))
##        SCREEN.blit(SKIES, (image_width + posX_skies, y_pos_bg))
        SCREEN.blit(DUNES, (posX_dunes, y_pos_bg+100))
        SCREEN.blit(DUNES, (image_width + posX_dunes, y_pos_bg+100))
        SCREEN.blit(LAYER, (posX_layer, y_pos_bg))
        SCREEN.blit(LAYER, (image_width + posX_layer, y_pos_bg))
        SCREEN.blit(FOREGROUND, (posX_foreground, y_pos_bg))
        SCREEN.blit(FOREGROUND, (image_width + posX_foreground, y_pos_bg))
        SCREEN.blit(TRACK, (x_pos_bg, y_pos_bg))
        SCREEN.blit(TRACK, (image_width + x_pos_bg, y_pos_bg))

        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= (game_speed//2)
        if posX_foreground <= -image_width+10:
            posX_foreground = 0
        posX_foreground -= (game_speed//6)
        if posX_layer <= -image_width:
            posX_layer = 0
        posX_layer -= (game_speed//8)
        if posX_dunes <= -image_width:
            posX_dunes = 0
        posX_dunes -= (game_speed//12)
        if posX_skies <= -image_width:
            posX_skies = 0
        posX_skies -= (game_speed//3)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        SCREEN.fill((173,216,230))
        background()
        for coyote in coyotes:
            coyote.update()
            coyote.draw(SCREEN)
        if len(coyotes) == 0:
            break
        if len(obstacles) == 0:
            rand_int = random.randint(0,1)
            if rand_int == 0:
                obstacles.append(Bison(BISON, random.randint(0,1)))
            elif rand_int ==1:
                obstacles.append(Rattlesnake(RATTLESNAKE, random.randint(0,1)))
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, coyote in enumerate(coyotes):
                if coyote.rect.colliderect(obstacle.rect):
                    ge[i].fitness -=1
                    remove(i)
                    ##run = False
                    ##pygame.quit()
                    ##sys.exit()
        for i, coyote in enumerate(coyotes):
            output = nets[i].activate((coyote.rect.y, distance((coyote.rect.x, coyote.rect.y),
                                                              obstacle.rect.midtop)))
            
            if output[0] > 0.5 and coyote.rect.y == coyote.posY:
                coyote.coyote_jump = True
                coyote.coyote_run = False
        statistics()
        score()
        clock.tick(30)
        pygame.display.update()
        
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path)
    pop = neat.Population(config)
    pop.run(eval_genomes, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__name__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)






    
    








