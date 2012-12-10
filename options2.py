from random import random, choice
from utility import filter_states
from environment import manhattan_dist, expand_state, Lightworld
import search
from numpy import array

class Option2(object):
    epsilon = 0.01
    target_field = None
    final_action = None

    def __init__(self):
        self.plan = None # plan is none or a list of posn-tuples on main path.

    def canInitialize(self, state):
        return self.can_initiate(None, state)

    def canTerminate(self, state):
        return self.is_terminated(None, state)

    def choose_action_parameterized(self, env, state, field, action):
        if self.room != state.r:
            self.room = state.r
            self.plan = None
        pos = (state.x, state.y)
        if self.plan is None or pos not in self.plan:
            key_pos = filter_states(env.states, field)
            # Not positive if this is right move here.
            if not key_pos:
                return array([choice(env.actions)])
            priority_func = lambda s: manhattan_dist(s, key_pos[0])
            expand_partial = lambda s: expand_state(env.states, s)
            self.plan = search.best_first_graph_search(pos, key_pos[0], priority_func, expand_partial)
        for i, pathpos in enumerate(self.plan):
            if i == len(self.plan)-1:
                return array([action])
            elif pos == pathpos:
                fx,fy = self.plan[i+1]
                dx,dy = (fx-state.x, fy-state.y)
                return array([env.movemap[dx,dy]])


class KeyOption(Option2):
    def can_initiate(self, env, state):
        self.room = -1
        return (state.h == 0)

    def is_terminated(self, env, state):
        if random() < self.epsilon:
            return True
        return (state.h == 1)

    def choose_action(self, env, state):
        return self.choose_action_parameterized(env, state, 
                Lightworld.field.KEY, Lightworld.actions.G)

class LockOption(Option2):
    def can_initiate(self, env, state):
        self.room = -1
        return (state.l == 1)

    def is_terminated(self, env, state):
        if random() < self.epsilon:
            return True
        return (state.l == 0)

    def choose_action(self, env, state):
        return self.choose_action_parameterized(env, state, 
                Lightworld.field.LOCK, Lightworld.actions.P)

class DoorOption(Option2):
    def can_initiate(self, env, state):
        self.room = -1
        return (state.l == 1)

    def is_terminated(self, env, state):
        if random() < self.epsilon:
            return True
        return (state.l == 0)

    def choose_action(self, env, state):
        if self.room != state.r:
            self.room = state.r
            self.plan = None
        pos = (state.x, state.y)
        if self.plan is None or pos not in self.plan:
            priority_func = lambda s: manhattan_dist(s, env.goal)
            expand_partial = lambda s: expand_state(env.states, s)
            self.plan = search.best_first_graph_search(pos, env.goal, priority_func, expand_partial)
        for i, pathpos in enumerate(self.plan):
            if i == len(self.plan)-1:
                return array([choice(env.actions)])
            elif pos == pathpos:
                fx,fy = self.plan[i+1]
                dx,dy = (fx-state.x, fy-state.y)
                return array([env.movemap[dx,dy]])


#class OptionAgent2(OptionAgent):
#    def __init__(self):
#        self.cur_option = None
#        self.options = [KeyOption(), LockOption(), DoorOption()]
#
#    def choose_action(self, env, obs):
#        if self.cur_option is not None and self.cur_option.is_terminated(self, env, obs):
#            self.cur_option = None
#        if self.cur_option is None:
#            for o in self.options:
#                if o.can_initiate(self, env, obs):
#                    self.cur_option = o
#                    break
#        return self.cur_option.chhose_action(self, env, state)
#
#    
#    def feedback(self, obs, action, reward, obs2): 
#        return


#KeyOption = make_option(Lightroom.field.KEY, Lightroom.actions.G)
#LockOption = make_option(Lightroom.field.LOCK, Lightroom.actions.I)
## This action can be none since we should never be able to act while on a door.
#DoorOption = make_option(Lightroom.field.DOOR, None)
