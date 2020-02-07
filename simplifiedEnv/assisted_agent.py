import numpy as np
import cv2

from rl.agents.dqn import DQNAgent


def get_colours(pixels, colour):
  return np.all(pixels > np.minimum(colour*.8, colour-25), axis=-1) & np.all(pixels < np.maximum(colour*1.2, colour+25), axis=-1)


def count_pixels(img, colour):
	ans = 0
	for x in range(len(img)):
		for y in range(len(img)):
				if get_colours(img[x, y], colour):
					return True
	return False

Green = np.array([129.0, 191.0, 65.0])
Yellow = np.array([100.0, 65.0, 5.0])
Red = np.array([185.0, 50.0, 50.0])

class AssistedAgent(DQNAgent):
	"""docstring for AssistedAgent"""
	def forward(self, observation):
		# Select an action.
		state = self.memory.get_recent_state(observation)
		q_values = self.compute_q_values(state)
		if self.training:
			if count_pixels(observation, Green):
				action = 3
			else:
				action = self.policy.select_action(q_values=q_values)
		else:
			action = self.test_policy.select_action(q_values=q_values)

		# Book-keeping.
		self.recent_observation = observation
		self.recent_action = action
		return action
		