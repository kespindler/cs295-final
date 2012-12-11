
def test_bfs():
    from numpy import array
    from search import best_first_graph_search, manhattan_dist
    from environment import Lightworld, expand_state
    maze_string2 = """\
111111111
1  1    1
1  1  1 1
1  1  1 1
1  1 11 1
1     1 1
1111111 1
1       1
111111111"""

    def arr_from_str(string):
        return array([[1 if z=='1' else 0 for z in l] for l in 
            string.split('\n')])

    structure = arr_from_str(maze_string2)
    h = len(structure[0])
    w = len(structure)
    print structure

    goal = (w-2, h-2)
    expand_state_partial = lambda s: expand_state(structure, s)
    manhattan_dist_partial = lambda s: manhattan_dist(s, goal)
    print best_first_graph_search((1,1), goal, manhattan_dist_partial, expand_state_partial)


def test_env(cls_agent):
    from utility import rooms_from_fpath, run_experiment
    from pygamerenderer import PygameRenderer
    from environment import Lightworld
    lightworld = Lightworld(*rooms_from_fpath('basic_lightworld.txt'))
    probdim = 5
    agent = cls_agent(lightworld.dimensions()[:probdim], len(lightworld.actions))
    rend = PygameRenderer(lightworld, agent)
    run_experiment(lightworld, agent, rend, delay=.05)

def test_env1():
    from agent import RandomAgent
    test_env(RandomAgent)

def test_env2():
    from agent import PerfectOptionAgent
    test_env(PerfectOptionAgent)

def test_env3():
    from agent import SarsaAgent
    test_env(SarsaAgent)

if __name__ == "__main__":
    test_env2()
