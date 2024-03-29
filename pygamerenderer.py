import pygame
from abc import ABCMeta, abstractmethod
from pygame.locals import *
from os import path
from environment import Lightworld
import numpy as np
field = Lightworld.field

class RenderEngine(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def update(self, state):
        return


FIELD_SIZE = 40
SQUARE_MARGIN = 1
IMG_MARGIN = 4

#TODO maybe wantt o standsard this a bit
LIGHTGREY = (0xfb, 0xfb, 0xfb)
MEDGREY = (0xc0, 0xc0, 0xc0)
LIGHTGREEN = (0x80, 0xfa,0x80)
BLACK = (0,0,0)
RED = (0xff,0,0)
GREEN = (0,0xff,0)
BLUE = (0,0,0xff)
WHITE = (0xff, 0xff, 0xff)

def load_img(name):
    # I'm not sure this path.dirname method is the best way to find the iamges. but seems to work well in my case?
    # Run this by someone to see if it needs to be generalized or something...
    img1 = pygame.image.load(path.join(path.dirname(__file__), 'images', name+'.png'))
    img2 = pygame.transform.scale(img1, (FIELD_SIZE - 2*IMG_MARGIN, 
                                         FIELD_SIZE - 2*IMG_MARGIN))
    return img2

def img_point(i, j):
    return (i * FIELD_SIZE + IMG_MARGIN, 
            j * FIELD_SIZE + IMG_MARGIN)
    
def norm(qval):
    #import pdb;pdb.set_trace()
    q2 = [0 if np.isinf(q) else q for q in qval]
    minv = min(q2)
    q3 = [q - minv for q in q2]
    maxv = max(abs(q) for q in q3)
    if maxv:
        return [q / maxv for q in q3]
    else:
        return q3

class PygameRenderer(RenderEngine):
    def __init__(self, maze_env = None, agent = None):
        pygame.init()
        self.maze = maze_env
        self.agent = agent
        self.screen = pygame.display.set_mode(tuple(dim * FIELD_SIZE for dim in self.maze.states.shape))
        pygame.display.set_caption("Visualizer")
        #TODO this imgs shouldnt be properties but globals i think...
        self.key_img = load_img('key')
        self.person_img = load_img('person')
        self.goal_img = load_img('goal')
        self.door_img = load_img('door')
        self.lock_img = load_img('lock')

    # make this a global funciton
    def make_rect(self, i, j):  #This should be a named tuple
        return (i * FIELD_SIZE + SQUARE_MARGIN, 
                j * FIELD_SIZE + SQUARE_MARGIN, 
                FIELD_SIZE - 2 * SQUARE_MARGIN, 
                FIELD_SIZE - 2 * SQUARE_MARGIN)

    def fill_triangle(self, state, max_val):
        rect = self.make_rect(state.x,state.y)
        center = (rect[0] + int((rect[2]/2)),
                  rect[1] + int((rect[3]/2)))
        point_list = [(rect[0] + rect[2]-1, rect[1]), 
                      (rect[0] + rect[2]-1, rect[1] + rect[3]-1), 
                      (rect[0], rect[1] + rect[3]-1),
                      (rect[0], rect[1])]
        #state = i * self.maze.states.shape[1] + j
        action_vals = self.agent.qTable[state[:self.agent.stateDim]][:4]
        for k, val in enumerate(action_vals): #4 directions, and their order is N E S W
            color = tuple([max(0, int(val/max_val*0xff))]*3)
            pygame.draw.polygon(self.screen, color, [point_list[k], center, point_list[(k+1)%4]])

    #def fill_grid(self):
    #    if self.agent is not None:
    #        max_val = int(1 + self.agent.pyb_agent.learner.module.params.max())
    #    for i in range(self.maze.states.shape[0]):
    #        for j in range(self.maze.states.shape[1]):
    #            if self.maze.states[i, j] == field.WALL:
    #                self.screen.fill(GREEN, self.make_rect(i,j))
    #            else:
    #                if self.agent is None:
    #                    self.screen.fill(LIGHTGREY, self.make_rect(i,j))
    #                else:
    #                    self.fill_triangle(i,j, max_val)
    #    self.screen.blit(self.goal_img, img_point(*self.maze.goal))
        
    def fill_state(self, state):
        if hasattr(self.agent, 'options') and hasattr(self.agent, 'qTable'):
            #door,key,lock
            #r,g,b
            qvals = self.agent.qTable[state[:self.agent.stateDim]]
            qvals = norm(qvals)
            x,y,w,h = self.make_rect(state.x,state.y)
            w = w/3
            for v, c, i in zip(qvals, [RED, GREEN, BLUE], range(3)):
                c = tuple(int(i * v) for i in c)
                self.screen.fill(c, (x+i*w,y,w,h))
        elif self.agent is not None and hasattr(self.agent, 'qTable'):
            # do triangle visu
            max_val = int(1 + self.agent.qTable.max())
            self.fill_triangle(state, max_val)
        else:
            self.screen.fill(LIGHTGREY, self.make_rect(state.x,state.y))

    def fill_grid(self,state):
        for i in range(self.maze.states.shape[0]):
            for j in range(self.maze.states.shape[1]):
                if self.maze.states[i, j] == field.WALL:
                    self.screen.fill(LIGHTGREEN, self.make_rect(i,j))
                else:
                    self.fill_state(state._replace(x=i,y=j))
                    if self.maze.states[i,j] == field.KEY:
                        self.screen.blit(self.key_img, img_point(i,j))
                    elif self.maze.states[i,j] == field.DOOR:
                        self.screen.blit(self.door_img, img_point(i,j))
                    elif self.maze.states[i,j] == field.LOCK:
                        self.screen.blit(self.lock_img, img_point(i,j))
        self.screen.blit(self.goal_img, img_point(*self.maze.goal))

    def update(self, state):
        self.screen.convert()
        self.fill_grid(state)
        #self.fill_state(state)
        self.screen.blit(self.person_img, img_point(state.x, state.y))
        pygame.display.update()
