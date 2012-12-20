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
    task_reward = -1

    def set_room(self, room):
        assert 0 <= room < len(self.rooms)
        self.room = room
        roomarr = self.rooms[room]
        self.states = roomarr.copy()
        self.goal = filter_states(self.states, self.field.DOOR)[0]
        self.initPos = filter_states(self.states, self.field.INIT)
        self.lock_pos = filter_states(self.states, self.field.LOCK)[0]
        key_pos = filter_states(self.states, self.field.KEY)
        self.key_pos = key_pos[0] if key_pos else None
        self.agent_holding_key = False

    def __init__(self, *rooms):
        #print rooms
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
        currRoom = self.room
        r = self.room
        x,y = pos
        h = 1 if self.agent_holding_key else 0
        l = 1 if self.states[self.goal] == self.field.DOOR else 0
        next_posns = [tuple(map(sum, zip(pos, dir))) for dir in Lightworld.movemap.values()]
        #field_locs = [filter_states(self.states, field) for field in [self.field.DOOR, self.field.KEY, self.field.LOCK]]
        #field_locs = [[self.goal], self.key_pos, self.lock_pos]
        #rgbs = [(0 if not fieldpos else max(0, 1. - manhattan_dist(pos, fieldpos[0])/20.)) for fieldpos in field_locs for pos in next_posns]
        #red == door
        rgbs = [0]*12
        cap_manhat_dist = lambda a,b: max(0, 1. - manhattan_dist(a, b)/20.)
        #rgbs[::3] = [0 if self.states[self.goal] == Lightworld.field.DOOR 
        reds = [0 if self.states[self.goal] == Lightworld.field.DOOR 
                     else cap_manhat_dist(p, self.goal) for p in next_posns]
        reds = [cap_manhat_dist(pos, self.goal) if r > 0 and r == max(reds) else 0 for r in reds]
        #rgbs[1::3] = [cap_manhat_dist(pos, self.lock_pos) for pos in next_posns]
        blues = [cap_manhat_dist(p, self.lock_pos) for p in next_posns]
        blues = [cap_manhat_dist(pos, self.lock_pos) if g > 0 and g == max(blues) else 0 for g in blues]
        greens = [0 if (self.key_pos is None or self.states[self.key_pos] != Lightworld.field.KEY)
                      else cap_manhat_dist(p, self.key_pos) for p in next_posns]
        greens = [cap_manhat_dist(pos, self.key_pos) if b > 0 and b == max(greens) else 0 for b in greens]
        rgbs[::3] = reds
        rgbs[1::3] = greens
        rgbs[2::3] = blues
        #for pos in next_posns:
        #    #pos2 = tuple(map(sum, zip(pos, dir)))
        #    # door, key, lock in rgb order
        #    for posls, field in zip(field_locs, [self.field.DOOR, self.field.KEY, self.field.LOCK]):
        #        if not pos
        #        
        #        if 
        #        
        #        #fields = filter_states(self.states, field)
        #        #rgbs.append(0 if not fields else 
        #        #        max(0, 1. - manhattan_dist(pos, fields[0])/20.))
        state = State(currRoom,int(x),int(y),h,l,*rgbs)
        return state

    def new_state(self):
        #pos = choice(filter_states(self.states, self.field.INIT))
        return self.calculate_state(choice(self.initPos))

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
                self.states[self.goal] = self.field.EMPTY
                #self.states[self.states == self.field.DOOR] = self.field.EMPTY
                reward = self.task_reward
        return (self.calculate_state(pos2), reward)
