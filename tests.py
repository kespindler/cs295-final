
def test_bfs():
    from numpy import array
    from search import best_first_graph_search, manhattan_dist
    from environment import Lightworld
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

    def expand_state(a):
        next_states = [tuple(map(sum, zip(a,b))) for b in 
                [(0, 1), (0, -1), (-1, 0), (1, 0)]]
        return [s for s in next_states if structure[s] != Lightworld.field.WALL]

    print best_first_graph_search((1,1), (w-2, h-2), manhattan_dist, expand_state)

def test_new_env():
    from agent import RandomAgent
    from utility import rooms_from_fpath, run_experiment
    from pygamerenderer import PygameRenderer
    from environment import Lightworld
    lightworld = Lightworld(*rooms_from_fpath('basic_lightworld.txt'))
    agent = RandomAgent()
    rend = PygameRenderer(lightworld)
    run_experiment(lightworld, agent, rend)

