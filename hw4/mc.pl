% Missionaries and cannibals
:- import append/3, select/3 from basics.
:- export is_perm/2, is_equivalent/2, transition/2.
:- export valid_state/1, outnumbered/1.

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

%% end helpers

%% Search algorithm

% TODO

%% end search
