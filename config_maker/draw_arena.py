import sys
from copy import deepcopy
from collections import namedtuple
import pygame
import numpy as np


args = sys.argv
FILENAME = args[1] if len(args) > 1 else "arena_test"
BORDERLINE_WIDTH = int(args[2]) if len(args) > 2 else 22
BORDERLINE_HEIGHT = int(args[3]) if len(args) > 3 else 22

COLORS = {
	"GoodGoal" : (148, 210, 83), 
	"GoodGoalMulti" : (176, 129, 25),
	"BadGoal": (180, 44, 46),
	"GenericGray": (153, 153, 153),
	"Ramp":  (255, 0, 255),
	"HotZone": (255, 145, 48),
	"DeathZone": (0, 0, 0),
	"Box": (64, 52, 40),
	"Cylinder":  (102, 153, 153),
	"InvisibleWalls":  (235, 235, 224),
	"Agent" : (0, 128, 255)
} 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 20
HEIGHT = 20
MARGIN = 1
ROTATION = 180

GoodGoal = namedtuple("GoodGoal", [])
GoodGoalMulti = namedtuple("GoodGoalMulti", [])
BadGoal = namedtuple("BadGoal", [])
Wall = namedtuple("Wall", ['with_food'])
Ramp = namedtuple("Ramp", ['rotation'])
CylinderTunnelTransparent = namedtuple("CylinderTunnelTransparent", ['rotation', 'with_food'])
Cardbox1 = namedtuple("Cardbox1", [])
WallTransparent = namedtuple("WallTransparent", [])
HotZone = namedtuple("HotZone", [])
Deathzone = namedtuple("Deathzone", [])
Agent = namedtuple("Agent", [])

grid = [[None for j in range(40)] for i in range(40)]
arena_grid = [[None for j in range(40)] for i in range(40)]
init_col = 20 - BORDERLINE_WIDTH // 2
init_row = 20 - BORDERLINE_HEIGHT // 2
for i in range(init_row, init_row + BORDERLINE_HEIGHT):
	grid[i][init_col] = 4
	arena_grid[i][init_col] = Wall(with_food=False)
	grid[i][init_col + BORDERLINE_WIDTH - 1] = 4
	arena_grid[i][init_col + BORDERLINE_WIDTH - 1] = Wall(with_food=False)

for i in range(init_col, init_col + BORDERLINE_WIDTH):
	grid[init_row][i] = 4
	arena_grid[init_row][i] = Wall(with_food=False)
	grid[init_row + BORDERLINE_HEIGHT - 1][i] = 4
	arena_grid[init_row + BORDERLINE_HEIGHT - 1][i] = Wall(with_food=False)

initial_grid = deepcopy(grid)
initial_arena_grid = deepcopy(arena_grid)

pygame.init()
 
WINDOW_SIZE = [(WIDTH + MARGIN) * 40 + MARGIN, (HEIGHT + MARGIN) * 40 + MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)
COUNTER = 0
 
done = False
 
clock = pygame.time.Clock()
code = 0
named_element = None

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == 49: code = 1; named_element = GoodGoal()
			if event.key == 50: code = 2; named_element = GoodGoalMulti()
			if event.key == 51: code = 3; named_element = BadGoal()
			if event.key == 52: code = 4; named_element = Wall(False)
			if event.key == 53: code = 5; named_element = Ramp(ROTATION)
			if event.key == 54: code = 6; named_element = CylinderTunnelTransparent(ROTATION, False)
			if event.key == 55: code = 7; named_element = Cardbox1()
			if event.key == 56: code = 8; named_element = WallTransparent()
			if event.key == 57: code = 9; named_element = HotZone()
			if event.key == 48: code = 10; named_element = Deathzone()
			if event.key == 97: code = 11; named_element = Agent()
			if event.key == 122: ROTATION += 90; ROTATION %= 360; print("ROTATION = {}".format(ROTATION))
			if event.key == 114:
				grid = deepcopy(initial_grid)
				arena_grid = deepcopy(initial_arena_grid)
			if event.key == 115:
				print("Saving array in {}_{}".format(FILENAME, COUNTER))
				np.save("{}_{}".format(FILENAME, COUNTER), np.rot90(arena_grid, 3))
				COUNTER += 1
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			column = pos[0] // (WIDTH + MARGIN)
			row = pos[1] // (HEIGHT + MARGIN)
			if grid[row][column] != None:
				if grid[row][column] == 6 and code == 1:
					grid[row][column] = (6, 1)
					arena_grid[row][column] = CylinderTunnelTransparent(ROTATION, with_food=True)
				if grid[row][column] == 4 and code == 2:
					grid[row][column] = (4, 2)
					arena_grid[row][column] = Wall(with_food=True)
			else:
				arena_grid[row][column] = named_element
				grid[row][column] = code
			if code == 6:
				grid[row - 1][column] = code
				grid[row - 1][column - 1] = code
				grid[row - 1][column + 1] = code
				grid[row][column - 1] = code
				grid[row][column + 1] = code
				grid[row + 1][column - 1] = code
				grid[row + 1][column] = code
				grid[row + 1][column + 1] = code
 
	screen.fill(BLACK)
 
	# Draw the grid
	for row in range(40):
		for column in range(40):
			color = WHITE
			if grid[row][column] == 1: color = COLORS['GoodGoal']
			if grid[row][column] == 2: color = COLORS['GoodGoalMulti']
			if grid[row][column] == 3: color = COLORS['BadGoal']
			if grid[row][column] == 4: color = COLORS['GenericGray']
			if grid[row][column] == 5: color = COLORS['Ramp']
			if grid[row][column] == 6: color = COLORS['Cylinder']
			if grid[row][column] == 7: color = COLORS['Box']
			if grid[row][column] == 8: color = COLORS['InvisibleWalls']
			if grid[row][column] == 9: color = COLORS['HotZone']
			if grid[row][column] == 10: color = COLORS['DeathZone']
			if grid[row][column] == 11: color = COLORS['Agent']
			if grid[row][column] == (6, 1): color = COLORS['GoodGoal']
			if grid[row][column] == (4, 2): color = COLORS['GoodGoalMulti']
			pygame.draw.rect(screen,
							 color,
							 [(MARGIN + WIDTH) * column + MARGIN,
							  (MARGIN + HEIGHT) * row + MARGIN,
							  WIDTH,
							  HEIGHT])
	clock.tick(60)
	pygame.display.flip()

pygame.quit()