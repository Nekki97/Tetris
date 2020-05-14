from parameters import *
from lower_functions import *

passed_time_steps = []
step_size = 7


def get_y(start_time, space, lane, old_rects, shape, orientation, move_y):
	# Gives back the new y-coordinate at the given time with or without having pressed space

	global passed_time_steps
	global step_size

	time = pygame.time.get_ticks() - start_time
	time_float = round(time/100.0)

	if space and len(passed_time_steps)%4 == 0:
		step_size = rec_size

	y_incr = max(shape_incr(shape, orientation), key = itemgetter(1))[1]

	if not bottom_reached(shape, orientation, lane, move_y, old_rects):
		if time_float not in passed_time_steps:
			move_y += step_size # 532 pixel total to touch the bottom 
			passed_time_steps.append(time_float)

			# print(passed_time_steps)
			# print("Step")
			return True, False, move_y
		else:
			return False, False, 0
	else:
		# print("Bottom reached!")
		passed_time_steps = []
		step_size = rec_size / 4
		return False, True, 0


def draw_shape(screen, move_y, lane, color, shape, orientation):
	# Draw the Shape specified in the parameters

	rects = []
	rects_incr = shape_incr(shape, orientation)

	for (x_incr, y_incr) in rects_incr:
		rec_x, rec_y = draw_rect(screen, lane + x_incr, move_y + y_incr * rec_size, color)
		if x_incr == 0 and y_incr == 0 and shape != "o":
			pygame.draw.rect(screen, BLACK, (hor_margin+lane*rec_size+int(rec_size/4), move_y+int(rec_size/4), int(rec_size/2), int(rec_size/2)))
		rects.append((rec_x, rec_y, color))

	return rects


def draw_old_rects(screen, old_rects):
	BLACK = (0,0,0)
	for x, y, color in old_rects:
		pygame.draw.rect(screen, BLACK, (x, y, rec_size, rec_size))
		pygame.draw.rect(screen, color, (x+rec_border, y+rec_border, rec_size-2*rec_border, rec_size-2*rec_border))



def move_available(shape, orientation, lane, move_y, old_rects, move):
	available = True

	new_lanes, new_orientation = get_new_lanes(shape, orientation, lane, move)

	for new_lane in new_lanes:
		if not (0 <= new_lane <= 9):
			return False

	if len(old_rects) == 0:
		return True

	if move != "turn": 
		if move == "right":
			new_lane = lane + 1
		elif move == "left":
			new_lane = lane - 1
	else:
		new_lane = lane

	if move == "turn": 
		orientation = new_orientation

	x_coords, y_coords = get_shape_coords(shape, orientation, new_lane, move_y)

	for i in range(len(x_coords)):
		if (x_coords[i], y_coords[i]) in [tuples[:-1] for tuples in old_rects]:
			available = False

	return available

