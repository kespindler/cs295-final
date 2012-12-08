from numpy import array
import pygame

def uniform_arr(*strings):
    maxw = max(max(len(l) for l in string) for string in strings)
    maxh = max(len(string.split('\n')) for string in strings)
    r = []
    for s in strings:
        s = s.replace(' ', '0')
        lines = s.split('\n')
        m = [[int(z) for z in l + '1'*(maxw-len(l))] for l in lines]
        m.extend([1]*maxw for _ in range(maxh-len(m)))
        r.append(array(m).T)
    return r

lr = lrg.LightroomGen()
room1 = lr.make_rand_room()
room2 = lr.make_rand_room()
room3 = lr.make_rand_room()

env = Lightroom(room1, room2, room3)
#agent = OptionAgent2()
agent = RandomAgent()
#agent = BridgeAgent(LearningAgent, ActionValueTable, SARSA, 56, 6)
# The first array should be the observation space of the environment...
# We should be able to calculate this.
#agent = BridgeAgent(LearningAgent, ActionValueTable, SARSA, [56, 6, 12], [0.1, 0.99])
rend = LightroomRenderer(env)

run_experiment(env, agent, rend)
