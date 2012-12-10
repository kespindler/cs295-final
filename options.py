from utility import enum
from random import random

class Option(SarsaAgent):
    """ Option
        Core learning uses standard agent to track qvalues, run SARSA(lambda)
        Only additions are initialization and termination sets
    """
    epsilon = .01

class KeyOption(Option):
    def canTerminate(self, state):
        if random() < self.epsilon:
            return True
        return (state.h == 1)

    def canInitialize(self, state):
        return (state.h == 0) # Maybe want to modify this?


class LockOption(Option):
    def canTerminate(self, state):
        if random() < self.epsilon:
            return True
        return (state.l == 0)

    def canInitialize(self, state):
        return (state.l == 1)# Maybe want to modify this.


class DoorOption(Option):
    def canTerminate(self, state):
        if random() < self.epsilon:
            return True
        return (state.r > self.last_room)

    def canInitialize(self, state):
        self.last_room = 0
        return True # Maybe want to modify this.

class OptionsAgent(SarsaAgent):
    numOptions = 3
    options = enum(KEY=0,LOCK=1,DOOR=2)
    
    def __init__(self, stateDesc, actionDesc):
        super(OptionAgent, self).__init__(stateDesc, numOptions)
        # TODO: set up option init and terminate
        self.options = [
            KeyOption(stateDesc, actionDesc),
            LockOption(stateDesc, actionDesc),
            DoorOption(stateDesc, actionDesc)
        ]
        self.currentOption = None
        self.currentOptionName = None
    
    def choose_action(self, env, obs):
        """ Choose option from meta-policy if no option is chosen
            Then choose action from option
        """
        # Check if option has terminated
        if (self.currentOption != None 
            && self.currentOption.terminate(obs)):
            self.currentOption = None
            self.currentOptionName = None
        
        # choose option
        while self.currentOption == None:
            next = None
            next = super(OptionAgent, self).choose_action(env, obs)
            self.currentOptionKey = next
            self.currentOption = self.options[next]
            # Check that option is initializable
            if not self.currentOption.canInitialize(obs):
                # if it is not set its qvalue so it is never picked again
                self.qTable[obs + tuple(next)] = float("-inf")
                next = None
                self.currentOptionName = None
                self.currentOption = None
        
        # get action
        return self.currentOption.choose_action(env, obs)
    
    # TODO I think this needs to be taken out...
    def shapeReward(self, obs, r, nextobs):
        """ Shape reward based on current option
        """
        optr = -1 # default step cost
        if self.currentOptionName == 'Key':
            if obs[3] == 0 && nextobs[3] == 1:
                optr = 100
            # check if key has been picked up
        elif self.currentOptionName == 'lock':
            # check if door is unlocked
            if obs[4] == 0 && nextobs[4] == 1:
                optr = 100
        elif self.currentOptionName == 'door':
            # check if room has changed
            if obs[0] != nextobs[0]:
                optr = 100
        
        return optr
        
    
    def feedback(self, obs, a, r, nextobs, nexta = None):
        if self.currentOption != None:
            optr = self.shapeReward(obs, r, nextobs)
            self.currentOption.feedback(obs,a,optr,nextobs,nexta)
            
            #
            nexta = self.currentOptionKey
            
            # check if state terminates
            if self.currentOption.terminate(obs):
                self.currentOption = None
                self.currentOptionName = None
                nexta = None # force it to choose egreedily
        
            super(OptionAgent, self).feedback(obs, self.currentOptionKey, r, nextobs, nexta)
        
        return
    
    def episode_finished(self):
        """ Reset options in addition to resetting self
        """
        o.episode_finished() for o in self.options
        return super(OptionAgent, self).episode_finished()

# from pylov.agent import OptionAgent, Option
# from pylov.lightroom import Lightroom
# from pylov.environment import filter_states
# 

