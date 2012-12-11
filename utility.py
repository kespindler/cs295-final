from time import sleep
from numpy import array, where
from datetime import datetime

def filter_states(states, field):
    return zip(*where(states == field))

def enum(*sequential,**named):
    enums = dict(zip(sequential, range(len(sequential))),**named)
    s = type('Enum',(), enums)
    s.__len__ = lambda self: len(enums)
    s.__getitem__ = lambda self, i: enums.values()[i]
    return s()

def run_experiment(env, agent, rend = None, episodes = None, agent_env = None delay = 0, outfpath = None):
    i = 0
    last = 0
    episode_lengths = []
    def run_interaction(state, render=False):
        action = agent.choose_action(env, state)
        state2, reward = env.perform_action(state, action)
        agent.feedback(state, action, reward, state2, env=env)
        if render and rend is not None:
            rend.update(state2)
        return state2
 
    if outfpath:
        with open(outfpath, 'a') as f:
            f.write('BEGAN ' + str(datetime.now()) + '\n')

    current_state = env.new_state()
    while 1:
        current_state = run_interaction(current_state, True)
        #print current_state
        if env.episode_finished(current_state):
            agent.episode_finished()
            steps_taken = i - last
            if outfpath:
                with open(outfpath, 'a') as f:
                    f.write(str(steps_taken) + '\n')
            episode_lengths.append(steps_taken)
            if episodes is not None and len(episode_lengths) == episodes:
                break
            elif agent_env is not None:
                # If there's an agent environment, run the agent in it once then return
                run_experiment(ageng_env, agent, None, 1)
            env.restart_episode()
            current_state = env.new_state()
            last = i

        if delay > 0:
            sleep(delay)

        i += 1
        #if i % 100 == 0:
        #    print i
    return episode_lengths

def uniform_arr(*strings):
    maxh = max(max(len(l) for l in string) for string in strings)
    maxw = max(len(string.split('\n')) for string in strings)
    rooms = []
    for s in strings:
        s = s.replace(' ', '0')
        lines = [s for s in s.split('\n')]
        m = [[int(z) for z in l + '1'*(maxw-len(l))] for l in lines]
        m.extend([1]*maxw for _ in range(maxh-len(m)))
        rooms.append(array(m).T)
    return rooms

def rooms_from_fpath(fpath):
    with open(fpath) as f:
        text = f.read().rstrip()
    strings = text.split('\n\n')
    #print '\n--------------\n'.join(strings)
    rooms = uniform_arr(*strings)
    #print rooms
    return rooms

class Bidict(dict):
    def __init__(self, d):
        for k,v in d.items():
            self[k] = v
        self.reverse = {v:k for k,v in d.items()}
    
    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        return self.reverse[key]
