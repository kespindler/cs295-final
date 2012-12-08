from time import sleep

def enum(*sequential,**named):
    enums = dict(zip(sequential, range(len(sequential))),**named)
    s = type('Enum',(), enums)
    s.__len__ = lambda self: len(enums)
    s.__getitem__ = lambda self, i: enums.values()[i]
    return s()

def run_experiment(env, agent, rend = None, steps = None, delay = 0):
    i = 0
    def run_interaction(state, render=False):
        obs = env.observation(state)
        action = agent.choose_action(env, obs)
        #observation, reward for a pomdp
        state2, reward = env.perform_action(state, action)
        obs2 = env.observation(state)
        agent.feedback(obs, action, reward, obs2)
        if render and rend is not None:
            rend.update(state2)
        return state2
 
    current_state = env.new_state()
    while 1:
        if steps is not None:
            if steps <= 0:
                break
            else:
                steps -= 1

        current_state = run_interaction(current_state, True)
        if delay > 0:
            sleep(delay)

        i += 1
        if i % 100 == 0:
            print i


def lightworld_from_fpath(fpath):
    with open(fpath) as f:
        text = f.read()
    strings = text.split('\n\n')
    print strings
    rooms = uniform_arr(*strings)
    return Lightworld(*rooms)
