from Games import TicTacToe, Nim
from GamePlayingAgent import Agent


class TicTacToeDisplay():
    def __init__(self):
        self.game = TicTacToe(board=None, move='X', nDimensions=3)
        self.aiPlayer = Agent()
        self.aiPlayer2 = Agent()

    def display(self):
        print("\n")
        for row in self.game.board:
            print('|'.join(row))
            print('-' * (2 * len(self.game.board) - 1))

    def play(self):
        while not self.game.isTerminal():
            if self.game.move == 'X':   # AI 1
                self.display()
                self.game.move = 'O'
                child = self.aiPlayer.bestMove(self.game, 2, True, 'dynamic')
                self.game.board = child.board
            else:                       # AI 2
                self.display()
                self.game.move = 'X'
                child = self.aiPlayer2.bestMove(self.game, 5, False, 'dynamic')
                self.game.board = child.board

        self.display()


class NimDisplay():
    def __init__(self):
        self.game = Nim(board=None, nDimensions=7)
        self.aiPlayer = Agent()
        self.aiPlayer2 = Agent()

    def display(self):
        print()
        print(self.game.move)
        for row in self.game.board:
            if row > 0:
                print('| ' * row)

    def play(self):
        # Given the rules for this version of Nim is "The player to remove"
        # the final stick loses, we swap the players role (min and max)
        while not self.game.isTerminal():
            if self.game.move == 'X':   # AI 1
                self.display()
                self.game.move = 'O'
                child = self.aiPlayer.bestMove(self.game, 3, False, 'dynamic')
                self.game.board = child.board
            else:                       # AI 2
                self.display()
                self.game.move = 'X'
                child = self.aiPlayer2.bestMove(self.game, 3, True, 'dynamic')
                self.game.board = child.board

        self.display()


if __name__ == "__main__":
    # TicTacToeDisplay().play()
    NimDisplay().play()
