from pylov.agent import OptionAgent
from pylov.environments import Lightroom


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

class LightroomOptionCreator(self):
    def __init__(self, field, action):
        self.field = field
        self.action = action
        self.filtered_states = filter_states(env, self.field)

    def choose_action(self, env, state):
        key_state = self.filtered_states[0]
        if state == key_state:
            return self.action
        else:
            x,y = state
            kx,ky = key_state
            assert (dx || dy)
            return next_step(kx-x,kx-y)
                
    def can_initiate(self, env, state):
        return bool(len(self.filtered_states))

    def is_terminated(self, env, state):
        # This is just opposite condition as can_initiate.
        # We can start option when there is a key, we can stop when there's no key.
        return not self.can_initiate(env, state)

PickUpKeyOption = LightroomOptionCreator(Lightroom.field.KEY, Lightroom.actions.G)
UnlockLockOption = LightroomOptionCreator(Lightroom.field.LOCK, 
        Lightroom.actions.I)
# This action can be none since we should never be able to act while on a door.
GotoDoorOption = LightroomOptionCreator(Lightroom.field.DOOR, None)
