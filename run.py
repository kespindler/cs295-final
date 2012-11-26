from pylov import run_experiment
from pylov.pygamerenderer import PygameRenderer, GREEN, LIGHTGREY, img_point
from pylov.lightroom import Lightroom, field
from pylov.agent import RandomAgent
from numpy import array

#0, ' ' is empty
#1 is wall
#2 is player
#3 is key
#4 is lock
#5 is door
lightroom_string = """\
1111111111111
12   111   11
1    5   3 11
1    111   11
13   111   11
1    41151411
1    111   11
11111111   61
11111111   11
1111111115111
1111111111111"""
class LightroomRenderer(PygameRenderer):
    def fill_grid(self):
        for i in range(self.maze.states.shape[0]):
            for j in range(self.maze.states.shape[1]):
                if self.maze.states[i, j] == field.WALL:
                    color = GREEN
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
                    elif self.maze.states[i,j] == field.KEY_LOCK:
                        self.screen.blit(self.lock_img, img_point(i,j))
        self.screen.blit(self.goal_img, img_point(*self.maze.goal))

def arr_from_str(string):
    string = string.replace(' ', '0')
    lines = string.split('\n')
    return array([[int(z) for z in l] for l in lines])

structure = arr_from_str(lightroom_string)
print structure
lock_pairs = {}
lock_pairs[5,5] = (5, 2)
lock_pairs[10,5] = (8, 5)
lock_pairs[11,7] = (9, 9)
env = Lightroom(structure, (9, 9), lock_pairs)
agent = RandomAgent()
rend = LightroomRenderer(env)

run_experiment(env, agent, rend)
