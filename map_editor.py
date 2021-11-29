import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
tile_size = 50
cols = 16
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * cols) + 50

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


#load images
background_image = pygame.image.load("images/game_functions/mountain_background.gif")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height - margin))
dirt_image = pygame.image.load("images/blocks/dirt_block.gif")
grass_on_dirt = pygame.image.load("images/blocks/dirt_grass_block.gif")
dirt_block_wsnow = pygame.image.load("images/blocks/dirt_block_wsnow.gif")
wolf_image_left = pygame.image.load('images/characters/hungry_wolf_left.gif')
platform_x_img = pygame.image.load('images/blocks/dirt_grass_block.gif')
platform_y_img = pygame.image.load('images/blocks/dirt_grass_block.gif')
ice_block = pygame.image.load("images/blocks/ice_block.gif")
ice_block_wsnow = pygame.image.load("images/blocks/ice_block_wsnow.gif")
ice_block_wcracks = pygame.image.load("images/blocks/ice_block_wcracks.gif")
snow_block = pygame.image.load("images/blocks/snow_block.gif")
water_block = pygame.image.load("images/blocks/water_block.gif")
water_surface = pygame.image.load("images/blocks/water_surface.gif")
dark_wood = pygame.image.load("images/blocks/dark_wooden_block.gif")
light_wood = pygame.image.load("images/blocks/wooden_block.gif")
coin_image = pygame.image.load('images/blocks/bitcoin_image.gif')
restart_image = pygame.image.load("images/game_functions/restart_button.gif")
start_image = pygame.image.load("images/game_functions/start_button.gif")
exit_image = pygame.image.load("images/game_functions/exit_button.gif")
load_image = pygame.image.load('images/game_functions/load_button.gif')
save_image = pygame.image.load("images/game_functions/save_button.gif")
stone_block = pygame.image.load("images/blocks/stone_block.gif")
stone_block_wgrass = pygame.image.load("images/blocks/stone_block_wgrass.gif")
mossy_stone = pygame.image.load("images/blocks/mossy_stone.gif")
mossy_stone_wgrass = pygame.image.load("images/blocks/mossy_stone_wgrass.gif")
plain_chest = pygame.image.load("images/blocks/plain_chest.gif")
wood_chest_wsnow = pygame.image.load("images/blocks/wood_chest_wsnow.gif")
steel_block = pygame.image.load("images/blocks/steel_block.gif")
ending_block = pygame.image.load("images/blocks/miner_stone.gif")

#define game variables
clicked = False
level = 1

#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(16):
	r = [0] * 16
	world_data.append(r)

#create boundary
for tile in range(0, 16):
	world_data[15][tile] = 1
	world_data[0][tile] = 1
	world_data[tile][0] = 1
	world_data[tile][15] = 1

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for c in range(17):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
		#horizontal lines
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
	for row in range(16):
		for col in range(16):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1: #dirt blocks
					img = pygame.transform.scale(dirt_image, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2: #grass_on_dirt blocks
					img = pygame.transform.scale(grass_on_dirt, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3: #enemy blocks
					img = pygame.transform.scale(wolf_image_left, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 4: #horizontally moving platform
					img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5: #vertically moving platform
					img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 6: # water surface
					img = pygame.transform.scale(water_surface, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 7: # water block
					img = pygame.transform.scale(water_block, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 8: # ending miner's block
					img = pygame.transform.scale(ending_block, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 9: # stone
					img = pygame.transform.scale(stone_block, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 10: # snow
					img = pygame.transform.scale(snow_block, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 11: # ice
					img = pygame.transform.scale(ice_block, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 12: # chest
					img = pygame.transform.scale(plain_chest, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 13: #exit
					img = pygame.transform.scale(exit_image, (tile_size * 3, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 14: # ice block w/snow
					img = pygame.transform.scale(ice_block_wsnow, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 15: # chest w/snow
					img = pygame.transform.scale(wood_chest_wsnow, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 16: # stone w/grass
					img = pygame.transform.scale(stone_block_wgrass, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 17: # mossy stone
					img = pygame.transform.scale(mossy_stone, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 18: # mossy stone w/grass
					img = pygame.transform.scale(mossy_stone_wgrass, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 19: # dark wood
					img = pygame.transform.scale(dark_wood, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 20: # light wood
					img = pygame.transform.scale(light_wood, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 21: # ice block wcracks
					img = pygame.transform.scale(ice_block_wcracks, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 22: # dirt w/snow
					img = pygame.transform.scale(dirt_block_wsnow, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))					
				if world_data[row][col] == 23: # steel block
					img = pygame.transform.scale(steel_block, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 24: # coin
					img = pygame.transform.scale(coin_image, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create load and save buttons
save_button = Button(screen_width // 2 + 25, screen_height -50, save_image)
load_button = Button(screen_width // 2 + 225, screen_height -50, load_image)

#main game loop
run = True
while run:

	clock.tick(fps)

	#draw background
	screen.fill(green)
	screen.blit(background_image, (0, 0))

	#load and save level
	if save_button.draw():
		#save level data
		pickle_out = open(f'levels/level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data
		if path.exists(f'levels/level{level}_data'):
			pickle_in = open(f'levels/level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)


	#show the grid and draw the level tiles
	## draw_grid()
	draw_world()


	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 45)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 25)
	draw_text('Press LOAD to edit and then SAVE', font, white, tile_size, screen_height - 5)

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < 16 and y < 16:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 24:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 24
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1
                                

	#update game display window
	pygame.display.update()

pygame.quit()
