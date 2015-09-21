""" Helper functions """

from collections import defaultdict
import config
from heapq import *
import sys

GOAL_NODE = tuple([tuple([-1, -1, 0, 0, 0, -1, -1]),
                   tuple([-1, -1, 0, 0, 0, -1, -1]),
                   tuple([ 0,  0, 0, 0, 0,  0,  0]),
                   tuple([ 0,  0, 0, 1, 0,  0,  0]),
                   tuple([ 0,  0, 0, 0, 0,  0,  0]),
                   tuple([-1, -1, 0, 0, 0, -1, -1]),
                   tuple([-1, -1, 0, 0, 0, -1, -1])])


def print_node(node):
    """ Print the 7x7 game board """
    nrows = len(node)
    ncols = len(node[0])
    for r in range(nrows):
        for c in range(ncols):
            print '{0:2d}'.format(node[r][c]),
        print
    print

def get_next_valid_node(node, pos, dir):
    """
        Return a node by moving the peg at
        position pos on the board defined by node
        in the direction specified by dir.
        
        Also returns the peg moved as the tuple:
            ((dest_row, dest_col),
             (source_row, source_col))

        If there is no valid move, return None, None.
    """

    #assert node[pos[0]][pos[1]] == 1

    nrows = len(node)
    ncols = len(node[0])
    #assert pos[0] >= 0 and pos[0] < nrows
    #assert pos[1] >= 0 and pos[1] < ncols
    
    newpos = (pos[0] + 2 * config.DIRECTION[dir][0],
              pos[1] + 2 * config.DIRECTION[dir][1])

    # is the target location off the board?
    if newpos[0] < 0 or newpos[1] < 0 or \
       newpos[0] >= nrows or newpos[1] >= ncols:
        return None, None
    
    # is the target location already occupied, or a corner?
    if node[newpos[0]][newpos[1]] != 0:
        return None, None

    midpos = (pos[0] + config.DIRECTION[dir][0],
              pos[1] + config.DIRECTION[dir][1])
    
    # is there a peg to jump over?
    if node[midpos[0]][midpos[1]] != 1:
        return None, None
    
    # create the new node
    newnode = list([list(l[:]) for l in node])
    newnode[pos[0]][pos[1]] = 0 # delete old peg
    newnode[newpos[0]][newpos[1]] = 1 # create new peg
    newnode[midpos[0]][midpos[1]] = 0 # delete mid peg
    
    return tuple([tuple(n) for n in newnode]), \
           ((newpos[0], newpos[1]), (pos[0], pos[1]))

def expand_node(node):
    nrows = len(node)
    ncols = len(node[0])
    children = []
    steps = []
    for r in range(nrows):
        for c in range(ncols):
            if node[r][c] == 1:
                pos = (r,c) # peg found at (r,c)

                # get nodes derived by valid moves of this peg
                for dir in ['N', 'S', 'E', 'W']:
                    child, step =  get_next_valid_node(node, pos, dir)
                    if child is not None:
                        children.append(child)
                        steps.append(step)

    return children, steps

def heuristic1(node):
    """
        Relax the problem as follows: allow each peg to
        be simply removed from the board. Then the heuristic
        is the number of pegs on the board minus 1.

        This is admissable, since reaching the goal
        will require moving pegs, and not simply taking
        them off the board. The heuristic will thus always
        *underestimate* the actual cost to the goal.

        This is also consistent; in each move, we always
        remove one peg from the board, and the path cost
        for each move is 1. Moving from a node n to
        its successor n', along a path costing c(n, a, n')
        will result in h(n) = h(n') + c(n, a, n').
    """
    h = 0
    nrows = len(node)
    ncols = len(node[0])
    for r in range(nrows):
        for c in range(ncols):
            if node[r][c] == 1:
                h += 1
    return h - 1

def heuristic2(node):
    """
        Relax the problem as follows: allow each peg to
        jump two steps in any direction, regardless of
        whether there exists a peg to jump over. Then the
        heuristic is half the sum of Manhattan distances of
        each peg from the center of the board.

        This is admissable, since reaching the goal will
        require pegs to be jumped over; the heuristic
        will always *underestimate* the actual cost to
        the goal.

        This may not be consistent. Let n be a search
        node and n' be its successor, reached after c(n, a, n')
        steps. Let h(n) be the heuristic value at node n,
        and h(n') be that at node n'.

        Let h(n') - h(n) = delta be the change in heuristic
        value in a single step.

        In each step, one peg is moved in some direction.
        This causes the sum of Manhattan distances of all
        pegs to decrease at most by 2.

            -2 <= delta1
        =>  -1 <= delta1/2

        Additionally, one peg is removed from the board,
        which can cause the sum of Manhattan distances of all
        pegs to decrease at most by 2 (in a solvable board, the
        furthest peg that can be jumped over cannot be adjacent
        to a corner or the board's edge, and lies at a Manhattan
        distance of at most 2 from the center).

            -2 <= delta2
        =>  -1 <= delta2/2

        The overall change in the heuristic function from
        node n to n' after c(n, a, n') steps is thus:

            h(n') - h(n) = delta1/2 + delta2/2 >= -2 * c(n, a, n')
        =>  h(n) <= h(n') + 2 * c(n, a, n')

        This doesn't satisfy the consistency criterion.
    """
    h = 0
    nrows = len(node)
    ncols = len(node[0])
    rcenter = nrows/2
    ccenter = ncols/2
    for r in range(nrows):
        for c in range(ncols):
            if node[r][c] == 1:
                manhattan_dist = abs(r - rcenter) + abs(c - ccenter)
                h += manhattan_dist
    return h/2

