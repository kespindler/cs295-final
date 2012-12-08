from abc import ABCMeta, abstractmethod
from random import choice
from pybrain.rl.agents import LearningAgent
from numpy import array

class Agent(object):
    __metaclass__ = ABCMeta

    @abstractmethod #@PyBrain calls this getAction()
    def choose_action(self, env, state):
        """choose_action is the policy. changes as we learn the environment.
        Takes in an obs but this state could just be a state."""
        return None # action

    @abstractmethod
    def feedback(self, state, action, reward, state2): 
        """this is the actual learning algorithm. sarsa, q-learning, td, etc."""
        return # doesn't return anything


class Option(object):
    def choose_action(self, env, state):
        pass
    def can_initiate(self, env, state):
        pass
    def is_terminated(self, env, state):
        pass


class RandomAgent(Agent):
    def choose_action(self, env, obs):
        return array([choice(env.actions)])

    def feedback(self, obs, action, reward, obs2): 
        pass
