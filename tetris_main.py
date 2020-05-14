import pygame, sys, random
from pygame.locals import *
from random import randint
from functions import *
from parameters import *
from lower_functions import *

pygame.init()
pygame.mixer.init()

myfont = pygame.font.SysFont('Comic Sans MS', 50)
textsurface = myfont.render('Game Over!', False, BLACK, RED)
game_over_size = myfont.size('Game Over!')[0]

myfont2 = pygame.font.SysFont('Comic Sans MS', 20)

screen = pygame.display.set_mode((windowwidth, windowheight), 0, 32)
screen.fill(CYAN)

# ============
space = False
old_rects = []
color = GREEN
colors = [RED, YELLOW, MAGENTA, GREEN, BLUE]

shape = "I"
shapes = ["I", "J", "L", "K", "o", "z", "s"]

orientation = 0 # orientation by how many times 90 degrees clockwise turned from original shape
orientations = [0, 1, 2, 3]

points = 0

score = myfont2.render('Score: ' + str(points), False, BLACK)

move_y = starting_y(shape, orientation) - rec_size # -rec_size because before drawing it gets incremented

lane = get_random_lane(shape, orientation)
# =============

start_time = pygame.time.get_ticks()

# example of show image on screen: coin = screen.blit(coin_Img, (x,get_coin_y(counter)))
# example of rectangle on screen: pygame.draw.rect(screen, WHITE, (top_left_corner_x, top_left_corner_y, x_length, y_length))

while True:

	# === Fixed Screen Content ===
	screen.fill(CYAN)
	pygame.draw.rect(screen, WHITE, (hor_margin,0,windowwidth-2*hor_margin,windowheight-vert_margin))
	draw_old_rects(screen, old_rects)
	screen.blit(score, (hor_margin, windowheight-vert_margin))

	# === Draw Current Rectangles ===
	new_step, bottom, new_step_size = get_y(start_time, space, lane, old_rects, shape, orientation, move_y)
	if new_step and not bottom: move_y = new_step_size

	rects = draw_shape(screen, move_y, lane, color, shape, orientation)

	# === Event Management ===
	for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				lowest_y = max(shape_incr(shape, orientation), key = itemgetter(1))[1]
				if event.key == pygame.K_LEFT:
					if move_available(shape, orientation, lane, move_y, old_rects, "left"): 
						lane -= 1
				elif event.key == pygame.K_RIGHT:
					if move_available(shape, orientation, lane, move_y, old_rects, "right"): 
						lane += 1
				elif event.key == pygame.K_SPACE:
					space = True

				elif event.key == pygame.K_f:
					if orientation < 3:
						new_orientation = orientation + 1
					else:
						new_orientation = 0

					if move_available(shape, orientation, lane, move_y, old_rects, "turn"):
						orientation = new_orientation

			if event.type == QUIT:
				pygame.quit()
				sys.exit()

	# === Reset All Parameters for new Rectangles ===
	if bottom:
		space = False
		for rect in rects:
			old_rects.append(rect)
		start_time = pygame.time.get_ticks()
		color = colors[randint(0, len(colors)-1)]
		shape = shapes[randint(0, len(shapes)-1)]
		orientation = orientations[randint(0,len(orientations)-1)] # orientation by how many times 90 degrees clockwise turned from original shape
		lane = get_random_lane(shape, orientation)
		move_y = starting_y(shape, orientation) - rec_size # -rec_size because before drawing it gets incremented

		# === Check for full rows, remove them and add points =====
		full_rows = get_full_rows(old_rects)
		old_rects = remove_row(old_rects, full_rows)

		points = update_score(full_rows, points)
		score = myfont2.render('Score: ' + str(points), False, BLACK)

	# ===== Check for any rects in the top row if yes then game over ====
	while game_over(old_rects):
		screen.fill(CYAN)
		pygame.draw.rect(screen, WHITE, (hor_margin,0,windowwidth-2*hor_margin,windowheight-vert_margin))
		draw_old_rects(screen, old_rects)
		screen.blit(textsurface,((windowwidth-game_over_size)/2,windowheight/3))
		screen.blit(score, (hor_margin, windowheight-vert_margin))

		# === Event Management ===
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()

	pygame.display.update()