def is_valid_trace(start_state, trace):
    """
        Runs the trace on the board configuration
        defined by start_state and reports if it is valid
    """

    board = [list(l) for l in start_state]
    nrows = len(board)
    ncols = len(board[0])
    for i in range(0, len(trace), 2):
        # peg is moved from r1, c1 to r2, c2
        r1, c1 = trace[i]
        r2, c2 = trace[i+1]

        assert r1 >= 0 and r2 >= 0 and \
               c1 >= 0 and c2 >= 0
        assert r1 < nrows and r2 < nrows and \
               c1 < ncols and c2 < ncols
        assert board[r1][c1] == 1
        assert board[r2][c2] == 0

        rmid = -1
        cmid = -1
        rowdiff = r2 - r1
        coldiff = c2 - c1
        assert coldiff == 0 or rowdiff == 0
        if rowdiff == 0:
            # direction = 'E' or 'W'
            rmid = r1 # = r2
            cmid = c1 + coldiff/2
        else:
            # direction = 'N' or 'S'
            cmid = c1 # = c2
            rmid = r1 + rowdiff/2

        board[r1][c1] = 0
        board[rmid][cmid] = 0
        board[r2][c2] = 1 

    board = tuple([tuple(l[:]) for l in board])
    return board == GOAL_NODE

""" Modifies pegSolitaireObject """
def a_star_search(pegSolitaireObject, heuristic_fn):
    # initialisation
    expanded = set([])
    parent = {}
    step_trace = {}
    path_cost = defaultdict(lambda: sys.maxint)
    heuristic_cost = defaultdict(lambda: -1)
    fringe = []

    # make a deep copy of the game board (tuple of tuples) as the initial state
    start_state = tuple([tuple(l[:]) for l in pegSolitaireObject.gameState])
    path_cost[start_state] = 0
    parent[start_state] = start_state
    
    # store search nodes as (f(n) = g(n) + h(n), n) tuples,
    # so that f(n) is used as the min-heap key
    start_node = (0, start_state)

    # start search (using a min-heap)
    heappush(fringe, start_node)
    while len(fringe) > 0:
        f_n, node = heappop(fringe)

        if node == GOAL_NODE:
            expanded.add(node)
            break

        # a popped node will turn out to be already expanded
        # only in the case of a board with no solution

        if node not in expanded:
            expanded.add(node)
            children, steps = expand_node(node)
            pegSolitaireObject.nodesExpanded += 1
            for child, step in zip(children, steps):
                if path_cost[node] + 1 < path_cost[child]:
                    """
                        The above condition ensures:
                            - Not adding a node to the fringe
                              that was previously expanded; this
                              is because an expanded node must
                              have had a lower path cost than
                              the path through this node.
                            - Not adding a node to the fringe
                              that is already in the fringe and
                              was found to have a shorter path
                              through another expanded node.
                    """
                    # test the above comment with an assertion
                    #assert child not in expanded

                    path_cost[child] = path_cost[node] + 1
                    parent[child] = node
                    step_trace[child] = step

                    if heuristic_cost[child] < 0:
                        heuristic_cost[child] = heuristic_fn(child)

                    heappush(fringe, (path_cost[child] + heuristic_cost[child],
                                      child))

    # if the solution was not found
    if not GOAL_NODE in expanded:
        pegSolitaireObject.trace = ['GOAL NOT FOUND']
        return

    # compute the trace if a solution was found
    node = GOAL_NODE
    while parent[node] != node:
        pegSolitaireObject.trace.extend(step_trace[node])
        #print_node(node)
        #print 'Step:', step_trace[node][::-1]
        #print
        node = parent[node]
    #print_node(node)

    pegSolitaireObject.trace = pegSolitaireObject.trace[::-1]

    # verify if the trace was valid
    #assert is_valid_trace(start_state, pegSolitaireObject.trace) 

""" Modifies pegSolitaireObject """
def iterative_deepening_search(pegSolitaireObject, max_depth):
    # start a depth limited search for each depth limit
    # - a depth limit of 0 will only run a goal test on the root node,
    #   but not expand it
    # - a depth limit of 1 will expand only the root node
    goal_found = False
    for depth_limit in range(max_depth+1):
        # initialisation
        parent = {}
        step_trace = {}
        depth = {}

        # make a deep copy of the game board (tuple of tuples) as the initial state
        start_state = tuple([tuple(l[:]) for l in pegSolitaireObject.gameState])
        depth[start_state] = 0
        parent[start_state] = start_state

        #print 'dls with depth =', depth_limit
        fringe = [start_state]
        while len(fringe) > 0:
            node = fringe.pop()

            if node == GOAL_NODE:
                goal_found = True
                break

            if depth[node] + 1 > depth_limit:
                # depth limit reached, don't expand
                break

            for child, step in zip(*expand_node(node)):
                pegSolitaireObject.nodesExpanded += 1
                depth[child] = depth[node] + 1
                parent[child] = node
                step_trace[child] = step
                fringe.append(child)

    # if the solution was not found
    if not goal_found:
        pegSolitaireObject.trace = ['GOAL NOT FOUND']
        return

    # compute the trace if a solution was found
    node = GOAL_NODE
    while parent[node] != node:
        pegSolitaireObject.trace.extend(step_trace[node])
        #print_node(node)
        #print 'Step:', step_trace[node][::-1]
        #print
        node = parent[node]
    #print_node(node)

    pegSolitaireObject.trace = pegSolitaireObject.trace[::-1]

    # verify if the trace was valid
    #assert is_valid_trace(start_state, pegSolitaireObject.trace)
