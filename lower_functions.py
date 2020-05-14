from parameters import *
from operator import itemgetter


def shape_incr(shape, orientation):
	# print(shape, orientation)
	if shape == "I":
		if orientation == 0:
			x_coords = [0, 0, 0, 0]
			y_coords = [-1, 0, 1, 2]
		elif orientation == 1:
			x_coords = [-2, -1, 0, 1]
			y_coords = [0, 0, 0, 0]
		elif orientation == 2:
			x_coords = [0, 0, 0, 0]
			y_coords = [-2, -1, 0, 1]
		elif orientation == 3:
			x_coords = [-1, 0, 1, 2]
			y_coords = [0, 0, 0, 0]

	elif shape == "J":
		if orientation == 0:
			x_coords = [0, 0, 0, -1]
			y_coords = [-1, 0, 1, 1]
		elif orientation == 1:
			x_coords = [-1, -1, 0, 1]
			y_coords = [-1, 0, 0, 0]
		elif orientation == 2:
			x_coords = [1, 0, 0, 0]
			y_coords = [-1, -1, 0, 1]
		elif orientation == 3:
			x_coords = [-1, 0, 1, 1]
			y_coords = [0, 0, 0, 1]

	elif shape == "L":
		if orientation == 0:
			x_coords = [0, 0, 0, 1]
			y_coords = [-1, 0, 1, 1]
		elif orientation == 1:
			x_coords = [-1, -1, 0, 1]
			y_coords = [1, 0, 0, 0]
		elif orientation == 2:
			x_coords = [-1, 0, 0, 0]
			y_coords = [-1, -1, 0, 1]
		elif orientation == 3:
			x_coords = [-1, 0, 1, 1]
			y_coords = [0, 0, 0, -1]

	elif shape == "K":
		if orientation == 0:
			x_coords = [-1, 0, 0, 1]
			y_coords = [0, 0, -1, 0]
		elif orientation == 1:
			x_coords = [0, 0, 1, 0]
			y_coords = [-1, 0, 0, 1]
		elif orientation == 2:
			x_coords = [-1, 0, 0, 1]
			y_coords = [0, 0, 1, 0]
		elif orientation == 3:
			x_coords = [0, 0, -1, 0]
			y_coords = [-1, 0, 0, 1]

	elif shape == "o":
		x_coords = [0, 1, 0, 1]
		y_coords = [0, 0, 1, 1]

	elif shape == "z":
		if orientation == 0:
			x_coords = [-1, 0, 0, 1]
			y_coords = [0, 0, 1, 1]
		elif orientation == 1:
			x_coords = [0, 0, -1, -1]
			y_coords = [-1, 0, 0, 1]
		elif orientation == 2:
			x_coords = [1, 0, 0, -1]
			y_coords = [0, 0, -1, -1]
		elif orientation == 3:
			x_coords = [0, 0, 1, 1]
			y_coords = [1, 0, 0, -1]

	elif shape == "s":
		if orientation == 0:
			x_coords = [1, 0, 0, -1]
			y_coords = [0, 0, 1, 1]
		elif orientation == 1:
			x_coords = [0, 0, 1, 1]
			y_coords = [-1, 0, 0, 1]
		elif orientation == 2:
			x_coords = [-1, 0, 0, 1]
			y_coords = [0, 0, -1, -1]
		elif orientation == 3:
			x_coords = [0, 0, -1, -1]
			y_coords = [1, 0, 0, -1]

	return list(zip(x_coords, y_coords))


def starting_y(shape, orientation):
	rects_incr = shape_incr(shape, orientation)
	max_y = max(rects_incr, key = itemgetter(1))[1]

	start_y = -1 * (max_y+1) * rec_size
	print("MAX:", max_y, "START:", start_y/28, "Orientation:", orientation)
	return start_y 


def get_random_lane(shape, orientation):
	# Get a random legal starting lane without any rects outside of the lanes

	lane = 0

	rects_incr = shape_incr(shape, orientation)
	min_x = min(rects_incr, key = itemgetter(0))[0]
	max_x = max(rects_incr, key = itemgetter(0))[0]

	lane = randint(-min_x, 9-max_x)

	return lane


