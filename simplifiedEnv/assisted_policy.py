import random
import numpy as np

from rl.policy import EpsGreedyQPolicy

def get_colours(pixels, colour):
  return np.all(pixels > np.minimum(colour*.8, colour-25), axis=-1) & np.all(pixels < np.maximum(colour*1.2, colour+25), axis=-1)

Green = np.array([129.0, 191.0, 65.0])
Yellow = np.array([215,165,60])
def count_pixels(img, colour):
	ans = 0
	type(img)
	for x in range(len(img)):
		for y in range(len(img)):
			if get_colours(img[x, y], colour):
				return True
	return False

class AssistedPolicy(EpsGreedyQPolicy):
	def select_action(self, q_values, observation):
		assert q_values.ndim == 1
		nb_actions = q_values.shape[0]
		if count_pixels(observation, Green):
			action = 3
		if np.random.uniform() < self.eps:
			action = np.random.randint(0, nb_actions)
		else:
			action = np.argmax(q_values)
		return action