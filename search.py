import heapq
from collections import namedtuple

Node = namedtuple('Node', ['priority', 'state', 'parent'])

def manhattan_dist(a,b):
    ax,ay = a
    bx,by = b
    return abs(by-ay) + abs(bx-ax)

    
def best_first_graph_search(start, end, f, expand_state):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    node = Node(0, start, None)
    if node.state == end:
        return [node.state]
    frontier = []
    heapq.heappush(frontier, node)
    explored = set() #states, not nodes, go in this set
    solved = False
    while frontier:
        node = heapq.heappop(frontier)
        if node.state == end:
            solved = True
            break
        explored.add(node.state)
        for s in expand_state(node.state):
            child = Node(node.priority + 1, s, node)
            if child.state not in explored:# their implementation also had: `and child not in frontier:`
                frontier.append(child)
            #elif child in frontier:
            #    incumbent = frontier[child]
            #    if f(child) < f(incumbent):
            #        del frontier[incumbent]
            #        frontier.append(child)
    if not solved:
        return None
    result = []
    while node:
        result.append(node.state)
        node = node.parent
    return result
