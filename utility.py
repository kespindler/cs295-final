from time import sleep
from numpy import array

def enum(*sequential,**named):
    enums = dict(zip(sequential, range(len(sequential))),**named)
    s = type('Enum',(), enums)
    s.__len__ = lambda self: len(enums)
    s.__getitem__ = lambda self, i: enums.values()[i]
    return s()

def run_experiment(env, agent, rend = None, steps = None, delay = 0):
    i = 0
    def run_interaction(state, render=False):
        action = agent.choose_action(env, state)
        state2, reward = env.perform_action(state, action)
        agent.feedback(state, action, reward, state2)
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

def uniform_arr(*strings):
    maxw = max(max(len(l) for l in string) for string in strings)
    maxh = max(len(string.split('\n')) for string in strings)
    rooms = []
    for s in strings:
        s = s.replace(' ', '0')
        lines = s.split('\n')
        m = [[int(z) for z in l + '1'*(maxw-len(l))] for l in lines]
        m.extend([1]*maxw for _ in range(maxh-len(m)))
        rooms.append(array(m).T)
    return rooms

def rooms_from_fpath(fpath):
    with open(fpath) as f:
        text = f.read()
    strings = text.split('\n\n')
    print '\n--------------\n'.join(strings)
    rooms = uniform_arr(*strings)
    return rooms
