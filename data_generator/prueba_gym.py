from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig
import numpy as np
import random
from PIL import Image
import cv2

env_path = '../env/AnimalAI'
worker_id = random.randint(1, 100)
arena_config_in = ArenaConfig('ordered_configs/avoid_red/1-25-1.yml')

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
try:
  while True:
    state = env.reset()
    while not done:  
      numpy_image = state[0] * 255
      numpy_image = numpy_image.astype('uint8')
      im = Image.fromarray(numpy_image)
      im.save('./images/{}.png'.format(i))
      i += 1
      for j in range(SKIPPED_FRAMES):
        state, reward, done, info = env.step(env.action_space.sample())
        # first = int(input())
        # second = int(input())
        # directions = {
        #   "n" : 0,
        #   "w" : 1,
        #   "s" : 2,
        #   "d" : 1,
        #   "a" : 2,
        # }
        # state, reward, done, info = env.step((directions[first], directions[second]))
except KeyboardInterrupt:
  env.close()

# im = Image.fromarray(numpy_image.astype('uint8'))
# im.save("image.jpeg")
