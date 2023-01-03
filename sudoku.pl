% sudoku.pl - A simple sudoku solver in Prolog
:- use_module(library(clpfd)).

% Resolve the sudoku puzzle, Board is a list of lists that represents the puzzle
sudoku(Board) :-
    length(Board, 9),
    maplist(same_length(Board), Board),
    flatten(Board, FullBoard),
    FullBoard ins 1..9,
    Rows = Board,
    maplist(all_distinct, Rows),
    Rows = [R1, R2, R3, R4, R5, R6, R7, R8, R9],
    columns(R1, R2, R3, R4, R5, R6, R7, R8, R9),
    blocks(R1, R2, R3), blocks(R4, R5, R6), blocks(R7, R8, R9),
    label(FullBoard).

% Check if all the elements in a column are different by checking the n-th
% element of each row recursively until they are empty
columns([], [], [], [], [], [], [], [], []).
columns([A|Ac],[B|Bc],[C|Cc],[D|Dc],[E|Ec],[F|Fc],[G|Gc],[H|Hc],[I|Ic]) :-
    all_distinct([A, B, C, D, E, F, G, H, I]),
    columns(Ac, Bc, Cc, Dc, Ec, Fc, Gc, Hc, Ic).

% Check if all the elements in a 3x3 block are different by checking the 
% 9 elements of the block recursively until there are no more blocks
blocks([], [], []).
blocks([X1,X2,X3|B1], [X4,X5,X6|B2], [X7,X8,X9|B3]) :-
    all_distinct([X1, X2, X3, X4, X5, X6, X7, X8, X9]),
    blocks(B1, B2, B3).