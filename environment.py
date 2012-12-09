from abc import ABCMeta, abstractmethod
from numpy import where, array
from random import choice
from utility import enum, filter_states, Bidict
from collections import namedtuple
from search import manhattan_dist
from itertools import product

def expand_state(states, a):
    next_states = [tuple(map(sum, zip(a,b))) for b in 
            Lightworld.movemap.values()]
    return [s for s in next_states if states[s] != Lightworld.field.WALL]

class Environment(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def perform_action(self, state, action):
        return None, None # state, reward

    @abstractmethod
    def new_state(self):
        return None # state


State = namedtuple('State', [c for c in 'rxyhl'] + 
        [''.join(x) for x in product('nsew', 'rgb')])


class Lightworld(Environment):
    # NSEW is north south east west
    # G is grab to grab a key
    # P is press lock
    field = enum(EMPTY=0,WALL=1,INIT=2,KEY=3,LOCK=4,DOOR=5)
    actions = enum(N=0,S=1,E=2,W=3,G=4,P=5)
    movemap = Bidict({actions.N:(0, -1),
        actions.S:(0, 1),
        actions.E:(1, 0),
        actions.W:(-1, 0)})
    step_reward = -1
    final_reward = 1000
    task_reward = 1

    def set_room(self, room):
        assert 0 <= room < len(self.rooms)
        self.room = room
        roomarr = self.rooms[room]
        self.states = roomarr.copy()
        self.goal = filter_states(self.states, self.field.DOOR)[0]
        self.initPos = filter_states(self.states, self.field.INIT)
        self.agent_holding_key = False

    def __init__(self, *rooms):
        print rooms
        self.rooms = rooms
        self.set_room(0)

    def forbidden_pos(self, pos):
        return self.states[pos] in [self.field.WALL, self.field.DOOR]

    def episode_finished(self, state):
        return (self.room == len(self.rooms) - 1 and
                (state.x, state.y) == self.goal)

    def dimensions(self):
        r = len(self.rooms)
        x,y = self.rooms[0].shape
        h,l = 2,2
        rgbs = [21]*12
        return tuple([r,x,y,h,l]+rgbs)
    
    def calculate_state(self, pos):
        r = self.room
        x,y = pos
        h = 1 if self.agent_holding_key else 0
        l = 1 if filter_states(self.states, self.field.DOOR) else 0
        rgbs = []
        for dir in Lightworld.movemap.values():
            pos2 = tuple(map(sum, zip(pos, dir)))
            # door, key, lock in rgb order
            for field in [self.field.DOOR, self.field.KEY, self.field.LOCK]:
                fields = filter_states(self.states, field)
                rgbs.append(0 if not fields else 
                        max(0, 1. - manhattan_dist(pos, fields[0])/20.))
        state = State(r,int(x),int(y),h,l,*rgbs)
        return state

    def new_state(self):
        pos = choice(filter_states(self.states, self.field.INIT))
        return self.calculate_state(pos)

    def restart_episode(self):
        self.set_room(0)

    def perform_action(self, state, action):
        assert action.shape == (1,)
        action = action[0] # in this case action i s 
        pos2 = (state.x, state.y)
        a = self.actions
        reward = self.step_reward
        if action in [a.N, a.S, a.E, a.W]:
            delta = self.movemap[action]
            pos2 = tuple(map(sum,zip(pos2, delta)))
            if self.forbidden_pos(pos2):
                pos2 = (state.x,state.y)
            if pos2 == self.goal:
                state = State(*[0]*17)._replace(x=pos2[0], y=pos2[1])
                if not self.episode_finished(state):
                    self.set_room(self.room + 1)
                    reward = self.task_reward
                    state2 = self.new_state()
                    pos2 = (state2.x, state2.y)
                else:
                    reward = self.final_reward
        elif action == a.G:
            if self.states[pos2] == self.field.KEY:
                self.agent_holding_key = True
                self.states[pos2] = self.field.EMPTY
                reward = self.task_reward
        elif action == a.P:
            if (self.states[pos2] == self.field.LOCK and
                    not filter_states(self.states, self.field.KEY)):
                self.agent_holding_key = False
                self.states[self.states == self.field.DOOR] = self.field.EMPTY
                reward = self.task_reward
        return (self.calculate_state(pos2), reward)
