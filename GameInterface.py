from Games import TicTacToe
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


if __name__ == "__main__":
    TicTacToeDisplay().play()
