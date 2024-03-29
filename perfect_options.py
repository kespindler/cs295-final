from random import random, choice
from utility import filter_states
from environment import manhattan_dist, expand_state, Lightworld
from agent import SarsaAgent
import search
import numpy as np

class Option2(object):
    epsilon = 0.05
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
                #print 'RANDOM action for plan', action
                return np.array([choice(env.actions)])
            priority_func = lambda s: manhattan_dist(s, key_pos[0])
            expand_partial = lambda s: expand_state(env.states, s)
            self.plan = search.best_first_graph_search(pos, key_pos[0], priority_func, expand_partial)
        for i, pathpos in enumerate(self.plan):
            if i == len(self.plan)-1:
                #print 'action', action, 'for plan', field
                return np.array([action])
            elif pos == pathpos:
                fx,fy = self.plan[i+1]
                dx,dy = (fx-state.x, fy-state.y)
                #print 'move', dx,dy, 'for plan', field
                return np.array([env.movemap[dx,dy]])


class KeyOption(Option2):
    def can_initiate(self, env, state):
        self.room = -1
        return (state.h == 0 and state.l == 1)

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
        return (state.l == 0 and state.h == 0)

    def is_terminated(self, env, state):
        if random() < self.epsilon:
            return True
        return env.goal == (state.x, state.y)

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
                #print 'choose random option in door plan'
                return np.array([choice(env.actions)])
            elif pos == pathpos:
                fx,fy = self.plan[i+1]
                dx,dy = (fx-state.x, fy-state.y)
                #print 'move in direction',dx,dy,'for door plan'
                return np.array([env.movemap[dx,dy]])

class PerfectOptionAgent(SarsaAgent):
    def __init__(self, state_desc, action_desc):
        self.options = [DoorOption(), KeyOption(), LockOption()]
        SarsaAgent.__init__(self, state_desc, (len(self.options),))
        self.stateDim = len(state_desc)  # dims in state vector that we care about
        self.option = None

    def choose_action(self, env, state):
        if self.option is None or self.option.is_terminated(env, state):
            self.option = None
            while self.option is None:
                opti = SarsaAgent.choose_action(self, env, state)[0]
                self.option = self.options[opti]
                if not self.option.can_initiate(env, state):
                    self.qTable[state[:self.stateDim]+(opti,)] = float('-inf')
                    self.option = None
                #print zip(*np.where(np.isinf(self.qTable)))
                assert not np.all(np.isinf(self.qTable[state[:self.stateDim]])), (self, state)
                #else:
                #    pass
                #    #print 'started option', self.option
        return self.option.choose_action(env, state)
        #    #return np.array([choice(env.actions)])
        #else:
        #    return self.option.choose_action(env, state)

    def feedback(self, state, action, reward, state2, action2 = None, env=None):
        assert self.option is not None
        opti = np.array([self.options.index(self.option)])
        SarsaAgent.feedback(self, state, opti,
                reward, state2, opti, env)

    def episode_finished(self):
        pass
