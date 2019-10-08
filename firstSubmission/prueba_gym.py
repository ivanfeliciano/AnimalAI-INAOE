from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig
import numpy as np
import random
from PIL import Image
import cv2

def get_colours(pixels, colour):
  return np.all(pixels > np.minimum(colour*.8, colour-25), axis=-1) & np.all(pixels < np.maximum(colour*1.2, colour+25), axis=-1)

env_path = './env/AnimalAI'
worker_id = random.randint(1, 100)
arena_config_in = ArenaConfig('examples/configs/2-Preferences.yaml')

env = AnimalAIEnv(environment_filename=env_path,
                  worker_id=worker_id,
                  n_arenas=1,
                  arenas_configurations=arena_config_in,
                  docker_training=False,
                  retro=False)

Green = np.array([129.0, 191.0, 65.0])
Yellow = np.array([100.0, 65.0, 5.0])
Red = np.array([185.0, 50.0, 50.0])


directions = {
  "nothing" : 0,
  "forward" : 1,
  "backward" : 2,
  "right" : 1,
  "left" : 2,
}
done = False
number_of_episodes = 10
i = 0
SKIPPED_FRAMES = 5
try:
  while i < number_of_episodes:
    state = env.reset()
    cummulative_reward = 0
    i += 1
    done = False
    while not done:  
      first = directions["forward"]
      second = 0
      num_of_left_green_pix = 0
      num_of_right_green_pix = 0
      num_of_left_red_pix = 0
      num_of_right_red_pix = 0
      num_of_right_yellow_pix = 0
      num_of_left_yellow_pix = 0
      numpy_image = state[0] * 255
      numpy_image = numpy_image.astype('uint8')
      for x in range(len(numpy_image)):
        for y in range(len(numpy_image)):
          if get_colours(numpy_image[x, y], Green):
            if y <= 41: num_of_left_green_pix += 1
            else: num_of_right_green_pix += 1
          if get_colours(numpy_image[x, y], Yellow):
            if y <= 41: num_of_left_yellow_pix += 1
            else: num_of_right_yellow_pix += 1
          if get_colours(numpy_image[x, y], Red):
            if y <= 41: num_of_left_red_pix += 1
            else: num_of_right_red_pix += 1
      if num_of_left_red_pix > num_of_left_yellow_pix + num_of_left_green_pix:
        second = directions["right"]
      if num_of_right_red_pix > num_of_right_yellow_pix + num_of_right_green_pix:
        second = directions["left"]
      # move to the left if there is some good stuff on the left
      if num_of_left_yellow_pix + num_of_left_green_pix > \
        num_of_right_yellow_pix + num_of_right_green_pix:
        second = directions["left"]
      # move to the right if there is some good stuff on the right
      elif num_of_left_yellow_pix + num_of_left_green_pix > \
        num_of_right_yellow_pix + num_of_right_green_pix:
        second = directions["right"]
      else:
        second = directions["right"]
        first = directions["nothing"]
      for j in range(SKIPPED_FRAMES):
        state, reward, done, info = env.step([first, second])
        cummulative_reward += reward
    print("Episode : {}\nAccumulative Reward : {}".format(i, cummulative_reward))
  env.close()
except KeyboardInterrupt:
  env.close()

# im = Image.fromarray(numpy_image.astype('uint8'))
# im.save("image.jpeg")
