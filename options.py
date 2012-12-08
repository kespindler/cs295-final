from pylov.agent import OptionAgent, Option
from pylov.lightroom import Lightroom
from pylov.environment import filter_states

def next_step(dx,dy):
    if dx>0:
        action = Lightroom.actions.E
    elif dx<0:
        action = Lightroom.actions.W
    elif dy>0:
        action = Lightroom.actions.S
    elif dy<0:
        action = Lightroom.actions.N
    return action

def make_option(a_field, an_action):
    class LightroomOption(Option):
        field = a_field
        action = an_action

        def choose_action(self, env, state):
            filtered_states = filter_states(env, self.field)
            key_state = filtered_states[0]
            if state == key_state:
                return action
            else:
                x,y = state
                kx,ky = key_state
                assert (dx or dy)
                return next_step(kx-x,kx-y)
                    
        def can_initiate(self, env, state):
            return bool(len(filtered_states))

        def is_terminated(self, env, state):
            # This is just opposite condition as can_initiate.
            # We can start option when there is a key, we can stop when there's no key.
            return not self.can_initiate(env, state)
    return LightroomOption

class OptionAgent2(OptionAgent):
    def __init__(self):
        self.cur_option = None
        self.options = [KeyOption(), LockOption(), DoorOption()]

    def choose_action(self, env, obs):
        if self.cur_option is not None and self.cur_option.is_terminated(self, env, obs):
            self.cur_option = None
        if self.cur_option is None:
            for o in self.options:
                if o.can_initiate(self, env, obs):
                    self.cur_option = o
                    break
        return self.cur_option.chhose_action(self, env, state)

    
    def feedback(self, obs, action, reward, obs2): 
        return


KeyOption = make_option(Lightroom.field.KEY, Lightroom.actions.G)
LockOption = make_option(Lightroom.field.LOCK, Lightroom.actions.I)
# This action can be none since we should never be able to act while on a door.
DoorOption = make_option(Lightroom.field.DOOR, None)
