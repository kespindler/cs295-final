from abc import ABCMeta, abstractmethod
from random import random, choice, randint, shuffle
import numpy as np
from math import isinf
from collections import deque

""" Default agent super class
    SARSA(lambda) and Random implementations
    Perfect options [I think this should be moved to options2.py - rl]
"""

class Agent(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, state_desc=None):
        self.stepCount = 0
    
    @abstractmethod
    def choose_action(self, env, state):
        """ Returns an action chosen using the agent's learned policy + exploration
            In MDP case, obs is just a state descriptor
            In POMDP, obs is full observation
            obs is a tuple
            :return: action
        """
        self.stepCount += 1
        return None
    
    @abstractmethod
    def feedback(self, state, action, reward, state2, action2 = None, env=None):
        """ Logs feedback from environment in SARSA form with agent
            As usual, obs is just a state in MDPs
            obs and a are tuples, r is a float
        """
        return # no return value
    
    def episode_finished(self):
        """ Resets the agent on end of an episode
            Returns step count
        """
        totalsteps = self.stepCount
        self.stepCount = 0
        return totalsteps
    

class SarsaAgent(Agent):
    """ Standard agent that learns with SARSA(lambda)
    """
    def __init__(self, stateDesc, actionDesc, 
                    alpha = 0.1, gamma = 0.99, slambda = 0.9, epsilon = 0.01, decay = 0.99,
                    traceThreshold = 0.0001):
        """ stateDesc gives size of state space (if state space is d-dim, stateDesc is tuple of length d)
            actionDesc gives size of actions space (sized similarly to stateDesc)
            learner is learning algorithm?
            epsilon is for epsilon exploration, decay is exploration decay rate
        """
        if type(actionDesc) is int:
            actionDesc = (actionDesc,)
        Agent.__init__(self)
        self.stateDesc = stateDesc
        self.stateDim = len(self.stateDesc)
        self.actionDesc = actionDesc
        self.actionDim = len(self.actionDesc)
        self.qTable = np.zeros(stateDesc + actionDesc)
        self.qTable[:] = 500
        self.alpha = alpha
        self.gamma = gamma
        #self.slambda = slambda
        hist_threshold = int(np.log(traceThreshold)/np.log(slambda))
        self.eligibility = np.array([slambda**i for i in range(1,hist_threshold)])
        self.epsilon = epsilon
        self.decay = decay
        #self.traceThreshold = 0.0001
        # observations stores history of SARSA feedback
        #self.observations = [[], []]
        self.prev_states = deque(maxlen=hist_threshold)
        self.prev_actions = deque(maxlen=hist_threshold)
        self.nextAction = None # ensures proper SARSA updates
    
    def choose_action(self, env, obs):
        Agent.choose_action(self, env, obs)
        # obs = tuple(int(x) for x in obs)[0:len(self.stateDesc)]
        obs = obs[:self.stateDim]
        i = self.nextAction
        if i is None:
            # Get subtable of actions at given state
            availableActions = self.qTable[obs]
        
            # Choose randomly or greedily?
            if random() > self.epsilon:
                # Greedily choose max; if tie, break randomly
                i = np.where(availableActions == availableActions.max())
                i = np.array(choice(zip(*i)))
            else:
                # totally random
                i = np.array(tuple(randint(0, x-1) for x in self.actionDesc))
        
        # cleanup
        self.nextAction = None
        self.epsilon *= self.decay
        return i
    
    def feedback(self, obs, a, r, nextobs, nexta = None, env=None):
        """ Straightforward implementation of SARSALambda, maybe better if moved into subclass?
        """
        # if no next action is given choose one using policy
        if nexta is None:
            nexta = self.choose_action(env, nextobs)
            self.nextAction = nexta
            #nexta = tuple(nexta)
        
        obs = obs[:self.stateDim]
        a = tuple(a[:self.actionDim])
        nextobs = nextobs[:self.stateDim]
        nexta = tuple(nexta[:self.actionDim])
        
        sa = obs+a
        q = self.qTable[sa]
        qnext = self.qTable[nextobs+nexta]
        if not isinf(q) and not isinf(qnext):
            
            # update current qvalue for s,a in table
            delta = r + self.gamma * qnext - q
            factor = self.alpha * delta
            newq = q + factor
            self.qTable[sa] = newq
            
            # compute backup
            #prevs = self.observations[0]
            #preva = self.observations[1]
            
            #lnumSamples = len(prevs)
            
            # backup
            #eligibility = self.slambda
            for state, action, elig in zip(self.prev_states, self.prev_actions, self.eligibility):
                sa = state + action
                self.qTable[sa] += factor * elig
                
                #state = prevs[i]
                #action = preva[i]
                
                #newq = self.qTable[sa] + factor * eligibility
                #print self.qTable[sa], factor*elig
                #if not isinf(self.qTable[sa]):
                
                #print zip(*np.where(np.isinf(self.qTable)))
                
                # decay trace, and terminate if trace is negligible
                #eligibility *= self.slambda
                #if eligibility < self.traceThreshold:
                #    break
        
        # add new observation
        self.prev_states.appendleft(obs)
        self.prev_actions.appendleft(a)
        #prevs.append(obs)
        #preva.append(a)
    
    def episode_finished(self):
        """ Erase history, but keep qvalues!
        """
        #self.observations = [[], []]
        self.prev_states.clear()
        self.prev_actions.clear()
        self.nextAction = None
        return Agent.episode_finished(self)


class RandomAgent(Agent):
    """ Selects actions entirely at random
    """
    def choose_action(self, env, obs):
        super(RandomAgent, self).choose_action(env, obs)
        return np.array([choice(env.actions)])

    def feedback(self, obs, action, reward, obs2): 
        pass

#------------------------------------------