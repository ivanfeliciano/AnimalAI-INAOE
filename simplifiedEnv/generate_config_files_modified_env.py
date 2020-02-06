import random
import math
import yaml
import sys

from animalai.envs.arena_config import Vector3, RGB, Item, Arena

class ArenaConfig(yaml.YAMLObject):
     yaml_tag = u'!ArenaConfig'
     def __init__(self, arenas):
         self.arenas = arenas
    
def save_arena(items, filename):
    arenas = {0 : Arena(t=250, items=items)}
    with open('{}.yml'.format(filename), 'w') as outfile:
        yaml.dump(ArenaConfig(arenas), outfile, default_flow_style=False)


class ArenaMatrix(object):
    def __init__(self, max_good_goals=10, max_gold_goals=10, max_bad_goals=10):
        self.max_gold_goals = max_gold_goals
        self.max_good_goals = max_good_goals
        self.max_bad_goals = max_bad_goals
        self.grid = [[None for i in range(40)] for j in range(40)]
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
    mi_arena_mat.generate_basic_food(number_of_conf=5, filename="./one_goal/basic_one_goal")
    mi_arena_mat.generate_basic_food(number_of_conf=10, max_bad_goals=3, \
                                    max_gold_goals=5, max_good_goals=2, filename="./multiple_food/multiple_goals")
    mi_arena_mat.generate_basic_food(number_of_conf=10, max_bad_goals=1, \
                                    max_gold_goals=5, max_good_goals=2,\
                                    max_walls=50,\
                                    filename="./multiple_food_walls/obstacles")