from numpy import array
from environment import Lightworld
from lightworld_gen import gen_world
from agent import RandomAgent
from pygamerenderer import PygameRenderer
from utility import run_experiment

env = Lightworld(*[room for iskey, room in gen_world()])
agent = RandomAgent()
rend = PygameRenderer(env)

run_experiment(env, agent, rend)
