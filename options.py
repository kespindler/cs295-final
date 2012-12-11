from utility import enum
from random import random
from agent import SarsaAgent

class Option(SarsaAgent):
    """ Option
        Core learning uses standard agent to track qvalues, run SARSA(lambda)
        Only additions are initialization and termination sets
    """
    opt_epsilon = .01

class KeyOption(Option):
    def canTerminate(self, state):
        if random() < Option.opt_epsilon:
            return True
        return (state.h == 1)

    def canInitialize(self, state):
        return (state.h == 0) # Maybe want to modify this?


class LockOption(Option):
    def canTerminate(self, state):
        if random() < Option.opt_epsilon:
            return True
        return (state.l == 0)

    def canInitialize(self, state):
        return (state.l == 1)# Maybe want to modify this.


class DoorOption(Option):
    def canTerminate(self, state):
        if random() < Option.opt_epsilon:
            return True
        return (state.r > self.last_room)

    def canInitialize(self, state):
        self.last_room = 0
        return True # Maybe want to modify this.

class OptionAgent(SarsaAgent):
    optionReward = 100 # shaped reward given to option
    optionEnum = enum(KEY=0, LOCK=1, DOOR=2)
    
    def __init__(self, stateDesc, actionDesc):
        self.options = [
            KeyOption(stateDesc, actionDesc),
            LockOption(stateDesc, actionDesc),
            DoorOption(stateDesc, actionDesc)
        ]
        super(OptionAgent, self).__init__(stateDesc, len(self.options))
        # TODO: set up option init and terminate
        self.currentOption = None
        self.currentOptionKey = None
    
    def choose_action(self, env, obs):
        """ Choose option from meta-policy if no option is chosen
            Then choose action from option
            Note - step count returned
        """
        o = obs[:self.stateDim]
        # Check if option has terminated
        if (self.currentOption is not None 
            and self.currentOption.canTerminate(obs)):
            self.currentOption = None
            self.currentOptionKey = None
        
        # choose option
        while self.currentOption is None:
            self.currentOptionKey = super(OptionAgent, self).choose_action(env, obs)
            self.currentOption = self.options[self.currentOptionKey]
            # Check that option is initializable
            if not self.currentOption.canInitialize(obs):
                # if it is not set its qvalue so it is never picked again
                self.qTable[o + tuple(self.currentOptionKey)] = float("-inf")
                self.currentOptionKey = None
                self.currentOption = None
        
        # get action
        return self.currentOption.choose_action(env, obs)
    
    def shapeReward(self, obs, r, nextobs):
        """ Shape reward based on current option
        """
        optr = -1 # default step cost
        
        # check if key is picked up
        if obs.h == 0 and nextobs.h == 1 and self.currentOptionKey == OptionAgent.optionEnum.KEY:
            optr = OptionAgent.optionReward
        # check if door is unlocked
        elif obs.l == 1 and nextobs.l == 0 and self.currentOptionKey == OptionAgent.optionEnum.LOCK:
            optr = OptionAgent.optionReward
        # check if room has changed
        elif obs.r != nextobs.r and self.currentOptionKey == OptionAgent.optionEnum.DOOR:
            optr = OptionAgent.optionReward
        
        return optr
        
    def feedback(self, obs, a, r, nextobs, nexta = None):
        if self.currentOption is not None:
            # update current option
            optr = self.shapeReward(obs, r, nextobs)
            self.currentOption.feedback(obs,a,optr,nextobs,nexta)
            
            # update metapolicy
            a = self.currentOptionKey
            nexta = self.currentOptionKey
            super(OptionAgent, self).feedback(obs, self.currentOptionKey, r, nextobs, nexta)
    
    def episode_finished(self):
        """ Reset options in addition to resetting self
            Note: value returned is number of times an option is picked
        """
        for opt in self.options:
            opt.episode_finished()
        return super(OptionAgent, self).episode_finished()

# from pylov.agent import OptionAgent, Option
# from pylov.lightroom import Lightroom
# from pylov.environment import filter_states
# 
