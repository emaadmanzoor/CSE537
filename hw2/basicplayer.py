# -*- coding: utf-8 -*-

from util import memoize, run_search_function
import util
import sys

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        k = board.get_k()
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    #score -= abs(3-col)
                    score -= abs(k-1-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    #score += abs(3-col)
                    score += abs(k-1-col)

    return score

def new_evaluate(board):
    """
        Evaluate the board as follows:
            For each contiguous four cells (horizontal, diagonal, vertical),
            count the number of cells occupied by the current player = x
            
            Similary, count the same for the opponent = y.

            From any given cell, three such scores can be computed: one
            for the vertical, one for the horizontal and one for the
            diagonal run. The max of these scores is selected.
            
            The subscore is x^2 - y^2 for each contiguous set of 4 cells.
            (squaring tends to perform better; this is
             what I found heuristically and is not a theoretical
             conclusion.)

                Note: In the general connect-k problem the set is of
                      k cells.

            The total score is then the sum of the scores for all such sets
            of 4 (or k) contiguous cells.
    """
    if board.is_game_over():
        return -10**4 
        
    score = 0
    current_player = board.get_current_player_id()
    other_player = board.get_other_player_id()
    k = board.get_k()
    # iterate half column/row widths since we follow the chains up to 3 (or k)
    #for r in xrange(3):
    for r in xrange(6 - k + 1):
        #for c in xrange(4):
        for c in xrange(7 - k + 1):
            # Current player
            score += max(
                          # 1. Horizontal chains (r, c), (r, c+1), ...
                          #sum([1 for c_i in xrange(c, c+3)
                          sum([1 for c_i in xrange(c, c+k-1)
                          if board.get_cell(r, c_i) == current_player]),

                          # 2. Vertical chains (r, c), (r+1, c), ...
                          #sum([1 for r_i in xrange(r, r+3)
                          sum([1 for r_i in xrange(r, r+k-1)
                               if board.get_cell(r_i, c) == current_player]),

                          # 3. Diagonal chains (r, c), (r+1, c+1), ...
                          #sum([1 for d_i in xrange(3)
                          sum([1 for d_i in xrange(k-1)
                               if board.get_cell(r+d_i, c+d_i) == current_player])
                        ) ** 2

            # Other player
            score -= max(
                            # 1. Horizontal chains (r, c), (r, c+1), ...
                            #sum([1 for c_i in xrange(c, c+3)
                            sum([1 for c_i in xrange(c, c+k-1)
                                 if board.get_cell(r, c_i) == other_player]),

                            # 2. Vertical chains (r, c), (r+1, c), ...
                            #sum([1 for r_i in xrange(r, r+3)
                            sum([1 for r_i in xrange(r, r+k-1)
                                 if board.get_cell(r_i, c) == other_player]),
    
                            # 3. Diagonal chains (r, c), (r+1, c+1), ...
                            #sum([1 for d_i in xrange(3)
                            sum([1 for d_i in xrange(k-1)
                                 if board.get_cell(r+d_i, c+d_i) == other_player])
                        ) ** 2

    return score

new_evaluate = memoize(new_evaluate)

def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()


def minimax(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = False):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """

    # the provided board cannot be an endgame
    assert not is_terminal_fn(depth, board)

    max_utility = -sys.maxint
    max_utility_move = -1
    for move, new_board in get_all_next_moves(board):
        utility = -minimax_decision(new_board, depth-1,
                                    eval_fn,
                                    get_next_moves_fn,
                                    is_terminal_fn, verbose)
        if utility > max_utility:
            max_utility = utility
            max_utility_move = move

    if verbose:
        print 'minimax final:', max_utility, max_utility_move

    return max_utility_move

def minimax_decision(board, depth, eval_fn,
                     get_next_moves_fn, is_terminal_fn,
                     verbose):

    util.NEXPANDED_MINIMAX += 1

    if verbose:
        for i in range(4-depth-1):
            print '\t',
    
    # recursion base case
    if is_terminal_fn(depth, board):
        if verbose:
            print '\tterminal minimax decision', depth, eval_fn(board)
            print board
        return eval_fn(board)
    else:
        if verbose:
            print 'minimax decision, recurse', depth

    # recurse, but flip the eval_fn sign so it switches between MAX/MIN
    max_utility = -sys.maxint
    for move, new_board in get_all_next_moves(board):
        max_utility = max(max_utility,
                          -minimax_decision(new_board, depth-1,
                                            eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn, verbose))

    if verbose:
        for i in range(4-depth-1):
            print '\t',
        print 'minimax decision,', depth, 'recurse result', max_utility

    return max_utility

def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
