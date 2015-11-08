% Missionaries and cannibals
:- import append/3, select/3, length/2, member/2 from basics.
:- import format/2 from format.
:- export is_perm/2, is_equivalent/2, transition/2.
:- export valid_state/1, outnumbered/1.
:- export find_solution/0, showlist/1, last/2.

%% State space definition

% initially, all missionaries (m) and cannibals (c)
% are on the same bank along with the boat (b).
initial_state([b, m, m, m, c, c, c] + []).

% goal
goal_state([] + [b, m, m, m, c, c, c]).

% valid states (cannibals don't outnumber missionaries)
valid_state(L + R) :-
  \+ outnumbered(L),
  \+ outnumbered(R).

% with the boat
outnumbered(S):- is_perm(S, [b, c, c, c, m, m]).
outnumbered(S):- is_perm(S, [b, c, c, c, m]).
outnumbered(S):- is_perm(S, [b, c, c, m]).
% without the boat
outnumbered(S):- is_perm(S, [c, c, c, m, m]).
outnumbered(S):- is_perm(S, [c, c, c, m]).
outnumbered(S):- is_perm(S, [c, c, m]).

%% end state space

%% Transitions
%%    Old banks: L1, R1
%%    New banks: L2, R2

% move one passenger from L to R
transition(L1 + R1, L2 + [b, Passenger | R1]) :-
  select(b, L1, L1_without_boat),
  select(Passenger, L1_without_boat, L2).

% move two passengers from L to R
transition(L1 + R1, L2 + [b, Passenger1, Passenger2 | R1]) :-
  select(b, L1, L1_without_boat),
  select(Passenger1, L1_without_boat, L1_without_boat2),
  select(Passenger2, L1_without_boat2, L2).

% move one passenger from R to L
transition(L1 + R1, [b, Passengers | L1] + R2) :-
  select(b, R1, R1_without_boat),
  select(Passengers, R1_without_boat, R2).

% move two passengers from R to L
transition(L1 + R1, [b, Passenger1, Passenger2 | L1] + R2) :-
  select(b, R1, R1_without_boat),
  select(Passenger1, R1_without_boat, R1_without_boat2),
  select(Passenger2, R1_without_boat2, R2).

%% end transitions

%% Helper functions

% check if states are equivalent
% order of b/m/c does not matter
is_equivalent(H1+T1, H2+T2) :-
  is_perm(H1, H2), is_perm(T1, T2).

% check if list s1 is a permutation of s2
is_perm([], []). % base case
is_perm(L, [H|T]) :-
  append(V, [H|U], L), % L = V + H + U, where
  append(V, U, W),     %  V + U = W, and
  is_perm(W, T).       %  W is a permutation of T

last([X],X).
last([_|L],X) :- last(L,X).

%% end helpers

%% Search algorithm (BFS)
%% Based on this tutorial: http://www.comp.leeds.ac.uk/brandon/vle/prolog_intro/prolog-intro-ex.pdf
%% (adapted for XSB Prolog)

find_solution :-
          initial_state( Initial ),
          goal_state( Goal ),
          solution( [[Initial]], Goal, StateList ),
          length( StateList, Len ),
          Transitions is Len -1,
          format( '~n** Solution path (each line is a boat move) (length = ~d) **', [Transitions] ), nl,
          showlist( StateList ).

%% Base case for finding solution.
%% Find a statelist whose last state is the goal or
%% or some state equivalent to the goal.
solution( StateLists, Goal, StateList ) :-
          member( StateList, StateLists ),
          last( StateList, Last ),
          is_equivalent( Last, Goal ).
          %report_progress( StateLists, final ).

%% Recursive rule that looks for a solution by extending
%% each of the generated state lists to add a further state.
solution( StateLists, Goal, StateList ) :-
          %report_progress( StateLists, ongoing ),
          extend( StateLists, Extensions ),
          solution( Extensions, Goal, StateList ).

%% Extend each statelist in a set of possible state lists.
%% If loopcheck(on) will not extend to any state previously reached
%% in any of the state lists, to avoid loops.
extend( StateLists, ExtendedStateLists ) :-
     setof( ExtendedStateList,
            StateList^Last^Next^( member( StateList, StateLists ),
                                  last( StateList, Last ),
                                  transition( Last, Next ),
                                  valid_state( Next ),
                                  no_loop_or_loopcheck_off( Next, StateLists ),
                                  append( StateList, [Next], ExtendedStateList )
                                ),
             ExtendedStateLists
           ).

no_loop_or_loopcheck_off( _, _) :- loopcheck(off), !.
no_loop_or_loopcheck_off( Next, StateLists ) :-
                        \+( already_reached( Next, StateLists ) ).

%% Check whether State (or some equivalent state) has already been
%% reached in any state list in StateLists.
already_reached( State,  StateLists ) :-
           member( StateList, StateLists ),
           member( State1, StateList ),
           is_equivalent( State, State1 ).

%% Print out list, each element on a separate line.
showlist([]).
showlist([H | T]) :- write( H ), nl, showlist( T ).

%% Report progress after each cycle of the planner:
report_progress( StateLists, Status ) :-
      length( StateLists, NS ),
      member( L , StateLists ), length( L, N ),
      Nminus1 is N - 1,
      write( 'Found '), write( NS ),
      write( ' states reachable in path length ' ), write(Nminus1), nl,
      ( Status = ongoing -> (write( 'Computing extensions of length : ' ), write(N), nl) ; true ).

%% end search

loopcheck(on).
:- find_solution.
