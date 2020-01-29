import random
import os
import sys

import numpy as np
import cv2

from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig

path = './ordered_configs'
env_path = '../env/AnimalAI'
number_of_images = 5
SKIPPED_FRAMES = 10
worker_id = 100

env = AnimalAIEnv(environment_filename=env_path,
					worker_id=worker_id,
					n_arenas=1,
					arenas_configurations=None,
					docker_training=False,
					retro=False)
for dir_name in os.listdir(path):
	if not os.path.exists('./datasets/{}'.format(dir_name)):
		os.makedirs('./datasets/{}'.format(dir_name))
	path_to_dir = os.path.join(path, dir_name)
	for file in os.listdir(path_to_dir):
		arena_file_path = os.path.join(path_to_dir, file)
		arena_config_in = ArenaConfig(arena_file_path)
		env.reset(arena_config_in)
		print(arena_file_path)
		i = 0
		done = False
		try:
			while True and i < number_of_images:
				done = False
				state = env.reset(arena_config_in)
				while not done and i < number_of_images:  
					numpy_image = state[0] * 255
					numpy_image = numpy_image.astype('uint8')
					cv_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB)
					resized = cv2.resize(cv_image, (300, 300), interpolation = cv2.INTER_AREA) 
					cv2.imwrite('./datasets/{}/{}_{}.png'.format(dir_name, file[:-4], i), resized)
					i += 1
					for j in range(SKIPPED_FRAMES):
						state, reward, done, info = env.step(env.action_space.sample())
		except KeyboardInterrupt:
			env.close()
env.close()