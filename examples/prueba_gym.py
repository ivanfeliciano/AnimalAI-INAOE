from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig
import numpy as np
import random
import cv2

env_path = '../env/AnimalAI'
worker_id = random.randint(1, 100)
arena_config_in = ArenaConfig('configs/1-Food.yaml')

env = AnimalAIEnv(environment_filename=env_path,
                  worker_id=worker_id,
                  n_arenas=1,
                  arenas_configurations=arena_config_in,
                  docker_training=False,
                  retro=False)


done = False
number_of_episodes = 10
i = 0
SKIPPED_FRAMES = 10
state = env.reset()
print(state[0].shape)
print(state[0].ndim)
print(tuple(env.action_space.sample()))
numpy_image = state[0] * 255
numpy_image = numpy_image.astype('uint8')
cv_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB)
resized = cv2.resize(cv_image, (300, 300), interpolation = cv2.INTER_AREA) 
cv2.imwrite('kk.png', resized)
state, reward, done, info = env.step(env.action_space.sample())
env.close()