def draw_rect(screen, lane, move_y, color):
	BLACK = (0,0,0)

	x = hor_margin + rec_size * lane
	y = move_y

	pygame.draw.rect(screen, BLACK, (x, y, rec_size, rec_size))
	pygame.draw.rect(screen, color, (x+rec_border, y+rec_border, rec_size - 2 * rec_border, rec_size - 2 * rec_border))
	return x, y


def bottom_reached(shape, orientation, lane, move_y, old_rects):
	# TODO to touch another old_rect the rect doesnt need to be the lowest it can be in the middle somewhere too

	bottom_reached = False
	lanes = []

	bottom = windowheight-vert_margin-rec_size # 600 - 40(bottom margin) - 28(rect width) normally
	
	rects_incr = shape_incr(shape, orientation)
	max_y = move_y + rec_size * max(rects_incr, key = itemgetter(1))[1]

	for x_incr, y_incr in rects_incr:
		for x, y, color in old_rects:
			if move_y + (y_incr+1)*rec_size == y and lane + x_incr == (x-hor_margin)/rec_size:
				# print("Old Rect touched")
				bottom_reached = True

	if max_y == bottom:
		# print("Reached Bottom")
		bottom_reached = True

	return bottom_reached


def get_new_lanes(shape, orientation, lane, move):
	new_lanes = []
	new_orientation = orientation
	rects_incr = shape_incr(shape, orientation)

	if move == "left":
		new_lanes.append(lane + min(rects_incr, key = itemgetter(0))[0]-1)
	elif move == "right":
		new_lanes.append(lane + max(rects_incr, key = itemgetter(0))[0]+1)
	elif move == "turn":
		if orientation != 3:
			new_orientation = orientation + 1
		else:
			new_orientation = 0

		new_rects_incr = shape_incr(shape, new_orientation)
		for (x_incr, y_incr) in new_rects_incr:
			new_lanes.append(lane + x_incr)
	return new_lanes, new_orientation


def round_to_rec_size(move_y, y_incr):
	rest = (move_y + y_incr*rec_size)%rec_size

	if rest >= rec_size/2:
		rounded = move_y + y_incr*rec_size - (move_y + y_incr*rec_size)%rec_size + rec_size
	else:
		rounded = move_y + y_incr*rec_size - (move_y + y_incr*rec_size)%rec_size

	return rounded


def get_shape_coords(shape, orientation, lane, move_y):
	x_coords = []
	y_coords = []
	rects_incr = shape_incr(shape, orientation)

	for x_incr, y_incr in rects_incr:
	
		x_coords.append((lane+x_incr) * rec_size + hor_margin)
	
		round_y = round_to_rec_size(move_y, y_incr)
		y_coords.append(round_y)

	return x_coords, y_coords


def game_over(old_rects):
	row = []
	game_over = False
	for x, y, color in old_rects:
		if y == 0:
			game_over = True

	return game_over


def get_full_rows(old_rects):
	full_rows = []

	y_range = range(0, 533, 28)
	y_arr = []

	for i in range(len(y_range)):
		y_arr.append(0)

	for x_coord, y_coord, color in old_rects:
		# print(y_range, y_coord)

		if x_coord > 0 and y_coord > 0 and y_coord in y_range:
			y_arr[y_range.index(y_coord)] += 1
		# print(y_arr)

	for i in range(len(y_range)):
		if y_arr[i] == 10:
			full_rows.append(y_range[i])

	return full_rows


def remove_row(old_rects, full_rows):
	new_old_rects = []

	if len(full_rows) != 0:
		for x, y, color in old_rects:
			if y not in full_rows:
				for full_row in full_rows:
					if y < full_row:
						y += rec_size
				new_old_rects.append((x, y, color))
		return new_old_rects
	else:
		return old_rects


def update_score(full_rows, points):
	if len(full_rows) == 1:
		return points + 10
	else:
		return points + 20 * len(full_rows)



