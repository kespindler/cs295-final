from numpy import array
from environment import Lightworld
from lightworld_gen import gen_world
from agent import RandomAgent
from pygamerenderer import PygameRenderer
from utility import run_experiment

rooms = gen_world()
env = Lightworld(*[room for iskey, room in rooms])
stateDesc = env.dimensions[0:5]
actionDesc = (6,)
agent = StandardAgent(stateDesc, actionDesc)
rend = PygameRenderer(env)

run_experiment(env, agent, rend)
