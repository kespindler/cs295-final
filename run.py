from numpy import array
from environment import Lightworld
from lightworld_gen import gen_world
from agent import SarsaAgent, RandomAgent
from options import OptionAgent
from pygamerenderer import PygameRenderer
from utility import rooms_from_fpath, run_experiment

problemSpaceDim = 5
#agentSpaceDim = 12

rooms = gen_world()
env = Lightworld(*[room for iskey, room in rooms])
env = Lightworld(*rooms_from_fpath('basic_lightworld.txt'))
stateDesc = env.dimensions()[0:problemSpaceDim]
actionDesc = (6,)
agent = OptionAgent(stateDesc, actionDesc)
#rend = PygameRenderer(env)
rend = None

run_experiment(env, agent, rend, outfpath = 'optionagent.txt')
