from agent import SarsaAgent
from gradient_descent import GradientDescentSarsaAgent
from random import random
from utility import enum
from options import ActionOption
from numpy import array

class COption(GradientDescentSarsaAgent):
    """ Agent Option
        Core learning uses standard agent to track qvalues, run SARSA(lambda)
        Only additions are initialization and termination sets
    """
    opt_epsilon = .01

class KeyCOption(COption):
    def canTerminate(self, state):
        if random() < COption.opt_epsilon:
            return True
        return (state.h == 1)

    def canInitialize(self, state):
        return (state.h == 0) # Maybe want to modify this?


class LockCOption(COption):
    def canTerminate(self, state):
        if random() < COption.opt_epsilon:
            return True
        return (state.l == 0)

    def canInitialize(self, state):
        return (state.l == 1)# Maybe want to modify this.


class DoorCOption(COption):
    def canTerminate(self, state):
        if random() < COption.opt_epsilon:
            return True
        return (state.r != self.last_room)

    def canInitialize(self, state):
        if state.l == 0:
            self.last_room = state.r
            return True # Maybe want to modify this.



class COptionAgent(SarsaAgent):
    """ Learns over Agent options
    """
    optionEnum = enum(KEY=0, LOCK=1, DOOR=2)
    optionReward = 10
    
    def __init__(self, stateDesc, agentStateOffset, actionDesc):
        stateDim = len(stateDesc) - agentStateOffset
        self.options = [
            KeyCOption(stateDim, agentStateOffset, actionDesc),
            LockCOption(stateDim, agentStateOffset, actionDesc),
            DoorCOption(stateDim, agentStateOffset, actionDesc),
            # ActionOption(array([0])),
            # ActionOption(array([1])),
            # ActionOption(array([2])),
            # ActionOption(array([3])),
            # ActionOption(array([4])),
            # ActionOption(array([5])),
        ]
        super(COptionAgent, self).__init__(stateDesc[:agentStateOffset], (len(self.options),))
        self.currentOption = None
        self.currentOptionKey = None
    
    def choose_action(self, env, obs):
        o = obs[:self.stateDim]
        
        if (self.currentOption is not None
            and self.currentOption.canTerminate(obs)):
            self.currentOption = None
            self.currentOptionKey = None
        
        # choose option
        while self.currentOption is None:
            self.currentOptionKey = super(COptionAgent, self).choose_action(env, obs)
            self.currentOption = self.options[self.currentOptionKey]
            # Check that option is initializable
            if not self.currentOption.canInitialize(obs):
                # if it is not set its qvalue so it is never picked again
                self.qTable[o + tuple(self.currentOptionKey)] = float("-inf")
                self.currentOptionKey = None
                self.currentOption = None
        
        return self.currentOption.choose_action(env, obs)
    
    def shapeReward(self, obs, r, nextobs):
        """ Shape reward based on current option
        """
        optr = -1 # default step cost
        
        # check if key is picked up
        if obs.h == 0 and nextobs.h == 1 and self.currentOptionKey == COptionAgent.optionEnum.KEY:
            optr = COptionAgent.optionReward
        # check if door is unlocked
        elif obs.l == 1 and nextobs.l == 0 and self.currentOptionKey == COptionAgent.optionEnum.LOCK:
            optr = COptionAgent.optionReward
        # check if room has changed
        elif obs.r != nextobs.r and self.currentOptionKey == COptionAgent.optionEnum.DOOR:
            optr = COptionAgent.optionReward
        
        return optr
    
    def feedback(self, obs, a, r, nextobs, nexta = None, env=None):
        if self.currentOption is not None:
            # update current option
            optr = self.shapeReward(obs, r, nextobs)
            self.currentOption.feedback(obs,a,optr,nextobs,nexta,env)
            
            # update problem option
            # self.options[a[0]+3].feedback(obs,a,optr,nextobs,nexta,env)
            
            # update metapolicy
            a = self.currentOptionKey
            nexta = self.currentOptionKey
            super(COptionAgent, self).feedback(obs, self.currentOptionKey, r, nextobs, nexta,env)
    
    def episode_finished(self):
        """ Reset options in addition to resetting self
            Note: value returned is number of times an option is picked
        """
        for opt in self.options:
            opt.episode_finished()
        self.currentOption = None
        self.currentOptionKey = None
        return super(COptionAgent, self).episode_finished()