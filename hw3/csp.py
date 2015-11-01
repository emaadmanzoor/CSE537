###########################################
# you need to implement five funcitons here
###########################################

from collections import deque
import random

def get_peers(assignment, var, n, m, k):
    i, j = var
    peers = set([(i,x) for x in xrange(n) if not isinstance(assignment[i,x], int)] +\
                [(x,j) for x in xrange(n) if not isinstance(assignment[x,j], int)] +\
                [(x,y) for x in xrange((i/m)*m, (i/m)*m + m)
                       for y in xrange((j/k)*k, (j/k)*k + k)
                       if not isinstance(assignment[x,y], int)])
    if not isinstance(assignment[i,j], int):
        peers.remove((i,j))
    return peers

def get_peers2(assignment, var, n, m, k):
    i, j = var
    peers = set([(i,x) for x in xrange(n)] +\
                [(x,j) for x in xrange(n)] +\
                [(x,y) for x in xrange((i/m)*m, (i/m)*m + m)
                       for y in xrange((j/k)*k, (j/k)*k + k)])
    peers.remove((i,j))
    return peers

def assign(assignment, var, val, n, m, k):
    """ Appends var=val to the provided assignment,
        Returns None if the assignment is not consistent
        (checks the 3 Sudoku consistency constraints)
    """
    peers = get_peers(assignment, var, n, m, k)
    new_assignment = {k: v for k, v in assignment.iteritems()}
    new_assignment[var] = val
    for peer in peers:
        new_assignment[peer] = new_assignment[peer] - set([val])
    return new_assignment

def is_assignment_complete(assignment):
    """ Returns true if all values in the
        assignment have been assigned values.
    """
    return all([isinstance(v, int) for v in assignment.values()])

def is_assignment_consistent(assignment, n):
    # row
    for i in xrange(1,n):
        if len(set(assignment[i,x] for x in xrange(n))) != n:
            return False

    # column
    for j in xrange(1,n):
        if len(set(assignment[x,j] for x in xrange(n))) != n:
            return False

    # subgrid
    for i in xrange(1,n):
        for j in xrange(1,n):
            if len(set([assignment[x,y]
                        for x in xrange((i/m)*m, (i/m)*m + m)
                        for y in xrange((j/k)*k, (j/k)*k + k)])) != n:
                return False

    return True

def backtrack(assignment, n, m, k,
              order_variables,
              order_values,
              forward_checking,
              constraint_prop,
              nchecks):
    """
        Backtracking search for CSPs.
        See Fig. 6.5, pg 215 in AIMA 3e.
    """

    nchecks += 1
    if is_assignment_complete(assignment):
        return assignment, nchecks

    vars = order_variables(assignment)
    if len(vars) == 0:
        return None, nchecks
    var = vars[0]

    #print_assignment(assignment, n)
    #raw_input()

    for val in order_values(assignment, var, n, m, k):

        new_assignment = assignment
        if forward_checking:
            new_assignment = fc(assignment, var, val, n, m, k)
            if new_assignment is None:
                return None, nchecks
        elif constraint_prop:
            new_assignment = ac3(assignment, var, val, n, m, k)
            if new_assignment is None:
                return None, nchecks

        result, nchecks = backtrack(assign(new_assignment, var, val, n, m, k),
                                    n, m, k, order_variables, order_values,
                                    forward_checking, constraint_prop, nchecks)
        if result is not None:
            return result, nchecks

    return None, nchecks

def print_assignment(assignment, n):
    for i in xrange(n):
        for j in xrange(n):
            x = assignment[i,j]
            if isinstance(x, int):
                print str(x).rjust(10),
            else:
                print str(list(x)).rjust(10),
        print

def parse_game_file(filename):
    """ Returns an immutable Sudoku game state,
        derived from the state represented in the file.
        assignment[i,j] contains the numbers that can be
        assigned to cell i,j.
    """
    assignment = {}
    with open(filename, 'r') as f:
        n, m, k = map(int, f.readline().replace(';', '')\
                                       .replace('\n', '')\
                                       .split(','))
        for i in xrange(n):
            row = f.readline().replace(';', '')\
                              .replace('\n', '')\
                              .split(',')
            for j in xrange(n):
                if row[j] == '-':
                    assignment[i,j] = frozenset(range(1,n+1))
                else:
                    assignment[i,j] = int(row[j])

    return assignment, n, m, k

def order_values_nil(assignment, var, n, m, k):
    return sorted(list(assignment[var]))

# no variables ordering (just sort tuples)
def order_variables_nil(assignment):
    return sorted([k for k, v in assignment.iteritems()
                   if not isinstance(v, int)])

# LCV value ordering
def order_values_lcv(assignment, var, n, m, k):
    peers = get_peers(assignment, var, n, m, k)
    vals = []
    for val in assignment[var]:
        conflicts = sum([1 for peer in peers
                         if val in assignment[peer]])
        vals.append((conflicts, val))
    vals = sorted(vals)
    return [v[1] for v in vals]

