from abc import ABCMeta, abstractmethod
from numpy import where, array
from random import choice
from utility import enum
from collections import namedtuple
from itertools import product

def filter_states(states, field):
    return zip(*where(states == field))

class Environment(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def perform_action(self, state, action):
        return None, None # state, reward

    @abstractmethod
    def new_state(self):
        return None # state

    def is_finished(self, state):
        return False


State = namedtuple('State', 'rxyhl'.split() + [''.join(x) for x in product('nsew', 'rgb')])

class Lightworld(Maze):
    # NSEW is north south east west
    # G is grab to grab a key
    # P is press lock
    field = enum(EMPTY=0,WALL=1,INIT=2,KEY=3,LOCK=4,DOOR=5)
    actions = enum(N=0,S=1,E=2,W=3,G=4,P=5)

    def set_room(self, room):
        assert 0 <= room < len(self.rooms)
        self.room = room
        roomarr = self.rooms[room]
        self.states = roomarr.copy()
        self.goal = filter_states(self.states, self.field.DOOR)[0]
        self.initPos = filter_states(self, self.field.INIT)
        self.agent_holding_key = False

    def __init__(self, *rooms):
        self.rooms = rooms
        self.set_room(0)

    def is_state_forbidden(self, state):
        return self.states[state] in [self.field.WALL, self.field.DOOR]

    def perform_action(self, state, action):
        a = self.actions
        if action in [a.N, a.S, a.E, a.W]:
            delta = {a.N:(0,-1), a.S:(0,1), a.E:(1,0), a.W:(-1,0)}[action]
            if reward == self.done_reward: # can't check goal state because we will have reset state at this point. maybe not the best?
                self.cur_room = (self.cur_room + 1)%len(self.rooms)
                room = self.rooms[self.cur_room].copy()
                self.states = room
                self.initPos = zip(*where(self.states == self.field.INIT))
                self.goal = zip(*where(room == self.field.DOOR))[0]
                state2 = self.new_state()
                reward = self.done_reward if self.cur_room == 0 else self.step_reward
            return state2, reward
        elif action == a.G:
            if self.states[state] == self.field.KEY:
                self.agent_holding_key = True
                self.states[state] = self.field.EMPTY
        elif action == a.I:
            if self.states[state] == self.field.LOCK:
                if len(filter_states(self, self.field.KEY)) == 0:
                    self.agent_holding_key = False
                self.states[self.states == self.field.DOOR] = self.field.EMPTY
        return state, self.step_reward

