import sys

import itertools

def parse_file(filepath):
    # read the layout file to the board array
    board = {}
    constraints = []
    variables = {}
    nvars = 0
    height, width = -1, -1
    with open(filepath) as fin:
        height, width = map(int, fin.readline().split(' '))
        for h in xrange(height):
            for w, x in enumerate(fin.readline().strip().split(',')):
                if x.lower() == 'x': # variable 
                    nvars += 1
                    board[h,w] = -1
                    variables[h,w] = nvars
                else: # constraint
                    board[h,w] = int(x)
                    constraints.append((h,w))
    return board, height, width, tuple(constraints), variables

def print_board(board, height, width):
    for i in xrange(height):
        for j in xrange(width):
            print board[i,j], '\t',
        print

def get_neighbors(constraint, height, width):
    h, w = constraint
    neighbors = [(h + deltah, w + deltaw)
                 for deltah, deltaw in itertools.product([-1,0,1],[-1,0,1])
                 if (deltah != 0 or deltaw != 0) and
                    h + deltah >= 0 and w + deltaw >= 0 and
                    h + deltah < height and w + deltaw < width]
    return neighbors

def convert2CNF(board, height, width, constraints, variables, output, filepath):
    # interpret the number constraints

    clauses = set([])
    for constraint in constraints:
        k = board[constraint]
        neighbor_vars = [neighbor
                         for neighbor in get_neighbors(constraint, height, width)
                         if board[neighbor] < 0]
        n = len(neighbor_vars)

        assert k >= 0

        """
        Exactly k out of n neighboring variables is true
        
        This can be interpreted as:
            - at most k of n neigbors is true           -- A
            - at least k of n neighbors is true AND     -- B

        Each of A and B can be represented as a conjunction
        of disjunctions as follows.

        P: Preliminaries

            A disjunction of p variables is equivalent to
            saying that at least 1 of p variables is true.

        A: At most k of n are true

            This means that in any size-(k+1) subset of n,
            at least 1 is false.
            
            Using preliminary P, at least 1 of (k+1) variables
            is false; so the clause for A is a disjunction
            of -x for x in the size-(k+1) subset of n.

        B: At least k of n are true
        
            This is equivalent to:

              At most n-k of n are false

            Using the same logic as in A, this means that in
            any size-(n-k+1) subset of n, at least 1 is true.

            Using prelimary P, the clause for B is a disjunction
            of x for x in the size-(n-k+1) subset of n.
        """

        if k == 0: # no neighbor has a mine
            clauses.update([tuple([-variables[v]]) for v in neighbor_vars])
        elif k == n: # all neighbors have a mine
            clauses.update([tuple([variables[v]]) for v in neighbor_vars])
        elif k > n: # invalid, should be UNSAT
            #print 'WARNING: Invalid board at:', constraint, 'in', filepath.strip()
            #print 'k =', k, 'mines expected, but only n =', n, 'variables'
            clauses.update([tuple([-variables[v]]) for v in neighbor_vars])
            clauses.update([tuple([variables[v]]) for v in neighbor_vars])
        else:
            A = [tuple([-variables[v] for v in s]) # size-(k+1) clause
                 for s in itertools.combinations(neighbor_vars, k + 1)]
            B = [tuple([variables[v] for v in s])
                 for s in itertools.combinations(neighbor_vars, n - k + 1)] 
            clauses.update(A + B)

        #print 'k =', k, 'n =', n, 'neighbors', neighbor_vars,
        #print [variables[v] for v in neighbor_vars]
        #print clauses

    clauses = sorted(list(clauses), key=lambda c: (len(c), c))

    with open(output, 'w') as fout:
        fout.write('c ' + filepath.strip() + '\n')
        fout.write('p cnf ' + str(len(variables)) + ' ' + str(len(clauses)) + '\n')
        for clause in clauses:
            fout.write(' '.join([str(v) for v in clause]) + ' 0\n')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board, height, width, constraints, variables = parse_file(sys.argv[1])
    convert2CNF(board, height, width, constraints, variables, sys.argv[2],
                sys.argv[1])
