# test_queens.py
#
# ICS 33 Spring 2023
# Project 0: History of Modern
#
# Unit tests for the QueensState class in "queens.py".
#
# Docstrings are not required in your unit tests, though each test does need to have
# a name that clearly indicates its purpose.  Notice, for example, that the provided
# test method is named "test_zero_queen_count_initially" instead of something generic
# like "test_queen_count", since it doesn't entirely test the "queen_count" method,
# but instead focuses on just one aspect of how it behaves.  You'll want to do likewise.

from queens import QueensState
import unittest
from collections import namedtuple
from queens import DuplicateQueenError
from queens import MissingQueenError

Position = namedtuple('Position', ['row', 'column'])  # namedtuple from Queens.py


class TestQueensState(unittest.TestCase):
    def test_zero_queen_count_initially(self):  # should give 0 from count
        state = QueensState(8, 8)
        self.assertEqual(state.queen_count(), 0)

    def test_number_queen_count(self):
        qs = QueensState(8, 8)
        positions = [Position(3, 0)]
        qsnew = qs.with_queens_added(positions)  # STILL NEED TO IMPLEMENT
        assert qsnew.queen_count() == 1

    def test_init_correct(self):  # test to see if works
        board = QueensState(4, 4)
        self.assertEqual(board.rows, 4)
        self.assertEqual(board.columns, 4)
        for row in board.og_board:
            for col in row:
                self.assertEqual(col, None)

    def test_init_failed(self):
        self.assertRaises(TypeError, QueensState, "Wrong", "Wrong")

    def test_queens(self):
        qs = QueensState(6, 5)
        positions = [Position(0, 0), Position(1, 1)]
        qs_new = qs.with_queens_added(positions)
        fp_list = qs_new.queens()
        assert fp_list == [Position(0, 0), Position(1, 1)]

    def test_has_queen_true(self):
        qs = QueensState(4, 4)
        positions = [Position(2, 2)]
        qsnew = qs.with_queens_added(positions)
        verdict = qsnew.has_queen(Position(2, 2))
        self.assertTrue(verdict)

    def test_has_queens_false(self):
        qs = QueensState(4, 4)
        positions = [Position(2, 3)]
        qsnew = qs.with_queens_added(positions)
        verdict = qsnew.has_queen(Position(1, 1))
        self.assertFalse(verdict)

    def test_with_queens_added(self):
        qs = QueensState(4, 4)
        position = [Position(0, 0), Position(1, 1)]
        newboard = qs.with_queens_added(position)
        expected_board = [["Q", None, None, None],
                          [None, "Q", None, None],
                          [None, None, None, None],
                          [None, None, None, None]]
        assert newboard.og_board == expected_board

    def test_with_queens_added_multiple(self):
        qs = QueensState(3, 3)
        board = qs.with_queens_added([Position(2, 2)])
        new = board.with_queens_added([Position(1, 1)])
        hold = new.with_queens_added([Position(0, 0)])
        check = hold.queen_count()
        assert check == 3

    def test_with_queens_added_error(self):  # need to fix
        qs = QueensState(3, 3)
        board = qs.with_queens_added([Position(2, 2)])
        with self.assertRaises(DuplicateQueenError):
            board.with_queens_added([Position(2, 2)])

    def test_with_queens_removed(self):
        qs = QueensState(4, 4)
        position = [Position(0, 0), Position(1, 1)]
        new_board = qs.with_queens_added(position)
        removed_board = new_board.with_queens_removed(position)
        expected_board = [[None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None]]
        assert removed_board.og_board == expected_board

    def test_with_queens_removed_error(self):
        qs = QueensState(3, 3)
        with self.assertRaises(MissingQueenError):
            qs.with_queens_removed([Position(2, 2)])

    def test_missing_queen_error_str(self):
        position = Position(2, 2)
        error = MissingQueenError(position)
        self.assertEqual(str(error), 'missing queen in row 2 column 2')

    def test_duplicate_queen_error_str(self):
        error = DuplicateQueenError(Position(2, 2))
        self.assertEqual(str(error), "duplicate queen in row 2 column 2")

    def test_any_queens_unsafe_true_right_diag_low(self):
        qs = QueensState(3, 5)
        position = [Position(0, 0), Position(1, 1)]
        new_board = qs.with_queens_added(position)
        verdict = new_board.any_queens_unsafe()
        self.assertTrue(verdict)

    def test_any_queens_unsafe_true_right_diag_up(self):
        qs = QueensState(4, 4)
        position = [Position(1, 1), Position(0,2)]
        new_board = qs.with_queens_added(position)
        verdict = new_board.any_queens_unsafe()
        self.assertTrue(verdict)

    def test_any_queens_unsafe_true_right(self):
        qs = QueensState(3, 5)
        position = [Position(0, 0), Position(0, 1)]
        new_board = qs.with_queens_added(position)
        verdict = new_board.any_queens_unsafe()
        self.assertTrue(verdict)

    def test_any_queens_unsafe_true_upper(self):
        qs = QueensState(3, 5)
        position = [Position(0, 0), Position(1, 0)]
        new_board = qs.with_queens_added(position)
        verdict = new_board.any_queens_unsafe()
        self.assertTrue(verdict)

    def test_any_queens_unsafe_false(self):
        qs = QueensState(3,4)
        position = [Position(0, 0),Position(1, 3)]
        new_board = qs.with_queens_added(position)
        verdict = new_board.any_queens_unsafe()
        self.assertFalse(verdict)

    def test_row_col_0_error(self):
        with self.assertRaises(ValueError):
            qs = QueensState(0, 0)

    def test_wrong_spot_missing_error(self):
        qs = QueensState(3, 3)
        with self.assertRaises(IndexError):
            qs.has_queen(Position(10, 10))


if __name__ == '__main__':
    unittest.main()
