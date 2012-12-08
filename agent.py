from abc import ABCMeta, abstractmethod
from random import random, choice, randint
from numpy import array, zeros, ones, append, argmax, unravel_index

class Agent(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def choose_action(self, env, obs):
        """ Returns an action chosen using the agent's learned policy + exploration
            In MDP case, obs is just a state descriptor
            In POMDP, obs is full observation
            obs is a tuple
            :return: action
        """
        return None
    
    @abstractmethod
    def feedback(self, obs, a, r, nextobs, nexta = None):
        """ Logs feedback from environment in SARSA form with agent
            As usual, obs is just a state in MDPs
            obs and a are tuples, r is a float
        """
        return # no return value

class StandardAgent(Agent):
    """ Standard agent that learns with SARSA(lambda)
    """
    def __init__(self, stateDesc, actionDesc, alpha = 0.1, gamma = 0.99, slambda = 0.9, epsilon = 0.01, traceThreshold = 0.0001):
        """ stateDesc gives size of state space (if state space is d-dim, stateDesc is tuple of length d)
            actionDesc gives size of actions space (sized similarly to stateDesc)
            learner is learning algorithm?
            epsilon is for epsilon exploration
        """
        self.stateDesc = stateDesc
        self.actionDesc = actionDesc
        self.qTable = zeros(stateDesc + actionDesc)
        self.alpha = alpha
        self.gamma = gamma
        self.slambda = slambda
        self.epsilon = epsilon
        self.traceThreshold = 0.0001
        # observations stores history of SARSA feedback
        self.observations = [[], []]
        self.nextAction = None # ensures proper SARSA updates
    
    def choose_action(self, env, obs):
        i = self.nextAction
        if i == None:
            # Get subtable of actions at given state
            availableActions = self.qTable[obs]
        
            # Choose randomly or greedily?
            if random() > self.epsilon:
                # greedy
                #Choose max; if tie, choose randomly
                i = argmax(availableActions)
                i = choice(unravel_index(i, self.actionDesc))
            else:
                # random
                i = tuple(randint(0, x-1) for x in self.actionDesc)
        
        self.nextAction = None
        return i
    
    def feedback(self, obs, a, r, nextobs, nexta = None):
        """ Straightforward implementation of SARSALambda, maybe better if moved into subclass?
        """
        # if no next action is given choose one using policy
        if nexta == None:
            nexta = self.choose_action(nextobs)
            self.nextAction = nexta
        
        q = self.qTable[obs+a]
        qnext = self.qTable[nextobs+nexta]
        
        # update current qvalue for s,a in table
        delta = r + self.gamma * qnext - q
        newq = q + self.alpha * delta
        self.qTable[obs+a] = newq
        
        # compute backup
        prevs = self.observations[0]
        preva = self.observations[1]
        
        numSamples = len(prevs)
        
        # backup
        eligibility = self.slambda
        for i in range(numSamples-1, 0, -1):
            state = prevs[i]
            action = preva[i]
            
            sa = state + action
            newq = self.qTable(sa) + self.alpha * delta * eligibility
            self.qTable(sa) = newq
            
            # decay trace, and terminate if trace is negligible
            eligibility *= self.slambda
            if eligibility < self.traceThreshold:
                break
        
        # add new observation
        prevs.append(obs)
        preva.append(a)

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