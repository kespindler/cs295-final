from numpy import array

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
