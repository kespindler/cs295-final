from abc import ABCMeta, abstractmethod
from random import choice
from pybrain.rl.agents import LearningAgent
from numpy import array

class Agent(object):
    __metaclass__ = ABCMeta

    @abstractmethod #@PyBrain calls this getAction()
    def choose_action(self, env, obs):
        """choose_action is the policy. changes as we learn the environment.
        Takes in an obs but this state could just be a state."""
        return None # action

    #in most cases the obs is just the cur state. maybe? need to make sure this generalizes..
    # in the pomdp case, (state, action, reward, state) just become (obs, ., ., obs)
    # and we indeed need different agents for pomdp, so we're okay there.
    @abstractmethod # @PyBrain calls this learn
    def feedback(self, obs, action, reward, obs2): 
        """this is the actual learning algorithm. sarsa, q-learning, td, etc."""
        return # doesn't return anything


class Option(object):
    def choose_action(self, env, state):
        pass
    def can_initiate(self, env, state):
        pass
    def is_terminated(self, env, state):
        pass


class OptionAgent(object):
    __metaclass__ = ABCMeta
    def __init__(self):
        self.cur_option = None
        self.options = []


class RandomAgent(Agent):
    def choose_action(self, env, obs):
        return array([choice(env.actions)])

    def feedback(self, obs, action, reward, obs2): 
        pass

class BridgeAgent(Agent):
    def __init__(self, controller, alg):
        controller.initialize(1.) #this is a hack perhaps?
        # seems like that step should be done by the pybrain agent...
        self.pyb_agent = LearningAgent(controller, alg)

    def choose_action(self, env, state):
        self.pyb_agent.integrateObservation(state)
        return self.pyb_agent.getAction()

    def feedback(self, state, action, reward, state2): 
        """this is the actual learning algorithm. sarsa, q-learning, td, etc."""
        self.pyb_agent.giveReward(reward)
        # more stuff that perhaps shouldn't be included but what can you do?
        self.pyb_agent.learn()
        self.pyb_agent.reset()
