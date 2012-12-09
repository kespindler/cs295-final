from abc import ABCMeta, abstractmethod
from random import random, choice, randint
from numpy import array, zeros, ones, append, argmax, unravel_index, where
from options2 import KeyOption

class Agent(object):
    __metaclass__ = ABCMeta
    
    def __init__(self):
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
    def feedback(self, state, action, reward, state2, action2 = None):
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
    
    

class StandardAgent(Agent):
    """ Standard agent that learns with SARSA(lambda)
    """
    def __init__(self, stateDesc, actionDesc, 
                    alpha = 0.1, gamma = 0.99, slambda = 0.9, epsilon = 0.01, traceThreshold = 0.0001):
        """ stateDesc gives size of state space (if state space is d-dim, stateDesc is tuple of length d)
            actionDesc gives size of actions space (sized similarly to stateDesc)
            learner is learning algorithm?
            epsilon is for epsilon exploration
        """
        super(StandardAgent, self).__init__()
        self.stateDesc = stateDesc
        self.stateNum = len(self.stateDesc)
        self.actionDesc = actionDesc
        self.actionNum = len(self.actionDesc)
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
        super(StandardAgent, self).choose_action(env, obs)
        # obs = tuple(int(x) for x in obs)[0:len(self.stateDesc)]
        obs = obs[0:self.stateNum]
        i = self.nextAction
        if i == None:
            # Get subtable of actions at given state
            availableActions = self.qTable[obs]
        
            # Choose randomly or greedily?
            if random() > self.epsilon:
                # Greedily choose max; if tie, break randomly
                i = where(availableActions == availableActions.max())
                i = array(choice(zip(*i)))
            else:
                # totally random
                i = array(tuple(randint(0, x-1) for x in self.actionDesc))
        
        self.nextAction = None
        return i
    
    def feedback(self, obs, a, r, nextobs, nexta = None):
        """ Straightforward implementation of SARSALambda, maybe better if moved into subclass?
        """
        # if no next action is given choose one using policy
        if nexta == None:
            nexta = self.choose_action(None, nextobs)
            self.nextAction = nexta
            nexta = tuple(nexta)
        
        # obs = tuple(int(x) for x in obs)[0:len(self.stateDesc)]
        # a = tuple(int(x) for x in a)[0:len(self.actionDesc)]
        # nextobs = tuple(int(x) for x in nextobs)[0:len(self.stateDesc)]
        # nexta = tuple(int(x) for x in nexta)[0:len(self.actionDesc)]
        obs = obs[0:self.stateNum]
        a = tuple(a[0:self.actionNum])
        nextobs = nextobs[0:self.stateNum]
        nexta = nexta[0:self.actionNum]
        
        sa = obs+a
        q = self.qTable[sa]
        qnext = self.qTable[nextobs+nexta]
        
        # update current qvalue for s,a in table
        delta = r + self.gamma * qnext - q
        newq = q + self.alpha * delta
        self.qTable[sa] = newq
        
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
            newq = self.qTable[sa] + self.alpha * delta * eligibility
            self.qTable[sa] = newq
            
            # decay trace, and terminate if trace is negligible
            eligibility *= self.slambda
            if eligibility < self.traceThreshold:
                break
        
        # add new observation
        prevs.append(obs)
        preva.append(a)
    
    def episode_finished(self):
        """ Erase history, but keep qvalues!
        """
        self.observations = [[], []]
        self.nextAction = None
        return super(StandardAgent,self).episode_finished()


class RandomAgent(Agent):
    
    def choose_action(self, env, obs):
        super(RandomAgent, self).choose_action(env, obs)
        return array([choice(env.actions)])

    def feedback(self, obs, action, reward, obs2): 
        pass


class TestOptionAgent(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.options = [KeyOption()]
        self.option = None
        self.room = -1

    def choose_action(self, env, state):
        if self.option is None or self.option.is_terminated(env, state):
            if self.options[0].can_initiate(env, state):
                print "Initiate option"
                self.option = self.options[0]
            else:
                print "option completed"
                return array([choice(env.actions)])
        return self.option.choose_action(env, state)

    def feedback(self, state, action, reward, state2, action2 = None):
        pass

    def episode_finished(self):
        pass

