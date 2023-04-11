from Games import TicTacToe, Nim, TigerAndDogs
from GamePlayingAgent import Agent


class TicTacToeDisplay():
    def __init__(self):
        self.game = TicTacToe(board=None, move='X', nDimensions=3)
        self.aiPlayer = Agent(maxPlayer=True)
        self.aiPlayer2 = Agent(maxPlayer=False)

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
                child = self.aiPlayer.getNextMove(state=self.game,
                                                  depth=3,
                                                  # isMaxPlayer=True,
                                                  mode='dynamic')
                self.game.board = child.board
            else:                       # AI 2
                self.display()
                self.game.move = 'X'
                child = self.aiPlayer2.getNextMove(state=self.game,
                                                   depth=2,
                                                   # isMaxPlayer=False,
                                                   mode='alphabeta')
                self.game.board = child.board

        self.display()


class NimDisplay():
    def __init__(self):
        self.game = Nim(board=None, nDimensions=7)
        self.aiPlayer = Agent(maxPlayer=True)
        self.aiPlayer2 = Agent(maxPlayer=False)

    def display(self):
        print()
        print(self.game.move)
        for row in self.game.board:
            if row > 0:
                print('| ' * row)

    def play(self):
        while not self.game.isTerminal():
            if self.game.move == 'X':   # AI 1
                self.display()
                self.game.move = 'O'
                child = self.aiPlayer.getNextMove(state=self.game,
                                                  depth=3,
                                                  # isMaxPlayer=False,
                                                  mode='dynamic')
                self.game.board = child.board
            else:                       # AI 2
                self.display()
                self.game.move = 'X'
                child = self.aiPlayer2.getNextMove(state=self.game,
                                                   depth=3,
                                                   # isMaxPlayer=True,
                                                   mode='dynamic')
                self.game.board = child.board

        self.display()
        print(self.game.getWinner(), " has won the game!")


class TigerAndDogsDisplay():
    def __init__(self):
        self.game = TigerAndDogs(board=None, nDimensions=5)
        self.aiPlayer = Agent(maxPlayer=True)
        self.aiPlayer2 = Agent(maxPlayer=False)

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
                child = self.aiPlayer.getNextMove(state=self.game,
                                                  depth=2,
                                                  mode='baseline')
                self.game.board = child.board
            else:                       # AI 2
                self.display()
                self.game.move = 'X'
                child = self.aiPlayer2.getNextMove(state=self.game,
                                                   depth=3,
                                                   mode='dynamic')
                self.game.board = child.board
            # time.sleep(0.5)

        self.display()
        print(self.game.getWinner(), " has won the game!")


if __name__ == "__main__":
    # TicTacToeDisplay().play()
    # NimDisplay().play()
    TigerAndDogsDisplay().play()
