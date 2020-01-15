from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig
import numpy as np
import random
from PIL import Image
import cv2


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


done = False
number_of_episodes = 1
i = 0
try:
  while i < number_of_episodes:
    state = env.reset()
    done = False
    cummulative_reward = 0
    while not done:
      # env.render()
      action = env.action_space.sample()
      state, reward, done, info = env.step(action)
      # print(state[0].shape)
      cummulative_reward += reward
    print("Episode : {}\nAccumulative Reward : {}".format(i, cummulative_reward))
    i += 1
  env.close()
  vision_from_sky = info['brain_info'].visual_observations[0][0, :, :, :] * 255.0
  im = Image.fromarray(vision_from_sky.astype('uint8'))
  im.save("ceil.jpeg")
  numpy_image = state[0] * 255
  numpy_image = numpy_image.astype('uint8')
  im = Image.fromarray(numpy_image.astype('uint8'))
  im.save("fps.jpeg")
  print(vision_from_sky)
  print("*" * 10)
  print(numpy_image)
except KeyboardInterrupt:
  env.close()

# im = Image.fromarray(numpy_image.astype('uint8'))
# im.save("image.jpeg")
