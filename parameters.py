from random import randint
import pygame
import math
from operator import itemgetter

windowheight = 600
windowwidth = 300

lanes = 10
vert_margin = 40
hor_margin = 10

rec_size = (windowwidth-2*hor_margin)/10
# Means that each lane is 28 pixels long

WHITE = (255, 255, 255)
BLACK = (0,0,0)
CYAN = (0,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
MAGENTA = (255, 0, 255)
BLUE = (0,0,255)

FPS = 100

rec_border = 2