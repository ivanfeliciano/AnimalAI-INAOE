import random
import math
import yaml
import sys
import numpy as np
from collections import namedtuple

from animalai.envs.arena_config import Vector3, RGB, Item, Arena

WALL_HEIGHT = 1
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

class ArenaConfig(yaml.YAMLObject):
	 yaml_tag = u'!ArenaConfig'
	 def __init__(self, arenas):
		 self.arenas = arenas
	
def save_arena(items, filename):
	arenas = {0 : Arena(t=250, items=items)}
	with open('{}.yaml'.format(filename), 'w') as outfile:
		yaml.dump(ArenaConfig(arenas), outfile, default_flow_style=False)


class ArenaMatrix(object):
	def __init__(self, max_good_goals=10, max_gold_goals=10, max_bad_goals=10):
		self.max_gold_goals = max_gold_goals
		self.max_good_goals = max_good_goals
		self.max_bad_goals = max_bad_goals
		self.grid = [["." for i in range(40)] for j in range(40)]
		# pos, sizes, rots, colors
		self.map_of_objects = {
			"Agent" : [[]],
			"CylinderTunnelTransparent" : [[], [], []],
			"Wall" : [[], [], [], []],
			"GoodGoal" : [[], []],
			"GoodGoalMulti": [[], []],
			"BadGoal" : [[], []],
			"Ramp" : [[], [], [], []],
			"Cardbox1" : [[], [], []],
			"WallTransparent": [[], [], []],
			"HotZone": [[], [], []],
			"Deathzone" : [[], [], []],
		}

	def spawn_borderlines(self, width=10, height=10, filename="borderlines", id=0):
		init_col = 20 - width // 2
		init_row = 20 - height // 2
		walls_pos = []
		walls_sizes = []
		items = []
		for i in range(init_row, init_row + height):
			self.grid[i][init_col] = "#"
			self.grid[i][init_col + width - 1] = "#"
			walls_pos.append(Vector3(init_col + 0.5, 0, i + 0.5))
			walls_pos.append(Vector3(init_col + width - 1 + 0.5, 0, i + 0.5))
			walls_sizes.append(Vector3(1, 2, 1))
			walls_sizes.append(Vector3(1, 2, 1))
		for i in range(init_col, init_col + width):
			self.grid[init_row][i] = "#"
			self.grid[init_row + height - 1][i] = "#"
			walls_pos.append(Vector3(i + 0.5, 0, init_row + 0.5))
			walls_pos.append(Vector3(i + 0.5, 0, init_row + height - 1 + 0.5))
			walls_sizes.append(Vector3(1, 2, 1))
			walls_sizes.append(Vector3(1, 2, 1))
		agent_pos = [Vector3(20, 0, 20)]
		agent_item = Item(name="Agent", positions=agent_pos)
		items.append(Item(name="Wall", positions=walls_pos, sizes=walls_sizes,\
								rotations=[0 for i in range(len(walls_pos))],\
								colors=[RGB(153, 153, 153) for i in range(len(walls_pos))]))
		items.append(agent_item)
		save_arena(items, "{}_{}".format(filename, id))
	def spawn_objects(self, width, height, name, n_objects):
		init_col = 20 - width // 2 + 1
		init_row = 20 - height // 2 + 1
		for i in range(n_objects):
			row = random.randint(init_row, init_row + height - 3)
			col = random.randint(init_col, init_col + width - 3)
			while self.grid[row][col] != ".":
				row = random.randint(init_row, init_row + height - 3)
				col = random.randint(init_col, init_col + width - 3)
			if name == "GoodGoal": self.grid[row][col] = "O"
			if name == "GoodGoalMulti": self.grid[row][col] = "o"
			if name == "BadGoal": self.grid[row][col] = "x"
	def spawn_ramp(self, width, height, ramp_height):
		init_col = 20 - width // 2 + 1
		init_row = 20 - height // 2 + 1
		ramp_width = (width - 2) / 10
		ramp_height = (height - 2) / 10


	def generate_arena(self, width=12, height=12):
		self.spawn_borderlines(width, height)
		self.spawn_objects(width, height, "GoodGoal", 3)
		self.spawn_objects(width, height, "GoodGoalMulti", 3)
		self.spawn_objects(width, height, "BadGoal", 3)
		for i in self.grid:
			print("".join(i))
	def handle_object_type(self, x, z, element):
		if element != None:
			name = type(element).__name__
			# pos
			self.map_of_objects[name][0].append(Vector3(x + 0.5, 0, z + 0.5))
			if name == "Agent":
				return
			if name == "Wall" and element.with_food == True:
				self.map_of_objects["GoodGoalMulti"][0].append(Vector3(x + 0.5, WALL_HEIGHT, z + 0.5))
				self.map_of_objects["GoodGoalMulti"][1].append(Vector3(1, 1, 1))
			# sizes
			if name == "CylinderTunnelTransparent":
				self.map_of_objects[name][1].append(Vector3(4, 4, 4))
				if element.with_food == True:
					self.map_of_objects["GoodGoal"][0].append(Vector3(x + 0.5, 0, z + 0.5))
					self.map_of_objects["GoodGoal"][1].append(Vector3(1, 1, 1))	
			else:
				self.map_of_objects[name][1].append(Vector3(1, WALL_HEIGHT, 1))
			# rotations
			if name == "CylinderTunnelTransparent" or name == "Ramp":
				self.map_of_objects[name][2].append(element.rotation)
			elif name not in ("GoodGoal", "GoodGoalMulti", "BadGoal"):
				self.map_of_objects[name][2].append(0)
			# colors
			if name == "Wall":
				self.map_of_objects[name][3].append(RGB(153, 153, 153))
			if name == "Ramp":
				self.map_of_objects[name][3].append(RGB(255, 0, 255))

	def create_arena_from_np_array(self, np_filename, filename="config_test", id=0):
		np_grid = np.load(np_filename, allow_pickle=True)
		items = []
		for row in range(np_grid.shape[0]):
			for col in range(len(np_grid[row])):
				self.handle_object_type(row, col, np_grid[row][col])
		for key in self.map_of_objects:
			if len(self.map_of_objects[key][0]) < 1: continue
			pos = self.map_of_objects[key][0]
			sizes = self.map_of_objects[key][1] if len(self.map_of_objects[key]) > 1 else []
			rotations = self.map_of_objects[key][2] if len(self.map_of_objects[key]) > 2 else []
			colors = self.map_of_objects[key][3] if len(self.map_of_objects[key]) > 3 else []
			items.append(Item(name=key, positions=pos, sizes=sizes,\
								rotations=rotations,\
								colors=colors))
		save_arena(items, "{}_{}".format(filename, id))

	def generate_basic_food(self, number_of_conf, max_bad_goals=0, max_gold_goals=0, max_good_goals=1, max_walls=0, filename="basic"):
		for config in range(number_of_conf):
			items = []
			green_goals_pos = []
			gold_goals_pos = []
			red_goals_pos = []
			green_goals_sizes = []
			gold_goals_sizes = []
			red_goals_sizes = []
			walls_pos = []
			walls_sizes = []
			walls_idx = []
			num_walls = random.randint(min(1, max_walls),\
							max_walls)
			num_green_balls = random.randint(min(1, max_good_goals),\
								max_good_goals)
			num_gold_balls = random.randint(min(1, max_gold_goals),\
								max_gold_goals)
			num_red_balls = random.randint(min(1, max_bad_goals),\
								max_bad_goals)
			list_of_idx = random.sample(range(40*40), num_red_balls + \
							num_gold_balls + num_green_balls + 1)
			while len(walls_idx) < num_walls:
				rand_i = random.randint(0, 40*40 - 1)
				if rand_i not in list_of_idx:
					walls_idx.append(rand_i)
			list_of_idx.sort()
			walls_idx.sort()
			k = 0
			l = 0
			for i in range(40):
				for j in range(40):
					if l < len(walls_idx) and 40 * i + j == walls_idx[l]:
						walls_pos.append(Vector3(i + 0.5, 0, j + 0.5))
						walls_sizes.append(Vector3(1, 2, 1))
						l += 1
					if k < len(list_of_idx) and 40 * i + j == list_of_idx[k]:
						if k == len(list_of_idx) - 1:
							agent_pos = [Vector3(i + 0.5, 0, j + 0.5)]
							agent_rot = [random.choice([0, 90, 180, 270])]
							agent_item = Item(name="Agent", positions=agent_pos, rotations=agent_rot)
						if num_green_balls > 0:
							num_green_balls -= 1
							green_goals_pos.append(Vector3(i + 0.5, 0, j + 0.5))
							green_goals_sizes.append(Vector3(1, 1, 1))
						elif num_red_balls > 0:
							num_red_balls -= 1
							red_goals_pos.append(Vector3(i + 0.5, 0, j + 0.5))
							red_goals_sizes.append(Vector3(1, 1, 1))
						elif num_gold_balls > 0:
							num_gold_balls -= 1
							gold_goals_pos.append(Vector3(i + 0.5, 0, j + 0.5))
							gold_goals_sizes.append(Vector3(1, 1, 1))
						k += 1
			if len(green_goals_pos) > 0: items.append(Item(name="GoodGoal", positions=green_goals_pos, sizes=green_goals_sizes))
			if len(gold_goals_pos) > 0: items.append(Item(name="GoodGoalMulti", positions=gold_goals_pos, sizes=gold_goals_sizes))
			if len(red_goals_pos) > 0: items.append(Item(name="BadGoal", positions=red_goals_pos, sizes=red_goals_sizes))
			if len(walls_pos) > 0:
				items.append(Item(name="Wall", positions=walls_pos, sizes=walls_sizes,\
								rotations=[0 for i in range(len(walls_pos))],\
								colors=[RGB(153, 153, 153) for i in range(len(walls_pos))]))
			items.append(agent_item)
			save_arena(items, "{}_{}".format(filename, config))



if __name__ == "__main__":
	# build_y_mazes()
	mi_arena_mat = ArenaMatrix()
	# mi_arena_mat.generate_arena(12, 12)
	mi_arena_mat.create_arena_from_np_array('arena_test_0.npy')
	# mi_arena_mat.generate_basic_food(number_of_conf=5, filename="./one_goal/basic_one_goal")
	# mi_arena_mat.generate_basic_food(number_of_conf=10, max_bad_goals=3, \
	# 								max_gold_goals=5, max_good_goals=2, filename="./multiple_food/multiple_goals")
	# mi_arena_mat.generate_basic_food(number_of_conf=10, max_bad_goals=1, \
	# 								max_gold_goals=5, max_good_goals=2,\
	# 								max_walls=50,\
	# 								filename="./multiple_food_walls/obstacles")