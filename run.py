from numpy import array
from environment import Lightworld
from lightworld_gen import gen_world
from agent import SarsaAgent, RandomAgent
from options import OptionAgent
from pygamerenderer import PygameRenderer
from utility import run_experiment

problemSpaceDim = 5
agentSpaceDim = 12

rooms = gen_world()
env = Lightworld(*[room for iskey, room in rooms])
stateDesc = env.dimensions()[0:problemSpaceDim]
actionDesc = (6,)
agent = OptionAgent(stateDesc, actionDesc)
rend = PygameRenderer(env)

run_experiment(env, agent, rend)
