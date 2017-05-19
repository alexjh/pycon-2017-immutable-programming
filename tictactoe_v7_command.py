import sys
from collections import Counter, namedtuple
from enum import Enum
from unittest import TestCase
from random import randrange


class Player(Enum):
    X = "X"
    O = "O"
    NA = " "


# COMMAND-START
class Undo(namedtuple('_Undo', ['count'])):
    def apply(self, board_states):
        return board_states[:-self.count]

class Move(namedtuple('_Move', ['x', 'y'])):
    def apply(self, board_states):
        if board_states[-1].board[self.x][self.y] == Player.NA:
            return board_states + (
                board_states[-1].do_move(self.x, self.y),
            )
        else:
            return board_states

class RevertTo(namedtuple('_RevertTo', ['idx'])):
    def apply(self, board_states):
        return board_states[:self.idx]
# COMMAND-END


def replace(tpl, idx, value):
    return tpl[:idx] + (value, ) + tpl[idx+1:]


class BoardState(namedtuple('_Board', ['board'])):

    @property
    def player(self):
        plays = Counter(sum(self.board, ()))
        if plays[Player.O] < plays[Player.X]:
            return Player.O
        else:
            return Player.X

    def __str__(self):
        return "--+---+--\n".join(
            " | ".join(play.value for play in row) + "\n"
            for row in self.board
        )

    def do_move(self, x, y):
        if self.board[x][y] == Player.NA:
            return BoardState(
                replace(self.board, x, replace(self.board[x], y, self.player))
            )
        else:
            return self

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

        if all(all(col != Player.NA for col in row) for row in self.board):
            return True

        return False

BoardState.__new__.__defaults__ = (((Player.NA,)*3,)*3,)

class TestTicTacToe(TestCase):
    def test_basic_play(self):
        initial = BoardState()
        all_moves = [(x, y) for x in range(3) for y in range(3)]
        for (x0, y0) in all_moves:
            with self.subTest(x0=x0, y0=y0):
                after_first = initial.do_move(x0, y0)
                self.assertNotEqual(initial.player, after_first.player)
                self.assertNotEqual(initial.board, after_first.board)
                for (x1, y1) in all_moves:
                    with self.subTest(x1=x1, y1=y1):
                        after_second = after_first.do_move(x1, y1)
                        if x1 == x0 and y1 == y0:
                            self.assertEqual(after_first.player, after_second.player)
                            self.assertEqual(after_first.board, after_second.board)
                        else:
                            self.assertNotEqual(initial.player, after_first.player)
                            self.assertNotEqual(initial.board, after_first.board)


# PLAYER-START
def move_human(state):

    while True:
        print(state)
        move = input(f"Player {state.player.value}: "
                      "x y to move, u to undo, "
                      "gN to revert to move N)? ")
        if move.startswith('u'):
            return Undo(1)
        elif move.startswith('g'):
            return RevertTo(int(move.replace('g', '')) + 1)
        else:
            try:
                x, y = move.split()
                return Move(int(x), int(y))
            except:
                print("Invalid move")
# PLAYER-END

# RANDOM-START
def move_random(state):
    x = randrange(3)
    y = randrange(3)

    return Move(x, y)
# RANDOM-END


class TestCommands(TestCase):

    def setUp(self):
        self.states = (
            BoardState(),
            BoardState().do_move(1, 1),
            BoardState().do_move(1, 1).do_move(0, 0),
            BoardState().do_move(1, 1).do_move(0, 0).do_move(0, 2),
        )

    def test_undo(self):
        self.assertEqual(
            Undo(1).apply(self.states),
            self.states[:-1]
        )

    # TEST-START
    def test_revert(self):
        self.assertEqual(
            RevertTo(2).apply(self.states),
            self.states[:2]
        )

    def test_inverse(self):
        start = (BoardState(), )
        for x in range(3):
            for y in range(3):
                self.assertEqual(
                    Undo(1).apply(Move(x, y).apply(start)),
                    start
                )
    # TEST-END

    def test_move(self):
        self.assertEqual(
            Move(2, 2).apply(self.states),
            self.states + (self.states[-1].do_move(2, 2), )
        )


def main():
    x_choice = int(input("Player X: 0 for human, 1 for AI: "))
    y_choice = int(input("Player Y: 0 for human, 1 for AI: "))

    # LOOP-START
    player_types = [move_human, move_random]
    players = {
        Player.X: player_types[x_choice],
        Player.O: player_types[y_choice],
    }

    states = (BoardState(), )
    while not states[-1].is_finished:
        move = players[states[-1].player](states[-1])
        states = move.apply(states)
    # LOOP-END

    print("Game Over!")
    for state in states:
        print(state)


if __name__ == "__main__":
    sys.exit(main())