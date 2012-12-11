import numpy as np
from environment import Lightworld
from lightworld_gen import gen_world
from agent import SarsaAgent, RandomAgent, PerfectOptionAgent
from options import OptionAgent
try:
    from pygamerenderer import PygameRenderer
except:
    pass
from utility import rooms_from_fpath, run_experiment
import os
import matplotlib.pyplot as plt
import multiprocessing as mp

problemSpaceDim = 5
#agentSpaceDim = 12
#actionDesc = (6,)

folder = 'lightworlds'
outcsv = 'agent.csv'
outpng = 'agent.png'
assert not os.path.exists(outcsv)
assert not os.path.exists(outpng)

worldfnames = [os.path.join(folder, f) for f in os.listdir(folder)]

N_DUPS = 3
#N_DUPS = 10
N_EPISODES = 70
#N_EPISODES = 1
worldfnames = worldfnames[:25] # dont' do this
q = mp.Queue()

def run_iteration(lightworldfname):
    print 'Begin lightworld', lightworldfname
    env = Lightworld(*rooms_from_fpath(lightworldfname))
    stateDesc = env.dimensions()[0:problemSpaceDim]
    action_desc = (6,)
    agent = PerfectOptionAgent(stateDesc, action_desc)
    #rend = PygameRenderer(env)
    rend = None
    episode_lengths = run_experiment(env, agent, rend, episodes = N_EPISODES)
    q.put(episode_lengths)

run_iteration(worldfnames[0]) #ensures a single run runs successfully...
lightworldfpaths = [f for f in worldfnames for _ in range(N_DUPS)]
pool = mp.Pool(8)
pool.map(run_iteration, lightworldfpaths)

resultarr = np.zeros((N_DUPS * len(worldfnames),N_EPISODES))
i = 0
while not q.empty():
    resultarr[i,:] = q.get()
    i += 1

means = resultarr.mean(0)
np.savetxt(outcsv, resultarr,delimiter=',')
plt.plot(means)
plt.savefig(outpng)
