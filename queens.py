# queens.py
#
# ICS 33 Spring 2023
# Project 0: History of Modern
#
# A module containing tools that could assist in solving variants of the
# well-known "n-queens" problem.  Note that we're only implementing one part
# of the problem: immutably managing the "state" of the board (i.e., which
# queens are arranged in which cells).  The rest of the problem -- determining
# a valid solution for it -- is not our focus here.
#
# Your goal is to complete the QueensState class described below, though
# you'll need to build it incrementally, as well as test it incrementally by
# writing unit tests in test_queens.py.  Make sure you've read the project
# write-up before you proceed, as it will explain the requirements around
# following (and documenting) an incremental process of solving this problem.
#
# DO NOT MODIFY THE Position NAMEDTUPLE OR THE PROVIDED EXCEPTION CLASSES.

from collections import namedtuple
from typing import Self

Position = namedtuple('Position', ['row', 'column'])

# Ordinarily, we would write docstrings within classes or their methods.
# Since a namedtuple builds those classes and methods for us, we instead
# add the documentation by hand afterward.
Position.__doc__ = 'A position on a chessboard, specified by zero-based row and column numbers.'
Position.row.__doc__ = 'A zero-based row number'
Position.column.__doc__ = 'A zero-based column number'


class DuplicateQueenError(Exception):
    """An exception indicating an attempt to add a queen where one is already present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where the duplicate queen exists."""
        self._position = position

    def __str__(self) -> str:
        return f'duplicate queen in row {self._position.row} column {self._position.column}'


class MissingQueenError(Exception):
    """An exception indicating an attempt to remove a queen where one is not present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where a queen is missing."""
        self._position = position

    def __str__(self) -> str:
        return f'missing queen in row {self._position.row} column {self._position.column}'


class QueensState:
    """Immutably represents the state of a chessboard being used to assist in
    solving the n-queens problem."""

    def __init__(self, rows: int, columns: int):
        """Initializes the chessboard to have the given numbers of rows and columns,
        with no queens occupying any of its cells."""
        self.rows = rows
        self.columns = columns
        self.og_board = []
        if self.rows <= 0 or self.columns <= 0:
            raise ValueError
        else:
            pass
        for r in range(rows):
            rl = []
            for c in range(columns):
                rl.append(None)
            self.og_board.append(rl)

    def queen_count(self) -> int:
        """Returns the number of queens on the chessboard."""
        count = 0
        for row in range(self.rows):
            for col in range(self.columns):
                if self.og_board[row][col] == "Q":
                    count += 1
        return count

    def queens(self) -> list[Position]:
        """Returns a list of the positions in which queens appear on the chessboard,
        arranged in no particular order."""
        full_position_list = []
        for row in range(self.rows):
            for col in range(self.columns):
                if self.og_board[row][col] == "Q":
                    full_position_list.append(Position(row, col))
        return full_position_list

    def has_queen(self, position: Position) -> bool:
        """Returns True if a queen occupies the given position on the chessboard, or
        False otherwise."""
        try:
            for row in range(self.rows):
                for col in range(self.columns):
                    if self.og_board[position.row][position.column] == "Q":
                        return True
            return False
        except IndexError:
            raise IndexError("You cannot access this part of the board because it doesn't exist")
            # quit() I am not sure if you want this part of the code to quit, it makes it more clean, yet I don't
            # know if u want it to still run

    def any_queens_unsafe(self) -> bool:

        """Returns True if any queens on the chessboard are unsafe (i.e., they can
            be captured by at least one other queen on the chessboard), or False otherwise."""
        # expected_board = [["Q"", None, None, None],   3x4 board
        #                  [None, None, "Q", None],
        #                 [None, None, None, None],
        total_positions = self.queens()
        for single_pos in total_positions:
            s_row = single_pos[0]
            s_col = single_pos[1]
            for i in range(s_col + 1, len(self.og_board)):
                if self.og_board[s_row][i] == "Q":
                    return True  # To check right
            for i in range(s_row - 1, -1, -1):
                if self.og_board[i][s_col] == "Q":
                    return True  # To check upper
            for i in range(1, len(self.og_board)):
                if s_row - i >= 0 and s_col + i <= self.columns - 1:
                    if self.og_board[s_row - i][s_col + i] == "Q":
                        return True
                    # Check upper right diagonal
            for i in range(1, len(self.og_board)):
                if s_row + i <= self.rows - 1 and s_col + i <= self.columns - 1:
                    if self.og_board[s_row + i][s_col + i] == "Q":
                        return True
                    # check down diagonal
        return False

    def with_queens_added(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens added in the given positions.
        Raises a DuplicateQueenException when there is already a queen in at
        least one of the given positions."""
        new_board = []
        for i in range(self.rows):
            n_row = []
            for j in range(self.columns):
                n_row.append(self.og_board[i][j])
            new_board.append(n_row)

        for single_pos in positions:  # list of pos [[1,2],[1,4]]
            if self.has_queen(single_pos):
                raise DuplicateQueenError(single_pos)
            else:
                row_col = Position(single_pos[0], single_pos[1])
                new_board[row_col.row][row_col.column] = "Q"

        new_queen_state = QueensState(self.rows, self.columns)
        new_queen_state.og_board = new_board  # if this isn't allowed, instead instantiate a blank QueensState
        return new_queen_state

    def with_queens_removed(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens removed from the given positions.
        Raises a MissingQueenException when there is no queen in at least one of
    the given positions."""
        new_board = []
        for i in range(self.rows):
            n_row = []
            for j in range(self.columns):
                n_row.append(self.og_board[i][j])
            new_board.append(n_row)

        for single_pos in positions:  # list of pos [[1,2],[1,4]]
            if not self.has_queen(single_pos):
                raise MissingQueenError(single_pos)
            else:
                row_col = Position(single_pos[0], single_pos[1])
                new_board[row_col.row][row_col.column] = None

        new_queen_state = QueensState(self.rows, self.columns)
        new_queen_state.og_board = new_board  # if this isn't allowed, instead instantiate a blank QueensState
        return new_queen_state


# qs = QueensState(3, 6)
'''
board = qs.with_queens_added([Position(2, 2)])
new = board.with_queens_added([Position(1, 1)])
hold = new.with_queens_added([Position(0, 0)])

print(qs.og_board)
print(board.og_board)
print(new.og_board)
print(hold.og_board)
print(qs.og_board)
'''
# newman = qs.with_queens_removed([Position(8, 8)])??
