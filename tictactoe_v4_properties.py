import sys
from collections import Counter
from enum import Enum
from unittest import TestCase


class Player(Enum):
    X = "X"
    Y = "Y"
    NA = " "


class TicTacToe():
    def __init__(self):
        self.board = [[Player.NA]*3 for _ in range(3)]

    @property
    def player(self):
        plays = Counter(sum(self.board, []))
        if plays[Player.Y] < plays[Player.X]:
            return Player.Y
        else:
            return Player.X

    def __str__(self):
        return "--+---+--\n".join(
            " | ".join(play.value for play in row) + "\n"
            for row in self.board
        )

    def do_move(self, x, y):
        if self.board[x][y] == Player.NA:
            self.board[x][y] = self.player

    @property
    def is_finished(self):
        for row in self.board:
            if row[0] != Player.NA and row[0] == row[1] == row[2]:
                return True

        for column in range(3):
            if self.board[0][column] != Player.NA and self.board[0][column] == self.board[1][column] == self.board[2][column]:
                return True

        if self.board[0][0] != Player.NA and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True

        if self.board[2][0] != Player.NA and self.board[2][0] == self.board[1][1] == self.board[0][2]:
            return True

        return False


class TestTicTacToe(TestCase):
    def setUp(self):
        self.game = TicTacToe()

    def test_basic_play(self):
        self.assertEqual(self.game.player, Player.X)
        self.game.do_move(0, 0)
        self.assertEqual(self.game.player, Player.Y)
        self.game.do_move(0, 1)
        self.assertEqual(self.game.player, Player.X)

    def test_same_move(self):
        self.assertEqual(self.game.player, Player.X)
        self.game.do_move(0, 0)
        self.assertEqual(self.game.player, Player.Y)
        self.game.do_move(0, 0)
        self.assertEqual(self.game.player, Player.Y)

    def test_game_end(self):
        self.assertFalse(self.game.is_finished)
        self.game.do_move(0, 0)
        self.assertFalse(self.game.is_finished)
        self.game.do_move(0, 1)
        self.assertFalse(self.game.is_finished)
        self.game.do_move(1, 0)
        self.assertFalse(self.game.is_finished)
        self.game.do_move(1, 1)
        self.assertFalse(self.game.is_finished)
        self.game.do_move(2, 0)
        self.assertTrue(self.game.is_finished)


def main():
    game = TicTacToe()
    while not game.is_finished:
        print(game)

        move = input(f"Player {game.player.value} move (x y)? ")
        x, y = move.split()

        game.do_move(int(x), int(y))

    print("Game Over!")
    print(game)


if __name__ == "__main__":
    sys.exit(main())