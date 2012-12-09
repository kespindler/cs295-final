class Option(StandardAgent):
    """ Option
        Core learning uses standard agent to track qvalues, run SARSA(lambda)
        Only additions are initialization and termination sets
    """
    
    def __init__(self, stateDesc, actionDesc, init, terminate):
        """ init and terminate are functions
        """
        super(Option, self).__init__(stateDesc, actionDesc)
        self.init = init
        self.terminate = terminate
    
    def canInitialize(self, obs):
        return init(obs)
    
    def terminate(self, obs):
        return terminate(obs)

class OptionsAgent(StandardAgent):
    numOptions = 3
    options = enum(KEY=0,LOCK=1,DOOR=2)
    
    def __init__(self, stateDesc, actionDesc):
        super(OptionAgent, self).__init__(stateDesc, numOptions)
        # TODO: set up option init and terminate
        self.options = [
            Option(stateDesc, actionDesc, keyInit, keyTerminate), # key
            Option(stateDesc, actionDesc, lockInit, lockTerminate), # lock
            Option(stateDesc, actionDesc, doorInit, doorTerminate) # door
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
            if !self.currentOption.canInitialize(obs):
                # if it is not set its qvalue so it is never picked again
                self.qTable[obs + tuple(next)] = float("-inf")
                next = None
                self.currentOptionName = None
                self.currentOption = None
        
        # get action
        return self.currentOption.choose_action(env, obs)
    
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
# def next_step(dx,dy):
#     if dx>0:
#         action = Lightroom.actions.E
#     elif dx<0:
#         action = Lightroom.actions.W
#     elif dy>0:
#         action = Lightroom.actions.S
#     elif dy<0:
#         action = Lightroom.actions.N
#     return action
# 
# def make_option(a_field, an_action):
#     class LightroomOption(Option):
#         field = a_field
#         action = an_action
# 
#         def choose_action(self, env, state):
#             filtered_states = filter_states(env, self.field)
#             key_state = filtered_states[0]
#             if state == key_state:
#                 return action
#             else:
#                 x,y = state
#                 kx,ky = key_state
#                 assert (dx or dy)
#                 return next_step(kx-x,kx-y)
#                     
#         def can_initiate(self, env, state):
#             return bool(len(filtered_states))
# 
#         def is_terminated(self, env, state):
#             # This is just opposite condition as can_initiate.
#             # We can start option when there is a key, we can stop when there's no key.
#             return not self.can_initiate(env, state)
#     return LightroomOption
# 
# class OptionAgent2(OptionAgent):
#     def __init__(self):
#         self.cur_option = None
#         self.options = [KeyOption(), LockOption(), DoorOption()]
# 
#     def choose_action(self, env, obs):
#         if self.cur_option is not None and self.cur_option.is_terminated(self, env, obs):
#             self.cur_option = None
#         if self.cur_option is None:
#             for o in self.options:
#                 if o.can_initiate(self, env, obs):
#                     self.cur_option = o
#                     break
#         return self.cur_option.chhose_action(self, env, state)
# 
#     
#     def feedback(self, obs, action, reward, obs2): 
#         return
# 
# 
# KeyOption = make_option(Lightroom.field.KEY, Lightroom.actions.G)
# LockOption = make_option(Lightroom.field.LOCK, Lightroom.actions.I)
# # This action can be none since we should never be able to act while on a door.
# DoorOption = make_option(Lightroom.field.DOOR, None)
