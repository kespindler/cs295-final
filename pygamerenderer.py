import pygame
from abc import ABCMeta, abstractmethod
from pygame.locals import *
from os import path
from environment import Lightworld
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
BLACK = (0,0,0)
BLUE = (0xa,0xa,0xfa)
GREEN = (0x80,0xf0,0x80)
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

    def fill_triangle(self, i, j, max_val):
        rect = self.make_rect(i, j)
        center = (rect[0] + int((rect[2]/2)),
                  rect[1] + int((rect[3]/2)))
        point_list = [(rect[0] + rect[2]-1, rect[1]), 
                      (rect[0] + rect[2]-1, rect[1] + rect[3]-1), 
                      (rect[0], rect[1] + rect[3]-1),
                      (rect[0], rect[1])]
        state = i * self.maze.states.shape[1] + j
        #action_vals = self.agent.learner.module.getActionValues(state)
        #for k, val in enumerate(action_vals): #4 directions, and their order is N E S W
        #    color = tuple([max(0, int(val/max_val*0xff))]*3)
        #    pygame.draw.polygon(self.screen, color, [point_list[k], center, point_list[(k+1)%4]])

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
        
    def fill_square(self, i, j):
        self.screen.fill(LIGHTGREY, self.make_rect(i,j))

    def fill_grid(self):
        for i in range(self.maze.states.shape[0]):
            for j in range(self.maze.states.shape[1]):
                if self.maze.states[i, j] == field.WALL:
                    self.screen.fill(GREEN, self.make_rect(i,j))
                else:
                    self.fill_square(self, i, j)
                    if self.maze.states[i,j] == field.KEY:
                        self.screen.blit(self.key_img, img_point(i,j))
                    elif self.maze.states[i,j] == field.DOOR:
                        self.screen.blit(self.door_img, img_point(i,j))
                    elif self.maze.states[i,j] == field.LOCK:
                        self.screen.blit(self.lock_img, img_point(i,j))
        self.screen.blit(self.goal_img, img_point(*self.maze.goal))

    def update(self, state):
        self.screen.convert()
        self.fill_grid()
        self.screen.blit(self.person_img, img_point(state.x, state.y))
        pygame.display.update()
