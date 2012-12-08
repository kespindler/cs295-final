from utility import run_experiment
from pygamerenderer import PygameRenderer
from environment import Maze
from agent import RandomAgent
from numpy import array
import lightroom_gen as lr_gen

maze_string2 = """\
111111111
1  1    1
1  1  1 1
1  1  1 1
1  1 11 1
1     1 1
1111111 1
1       1
111111111"""

def arr_from_str(string):
    return array([[1 if z=='1' else 0 for z in l] for l in string.split('\n')])

lrg = lr_gen.LightroomGen()
structure = lrg.make_rand_room() #arr_from_str(maze_string2) #
h = len(structure[0])
w = len(structure)
print structure
env = Maze(structure, (w-2, h-2))
agent = RandomAgent()
rend = PygameRenderer(env)

run_experiment(env, agent, rend)
