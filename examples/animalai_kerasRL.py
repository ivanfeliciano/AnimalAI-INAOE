from __future__ import division
import argparse
import random

from PIL import Image
import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Convolution2D, Permute
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from rl.callbacks import FileLogger, ModelIntervalCheckpoint


from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig

INPUT_SHAPE = (84, 84)
WINDOW_LENGTH = 4
worker_id = random.randint(1, 100)


class AnimalAIProcessor(Processor):
    def process_observation(self, observation):
        assert observation[0].ndim == 3  # (height, width, channel)
        numpy_image = observation[0] * 255
        numpy_image = numpy_image.astype('uint8')
        img = Image.fromarray(numpy_image)
        img = img.resize(INPUT_SHAPE).convert('L')  # resize and convert to grayscale
        processed_observation = np.array(img)
        assert processed_observation.shape == INPUT_SHAPE
        return processed_observation.astype('uint8')  # saves storage in experience memory

    def process_state_batch(self, batch):
        # We could perform this processing step in `process_observation`. In this case, however,
        # we would need to store a `float32` array instead, which is 4x more memory intensive than
        # an `uint8` array. This matters if we store 1M observations.
        processed_batch = batch.astype('float32') / 255.
        return processed_batch

    def process_action(self, action):
        actions_list = [(0, 0), (0, 1),
                        (0, 2), (1, 0),
                        (2, 0)]
        return np.array(actions_list[action])
    def process_info(self, info):
        return {}


parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['train', 'test'], default='train')
parser.add_argument('--weights', type=str, default=None)
parser.add_argument('--config-file', type=str, default=None)
args = parser.parse_args()
arena_config_in = ArenaConfig(args.config_file)

# Get the environment and extract the number of ENV_NAME
ENV_NAME = "AnimalAIEnv"
env = AnimalAIEnv(environment_filename='../env90deg/AnimalAILinux',
                  worker_id=worker_id,
                  n_arenas=1,
                  arenas_configurations=arena_config_in,
                  docker_training=False,
                  retro=False)

np.random.seed(123)
env.seed(123)
nb_actions = 5

# Next, we build our model. We use the same model that was described by Mnih et al. (2015).
input_shape = (WINDOW_LENGTH,) + INPUT_SHAPE
print(input_shape)
model = Sequential()
# if K.common.image_dim_ordering() == 'tf':
#     # (width, height, channels)
model.add(Permute((2, 3, 1), input_shape=input_shape))
model.add(Convolution2D(32, (8, 8), strides=(4, 4)))
model.add(Activation('relu'))
model.add(Convolution2D(64, (4, 4), strides=(2, 2)))
model.add(Activation('relu'))
model.add(Convolution2D(64, (3, 3), strides=(1, 1)))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

memory = SequentialMemory(limit=1000000, window_length=WINDOW_LENGTH)
processor = AnimalAIProcessor()

policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
                              nb_steps=1000000)

dqn = DQNAgent(model=model, nb_actions=nb_actions, policy=policy, memory=memory,
               processor=processor, nb_steps_warmup=50000, gamma=.99, target_model_update=10000,
               train_interval=4, delta_clip=1.)
dqn.compile(Adam(lr=.00025), metrics=['mae'])

if args.mode == 'train':
    weights_filename = './models/dqn_{}_weights.h5f'.format(ENV_NAME)
    checkpoint_weights_filename = './models/dqn_' + ENV_NAME + '_weights_{step}.h5f'
    log_filename = './models/dqn_{}_log.json'.format(ENV_NAME)
    callbacks = [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=1000)]
    callbacks += [FileLogger(log_filename, interval=100)]
    dqn.fit(env, callbacks=callbacks, nb_steps=10000, log_interval=100)

    # After training is done, we save the final weights one more time.
    dqn.save_weights(weights_filename, overwrite=True)

    # Finally, evaluate our algorithm for 10 episodes.
    dqn.test(env, nb_episodes=1, visualize=True)
elif args.mode == 'test':
    weights_filename = './models/dqn_{}_weights.h5f'.format(ENV_NAME)
    if args.weights:
        weights_filename = args.weights
    dqn.load_weights(weights_filename)
    dqn.test(env, nb_episodes=10, visualize=True)
