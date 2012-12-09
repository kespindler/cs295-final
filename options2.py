from random import random, choice

def make_option(a_field, an_action):
    class LightroomOption(Option):
        field = a_field
        action = an_action

        def is_terminated(self, env, state):
            pass

        canTerminate = is_terminated

        def can_initiate(self, env, state):
            pass

        canInitialize = can_initiate

class Option2(object):
    epsilon = 0.01
    def __init__(self):
        self.plan = None # plan is none or a list of posn-tuples on main path.

class KeyOption(Option2):
    def can_initiate(self, env, state):
        return (state.h == 0)

    def canInitialize(self, state):
        return self.can_initiate(None, state)

    def is_terminated(self, env, state):
        if random() < self.epsilon:
            return True
        return (state.h == 1)

    def canTerminate(self, state):
        return self.is_terminated(None, state)

    def choose_action(self, env, state):
        pos = (state.x, state.y)
        if self.plan is None or pos not in self.plan:
            key_pos = filter_states(env.states, env.field.KEY)
            # Not positive if this is right move here.
            if not key_pos:
                return choice(env.actions)
            priority_func = lambda s: manhattan_dist(s, env.goal)
            expand_partial = lambda s: expand_state(env.states, s)
            self.plan = search.best_first_graph_search(state, key_pos[0], priority_func, expand_partial)
        for i, pathpos in enumerate(self.plan):
            if i == len(self.plan)-1:
                return Lightworld.action.G
            elif pos == pathpos:
                fx,fy = pathpos
                dx,dy = (fx-state.x, fy-state.y)
                return env.movemap[dx,dy]

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


#KeyOption = make_option(Lightroom.field.KEY, Lightroom.actions.G)
#LockOption = make_option(Lightroom.field.LOCK, Lightroom.actions.I)
## This action can be none since we should never be able to act while on a door.
#DoorOption = make_option(Lightroom.field.DOOR, None)
