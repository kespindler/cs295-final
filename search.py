import heapq
from collections import namedtuple

Node = namedtuple('Node', ['priority', 'state', 'parent'])

def manhattan_dist(a,b):
    ax,ay = a
    bx,by = b
    return abs(by-ay) + abs(bx-ax)

def expand_state(a):
    return [map(sum, zip(a,b)) for b in [(0, 1), (0, -1), (-1, 0), (1, 0)]]
    
def best_first_graph_search(env, start, end, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    node = Node(0, start, None)
    if env.is_goal(node.state):
        return [node.state]
    frontier = []
    heapq.heappush(frontier, node)
    explored = set() #states, not nodes, go in this set
    end = None
    while frontier:
        node = heapq.heappop(frontier)
        if env.is_goal(node.state):
            end = node
            break
        explored.add(node.state)
        for s in expand_state(node.state):
            child = Node(node.priority + 1, s, node.state)
            if child.state not in explored:# their implementation also had: `and child not in frontier:`
                frontier.append(child)
            #elif child in frontier:
            #    incumbent = frontier[child]
            #    if f(child) < f(incumbent):
            #        del frontier[incumbent]
            #        frontier.append(child)
    if end is None:
        return None
    result = []
    while node:
        result.append(node.state)
        node = node.parent
    return result
