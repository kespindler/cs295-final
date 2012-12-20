from numpy import array
from environment import Lightworld
from lightworld_gen import gen_world
from agent import SarsaAgent, RandomAgent, PerfectOptionAgent
from options import OptionAgent
from gradient_descent import GradientDescentSarsaAgent
from agent_options import COptionAgent
from pygamerenderer import PygameRenderer
from utility import rooms_from_fpath, run_experiment

problemSpaceDim = 5
agentSpaceDim = 12
actionDesc = (6,)

rooms = gen_world()
env = Lightworld(*[room for iskey, room in rooms])
env = Lightworld(*rooms_from_fpath('basic_lightworld.txt'))
stateDesc = env.dimensions()
# agent = OptionAgent(stateDesc[0:problemSpaceDim], actionDesc)
# agent = SarsaAgent(stateDesc[0:problemSpaceDim], actionDesc)
# agent = GradientDescentSarsaAgent(agentSpaceDim, problemSpaceDim, actionDesc)
agent = COptionAgent(stateDesc, problemSpaceDim, actionDesc)
# agent = PerfectOptionAgent(stateDesc[:problemSpaceDim])
rend = PygameRenderer(env, agent)
# rend = None

run_experiment(env, agent, rend, outfpath = 'optionagent.txt')
