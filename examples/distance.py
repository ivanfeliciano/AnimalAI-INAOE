from animalai.envs.environment import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
import time
import random

worker_id = random.randint(0, 100)

env = UnityEnvironment(
    n_arenas=1,
    file_name='../env_modified/AnimalAILinux',
    worker_id=worker_id,
    seed=0,
    docker_training=False,
    inference=True
)

arena_config_in = ArenaConfig('configs/empty.yaml')
env.reset(arenas_configurations=arena_config_in)
total_distance = 0
# step_time_length = 0.0595
try:
    while True:
        step = 0
        direction = input()
        if direction == "w":
            action = [1 , 0]
        if direction == "s":
            action = [2 , 0]
        if direction == "d":
            action = [0 , 1]
        if direction == "a":
            action = [0 , 2]
        while step < 1.0:
            start = time.time()     # start a timer before taking a step
            res = env.step(action)  # send a forward action to the environment
            if action == [0, 1] or action == [0, 2]:
                break
            step_time_length = time.time() - start      # compute the time it took to take the step
            speed = res['Learner'].vector_observations
            delta_distance = step_time_length * speed[0, 2]    # compute the distance covered in one step
            total_distance += delta_distance
            step += step_time_length * speed[0, 2]    # compute the distance covered in one step
            print("speed = {0:.4f}, delta_time = {1:.4f}, delta_distance = {2:.4f}, total_distance = {3:.4f}".format(speed[0,2],
                 step_time_length, delta_distance, total_distance))
            if speed[0, 2] == 0:
                #   if our agent reached the other end of the arena we close the environment
                print('Distance covered by the agent {}'.format(total_distance))
                # raise KeyboardInterrupt
    env.close()
except KeyboardInterrupt:
    env.close()