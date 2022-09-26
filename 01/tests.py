import unittest
import io
import sys
from main import TicTacGame


class TestGame(unittest.TestCase):

    def test_validate_input(self):
        game = TicTacGame()
        self.assertTrue(game.validate_input('a1'))
        self.assertEqual(game.validate_input('a1'), 1)
        self.assertEqual(game.validate_input('b2'), 5)
        self.assertEqual(game.validate_input('c3'), 9)
        game.cells = ['_', '_', '_', '_', '_', '_', '_', '_', 'X']
        self.assertEqual(game.validate_input('c3'), -4)
        self.assertEqual(game.validate_input('c3c'), -1)
        self.assertEqual(game.validate_input('cc'), -2)
        self.assertEqual(game.validate_input('c4'), -3)

    def test_check_winner(self):
        game = TicTacGame()
        game.move = 'X'
        game.cells = ['X', '0', 'X', '0', 'X', '0', 'X', '_', '_']
        self.assertTrue(game.check_winner())
        game.cells = ['X', 'X', '0', '0', 'X', '0', '0', 'X', '_']
        self.assertTrue(game.check_winner())
        game.cells = ['X', 'X', '0', '0', 'X', 'X', 'X', '0', '0']
        self.assertFalse(game.check_winner())
        game.cells = ['X', 'X', 'X', '0', '_', '0', 'X', '_', '0']
        self.assertTrue(game.check_winner())
        game.cells = ['X', '0', 'X', '0', 'X', '0', 'X', '_', '_']
        game.move = '0'
        self.assertFalse(game.check_winner())

    def test_print(self):
        exceptions = [
            "Неверное количество символов\n",
            "Введен символ вместа числа\n",
            "Такой ячейки не существует\n",
            "Данная ячейка занята\n"
        ]
        self.assertEqual(self.get_stdout(-1).getvalue(), exceptions[0])
        self.assertEqual(self.get_stdout(-2).getvalue(), exceptions[1])
        self.assertEqual(self.get_stdout(-3).getvalue(), exceptions[2])
        self.assertEqual(self.get_stdout(-4).getvalue(), exceptions[3])

    @staticmethod
    def get_stdout(err):
        game = TicTacGame()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        game.print_err(err)
        sys.stdout = sys.__stdout__
        return captured_output

