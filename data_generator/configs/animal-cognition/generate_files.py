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


def tunnel_tasks(number_of_conf=10):
    for i in range(number_of_conf):
        x_ref = random.randint(5, 20)
        z_ref = random.randint(5, 20)
        goal_pos = Vector3(x_ref, 0, z_ref)
        goal_item = Item(name="GoodGoal", positions=[goal_pos])
        if i % 2 == 0:
            wall_item = Item(name="CylinderTunnelTransparent", positions=[goal_pos])
        else:
            wall_item = Item(name="CylinderTunnel", positions=[goal_pos], colors=[RGB(153, 153, 153)])
        items = [
                wall_item,
                goal_item
            ]
        save_arena(items, "tunnel_tasks_{}".format(i))

# to-do implement this function to test files
def detour_tasks(number_of_conf=2):
    """
    Build config files with transparent walls and the agent is in the
    opposite side of the food.
    """
    min_x = 5
    max_x = 35
    min_z = 5
    max_x = 35
    for i in range(number_of_conf):
        region = random.randint(1, 4)
        x_wall_pos = random.randint(min_x, max_x)
        z_wall_pos = random.randint(min_z, max_z)
        # lv
        if region == 0:
            food_pos = Vector3(x_wall_pos, 0, z_wall_pos)
    

# To-do: find the range of values for x and z
def build_y_mazes(number_of_conf=2):
    """
    Build config files with Y mazes. Even numbers have the good goal 
    on the left and odd numbers on the right.
    +----------+
    |\  \  /  /|
    | \  \/  / |
    |  |    |  |
    |  |    |  |
    +----------+
    wall[0] : lvw : left vertical wall
    wall[1] : rvw : right vertical wall
    wall[2] : ldwo : left vertical wall outside
    wall[3] : rdwo : right diagonal wall outside
    wall[4] : ldwi : left diagonal wall inside
    wall[5] : rdwi : right diagonal wall inside
    """
    min_x_ref = 10
    max_x_ref = 10
    min_z_ref = 10
    max_z_ref = 10
    colors = [RGB(153, 153, 153) for i in range(6)]
    for i in range(number_of_conf):
        x_ref = random.randint(min_x_ref, max_x_ref)
        z_ref = random.randint(min_x_ref, max_z_ref)
        t_ref = 40 - 2 * x_ref
        thickness = 0.1
        height = 5
        walls_pos = [None for i in range(6)]
        walls_pos[0] = Vector3(x_ref, 0, z_ref)
        walls_pos[1] = Vector3(x_ref + t_ref, 0, z_ref)
        walls_pos[2] = Vector3(x_ref / 2, 0, z_ref + 20)
        walls_pos[3] = Vector3((40 + x_ref + t_ref) / 2 , 0, z_ref + 20)
        walls_pos[4] = Vector3((x_ref / 2) + 10, 0, z_ref + 20)
        walls_pos[5] = Vector3((x_ref + t_ref) / 2 +  10 , 0, z_ref + 20)
        walls_sizes = [None for i in range(6)]
        walls_sizes[0] = Vector3(thickness, height, z_ref * 2)
        walls_sizes[1] = Vector3(thickness,  height, z_ref * 2)
        walls_sizes[2] = walls_sizes[3] = walls_sizes[4] = walls_sizes[5] =\
            Vector3(thickness, height,  math.sqrt(x_ref ** 2 + (40 - 2 * z_ref) ** 2) - 4 * thickness)
        walls_rot = [0 for i in range(6)]
        angle = math.degrees(math.atan((x_ref / 2) / (20 - z_ref)))
        walls_rot[2] = walls_rot[4] = 360 - angle
        walls_rot[3] = walls_rot[5] = angle
        left_food_pos = Vector3((x_ref + 10) / 2, 0, z_ref + 20)
        right_food_pos = Vector3((30 + t_ref + x_ref) / 2, 0, z_ref + 20)
        good_goal_pos = left_food_pos if i % 2 == 0 else right_food_pos  
        bad_goal_pos = right_food_pos if i % 2 == 0 else left_food_pos  
        items = [
                    Item(name="Wall", positions=walls_pos, rotations=walls_rot, sizes=walls_sizes, colors=colors),
                    Item(name="GoodGoal", positions=[good_goal_pos]),
                    Item(name="BadGoal", positions=[bad_goal_pos]),
                    Item(name="Agent", positions=[Vector3(20, 0, 5)]),
                ]
        save_arena(items, "y_maze_{}".format(i))

if __name__ == "__main__":
    # build_y_mazes()
    tunnel_tasks()