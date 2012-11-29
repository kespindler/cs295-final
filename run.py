from pylov import run_experiment
from pylov.pygamerenderer import PygameRenderer, GREEN, LIGHTGREY, img_point, FIELD_SIZE
from pylov.lightroom import Lightroom, field
from pylov.pylov_bridge import BridgeAgent
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q, SARSA
from pybrain.rl.learners.valuebased import ActionValueTable
from pylov.agent import RandomAgent
from numpy import array
import pygame

#0, ' ' is empty
#1 is wall
#2 is initial position of agent
#3 is key
#4 is lock
#5 is door
#6 is a lock that does not require a key
room1="""\
1111111
12   11
1    51
1    11
13   11
1    41
1    11
1111111"""

room2="""\
111111
11   1
12 3 1
11   1
11   1
115141
111111"""

room3="""\
111111
121111
1   11
1   61
1   11
115111
111111"""

class LightroomRenderer(PygameRenderer):
    def __init__(self, env):
        #print kwargs
        PygameRenderer.__init__(self, env)
        pygame.display.set_mode((640, 480))

    def fill_grid(self):
        for i in range(self.maze.states.shape[0]):
            for j in range(self.maze.states.shape[1]):
                if self.maze.states[i, j] == field.WALL:
                    self.screen.fill(GREEN, self.make_rect(i,j))
                else:
                    self.screen.fill(LIGHTGREY, self.make_rect(i,j))
                    if self.maze.states[i,j] == field.KEY:
                        self.screen.blit(self.key_img, img_point(i,j))
                    elif self.maze.states[i,j] == field.KEY_LOCK:
                        self.screen.blit(self.lock_img, img_point(i,j))
                        self.screen.blit(self.key_img, img_point(i,j))
                    elif self.maze.states[i,j] == field.LOCK_DOOR:
                        self.screen.blit(self.door_img, img_point(i,j))
                    elif self.maze.states[i,j] == field.KEYLESS_LOCK:
                        self.screen.blit(self.lock_img, img_point(i,j))
        self.screen.blit(self.goal_img, img_point(*self.maze.goal))

def arr_from_str(string):
    string = string.replace(' ', '0')
    lines = string.split('\n')
    return array([[int(z) for z in l] for l in lines]).T

room1 = arr_from_str(room1)
room2 = arr_from_str(room2)
room3 = arr_from_str(room3)
env = Lightroom(room1, room2, room3)
#agent = RandomAgent()
#agent = BridgeAgent(LearningAgent, ActionValueTable, SARSA, 56, 6)
agent = BridgeAgent(LearningAgent, ActionValueTable, SARSA, [56, 6], [0.1, 0.99])
rend = LightroomRenderer(env)

run_experiment(env, agent, rend)
