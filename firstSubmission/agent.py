import numpy as np

def get_colours(pixels, colour):
  return np.all(pixels > np.minimum(colour*.8, colour-25), axis=-1) & np.all(pixels < np.maximum(colour*1.2, colour+25), axis=-1)

Green = np.array([129.0, 191.0, 65.0])
Yellow = np.array([100.0, 65.0, 5.0])
Red = np.array([185.0, 50.0, 50.0])


class Agent(object):

    def __init__(self):
        """
         Load your agent here and initialize anything needed
        """
        self.skipped_frames = 5
        self.counter = 0
        self.action = None
        self.directions = {
          "nothing" : 0,
          "forward" : 1,
          "backward" : 2,
          "right" : 1,
          "left" : 2,
        }
    def reset(self, t=250):
        """
        Reset is called before each episode begins
        Leave blank if nothing needs to happen there
        :param t the number of timesteps in the episode
        """
        self.counter = 0

    def step(self, obs, reward, done, info):
        """
        :param obs: agent's observation of the current environment
        :param reward: amount of reward returned after previous action
        :param done: whether the episode has ended.
        :param info: contains auxiliary diagnostic information, including BrainInfo.
        :return: the action to take, a list or size 2
        """
        # if self.counter == self.skipped_frames: self.counter = 0
        # if self.counter != 0: return self.action
        # self.counter += 1
        first = self.directions["forward"]
        second = 0
        num_of_left_green_pix = 0
        num_of_right_green_pix = 0
        num_of_left_red_pix = 0
        num_of_right_red_pix = 0
        num_of_right_yellow_pix = 0
        num_of_left_yellow_pix = 0
        numpy_image = obs[0] * 255
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
            second = self.directions["right"]
        if num_of_right_red_pix > num_of_right_yellow_pix + num_of_right_green_pix:
            second = self.directions["left"]
        # move to the left if there is some good stuff on the left
        if num_of_left_yellow_pix + num_of_left_green_pix > \
            num_of_right_yellow_pix + num_of_right_green_pix:
            second = self.directions["left"]
        # move to the right if there is some good stuff on the right
        elif num_of_left_yellow_pix + num_of_left_green_pix > \
            num_of_right_yellow_pix + num_of_right_green_pix:
            second = self.directions["right"]
        else:
            second = self.directions["right"]
            first = self.directions["nothing"]
        self.action = [first, second]
        return self.action