def backtracking(filename):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    assignment, n, m, k = parse_game_file(filename)
    goal, consistency_checks = backtrack(assignment, n, m, k,
                                         order_variables_nil,
                                         order_values_nil,
                                         False, False, 0)
    goallist = []
    if goal is not None:
        for i in xrange(n):
            row = []
            for j in xrange(n):
                row.append(goal[i,j])
            goallist.append(row)
    else:
        goallist = [None]

    return (goallist, consistency_checks)

def order_variables_mrv(assignment):
    vars = sorted([(len(v), k)
                   for k, v in assignment.iteritems()
                   if not isinstance(v, int)])
    return [v[1] for v in vars]

def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    assignment, n, m, k = parse_game_file(filename)
    goal, consistency_checks = backtrack(assignment, n, m, k,
                                         order_variables_mrv,
                                         order_values_nil,
                                         False, False, 0)
    goallist = []
    if goal is not None:
        for i in xrange(n):
            row = []
            for j in xrange(n):
                row.append(goal[i,j])
            goallist.append(row)
    else:
        goallist = [None]

    return (goallist, consistency_checks)

def fc(assignment, var, val, n, m, k):
    return ac3(assignment, var, val, n, m, k)

def backtrackingMRVfwd(filename):
    ###
    # use backtracking +MRV + forward propogation
    # to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    
    assignment, n, m, k = parse_game_file(filename)
    goal, consistency_checks = backtrack(assignment, n, m, k,
                                         order_variables_mrv,
                                         order_values_lcv,
                                         True, False, 0)

    goallist = []
    if goal is not None:
        for i in xrange(n):
            row = []
            for j in xrange(n):
                row.append(goal[i,j])
            goallist.append(row)
    else:
        goallist = [None]

    return (goallist, consistency_checks)

def ac3(assignment, var, val, n, m, k):
    new_assignment = {k: v for k, v in assignment.iteritems()}
    new_assignment[var] = val

    arcs = deque([])
    for peer in get_peers(new_assignment, var, n, m, k):
        arcs.append((var, peer))
    
    while len(arcs) > 0:
        x, y = arcs.popleft()
 
        revised = False
        if isinstance(new_assignment[x], int):
            if new_assignment[x] in new_assignment[y]:
                new_assignment[y] = new_assignment[y] - set([new_assignment[x]])
                revised = True
        else:
            for e in new_assignment[x]:
                if not any([f != e for f in new_assignment[y]]):
                    new_assignment[x] = new_assignment[x] - set([e])
                    revised = True

        if revised:
            if len(new_assignment[y]) == 0:
                return None
            for z in get_peers(new_assignment, x, n, m, k) - set([x]):
                arcs.append((x, z))

    return new_assignment

def backtrackingMRVcp(filename):
    ###
    # use backtracking + MRV + cp to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    
    assignment, n, m, k = parse_game_file(filename)
    goal, consistency_checks = backtrack(assignment, n, m, k,
                                         order_variables_mrv,
                                         order_values_lcv,
                                         False, True, 0)

    goallist = []
    if goal is not None:
        for i in xrange(n):
            row = []
            for j in xrange(n):
                row.append(goal[i,j])
            goallist.append(row)
    else:
        goallist = [None]

    return (goallist, consistency_checks)

def is_conflicted(assignment, var, n, m, k):
    i, j = var
    val = assignment[var]

    # row
    if val in set(assignment[i,x] for x in xrange(n)):
        return True

    # column
    if val in set(assignment[x,j] for x in xrange(n)):
        return True

    # subgrid
    if val in set([assignment[x,y]
                   for x in xrange((i/m)*m, (i/m)*m + m)
                   for y in xrange((j/k)*k, (j/k)*k + k)]):
        return True

    return False


def minConflict(filename):
    ###
    # use minConflict to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    
    assignment, n, m, k = parse_game_file(filename)
    max_steps = 10000

    fixed = set([key for key,val in assignment.iteritems()
                 if isinstance(val, int)])

    # initial complete assignment
    for key, v in assignment.iteritems():
        if not key in fixed:
            assignment[key] = list(assignment[key])[0]

    goal = None
    for i in xrange(max_steps):
        if is_assignment_complete(assignment) and\
           is_assignment_consistent(assignment, n):
            goal = assignment
            break

        key = random.choice(assignment.keys())
        while not is_conflicted(assignment, key, n, m, k):
            key = random.choice(assignment.keys())

        peers = get_peers2(assignment, key, n, m, k)
        vals = []
        for val in range(1,n+1):
            conflicts = sum([1 for peer in peers
                             if val == assignment[peer]])
            vals.append((conflicts, val))
        vals = sorted(vals)

        assignment[key] = vals[0][1]

    goallist = []
    if goal is not None:
        for i in xrange(n):
            row = []
            for j in xrange(n):
                row.append(goal[i,j])
            goallist.append(row)
    else:
        goallist = [None]

    return (goallist, 0)
