'''
Created on Aug 18, 2016

@author: rbhat
'''
import numpy as np
import gym

from keras.layers import Dense, Dropout, Activation, Flatten, Reshape
from keras.layers import Convolution1D, MaxPooling1D, Convolution2D, MaxPooling2D

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, merge, Embedding
from keras.optimizers import RMSprop

from com.rl.continous.keras.ddpg import DDPGAgent
from com.rl.continous.keras.memory import SequentialMemory
from com.rl.continous.keras.Random1 import OrnsteinUhlenbeckProcess


#ENV_NAME = 'CarRacing-v0'
ENV_NAME = 'Pendulum-v0'
gym.undo_logger_setup()



# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
assert len(env.action_space.shape) == 1
nb_actions = env.action_space.shape[0]

# Next, we build a very simple model.
actor = Sequential()
actor.add(Flatten(input_shape=(1,) + env.observation_space.shape))
actor.add( Reshape( (3, 1) ) )
actor.add(Convolution1D(8, 1, border_mode='valid'))
actor.add(Flatten())
#actor.add(Dense(16))
#actor.add(Activation('relu'))
#actor.add(Dense(16))
#actor.add(Activation('relu'))
actor.add(Dense(16))
actor.add(Activation('relu'))
actor.add(Dense(nb_actions))
actor.add(Activation('linear'))
print(actor.summary())

action_input = Input(shape=(nb_actions,), name='action_input')
observation_input = Input(shape=(1,) + env.observation_space.shape, name='observation_input')
flattened_observation = Flatten()(observation_input)
x = merge([action_input, flattened_observation], mode='concat')
x = Reshape((4, 1))(x)
x = Convolution1D(8, 1, border_mode='valid')(x)
x = Flatten()(x)
#x = Dense(32)(x)
#x = Activation('relu')(x)
#x = Dense(32)(x)
#x = Activation('relu')(x)
x = Dense(32)(x)
x = Activation('relu')(x)
x = Dense(1)(x)
x = Activation('linear')(x)
critic = Model(input=[action_input, observation_input], output=x)
print(critic.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=100000)
random_process = OrnsteinUhlenbeckProcess(theta=.15, mu=0., sigma=.3)
agent = DDPGAgent(nb_actions=nb_actions, actor=actor, critic=critic, critic_action_input=action_input,
                  memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                  random_process=random_process, gamma=.99, target_model_update=1e-3,
                  delta_range=(-10., 10.))
agent.compile([RMSprop(lr=.001), RMSprop(lr=.001)], metrics=['mae'])

#agent.load_weights('ddpg_{}_weights.h5f'.format(ENV_NAME))

#env.reset()
#env.render()

#env.monitor.start('/home/rahul/S3Lab/Keras-RL/keras-rl/pendulumvids7')
# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
agent.fit(env, nb_steps=100000, visualize=True, verbose=1, nb_max_episode_steps=200) #True

env.monitor.close()

# After training is done, we save the final weights.
agent.save_weights('ddpg7_{}_weights.h5f'.format(ENV_NAME), overwrite=False)

# Finally, evaluate our algorithm for 5 episodes.
agent.test(env, nb_episodes=5, visualize=True, nb_max_episode_steps=200)
