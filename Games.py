from __future__ import annotations
from random import Random
import time


class GameState():
    def __init__(self):
        self.board = None
        pass

    def eval(self) -> float:
        pass

    def getBaseline(self) -> GameState:
        pass

    def isTerminal(self) -> bool:
        pass

    def getChildren(self) -> list[GameState]:
        pass

    def getMove(self) -> str:
        pass

    def getMemoization(self) -> str:
        """Returns a unique string that represents the board"""
        pass


class TicTacToe(GameState):
    def __init__(self, board=None, move=None, nDimensions: int = 3):
        super().__init__()
        if board is None:
            self.board = [[' ' for _ in range(nDimensions)]
                          for _ in range(nDimensions)]
        else:
            self.board = board
        self.k = nDimensions
        self.move = move

        def generateLines(n):
            lines = []
            for i in range(n):
                # Horizontal lines
                lines.append([(i, j) for j in range(n)])
                # Vertical lines
                lines.append([(j, i) for j in range(n)])
            # Diagonal lines
            lines.append([(i, i) for i in range(n)])
            lines.append([(i, n - i - 1) for i in range(n)])
            return lines

        self.lines = generateLines(self.k)

    def eval(self) -> float:
        def count(player):
            opponent = "O" if player == "X" else "X"
            playerScore = 0
            opponentScore = 0

            for line in self.lines:
                # Get count of both players per line
                playerCount = sum([1 for x, y in line
                                   if self.board[x][y] == player])
                opponentCount = sum([1 for x, y in line
                                     if self.board[x][y] == opponent])

                if playerCount == self.k:
                    return 10       # Win
                elif opponentCount == self.k:
                    return -10      # Lose
                # About to win
                if playerCount == self.k - 1 and opponentCount == 0:
                    playerScore += 2
                # Opponent about to win / block them
                if opponentCount == self.k - 1 and playerCount == 0:
                    opponentScore += 2
                # Keep trying to fill the winnable lines
                if playerCount >= 1 and opponentCount == 0:
                    playerScore += 1
                if opponentCount >= 1 and playerCount == 0:
                    opponentScore += 1

            return playerScore - opponentScore
        return count("X") - count("O")

    def getBaseline(self) -> GameState:
        availableMoves = []
        for x, rows in enumerate(self.board):
            for y, col in enumerate(rows):
                if col == " ":
                    availableMoves.append((x, y,))
        x, y = availableMoves[
            Random((int)(time.time())).randint(0, len(availableMoves)-1)
        ]

        new_board = [row.copy() for row in self.board]
        new_board[x][y] = 'X' if self.move == 'O' else 'O'

        return TicTacToe(new_board, new_board[x][y], self.k)

    def isTerminal(self) -> bool:
        """Returns True if game is over"""

        for row in range(self.k):
            if all(self.board[row][col] == self.board[row][0] and
                   self.board[row][0] != ' ' for col in range(self.k)):
                return True

        # Check columns
        for col in range(self.k):
            if all(self.board[row][col] == self.board[0][col] and
                   self.board[0][col] != ' ' for row in range(self.k)):
                return True

        # Check diagonals
        if all(self.board[i][i] == self.board[0][0] and
               self.board[0][0] != ' ' for i in range(self.k)):
            return True
        if all(self.board[i][self.k - i - 1] == self.board[0][self.k - 1] and
               self.board[0][self.k - 1] != ' ' for i in range(self.k)):
            return True

        # Check for an empty cell
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False

        # Board is full (tied)
        return True

    def getWinner(self):
        # Check rows
        for row in range(self.k):
            if all(self.board[row][col] == self.board[row][0] and
                   self.board[row][0] != ' ' for col in range(self.k)):
                return self.board[row][0]

        # Check columns
        for col in range(self.k):
            if all(self.board[row][col] == self.board[0][col] and
                   self.board[0][col] != ' ' for row in range(self.k)):
                return self.board[0][col]

        # Check diagonals
        if all(self.board[i][i] == self.board[0][0] and
               self.board[0][0] != ' ' for i in range(self.k)):
            return self.board[0][0]
        if all(self.board[i][self.k - i - 1] == self.board[0][self.k - 1] and
               self.board[0][self.k - 1] != ' ' for i in range(self.k)):
            return self.board[0][self.k - 1]

        return None

    def getChildren(self):
        children = []
        for row in range(self.k):
            for col in range(self.k):
                if self.board[row][col] == ' ':
                    new_board = [row.copy() for row in self.board]
                    new_board[row][col] = 'X' if self.move == 'O' else 'O'
                    children.append(TicTacToe(new_board, new_board[row][col],
                                              self.k))
        return children

    def getMove(self):
        return self.move

    def getMemoization(self) -> str:
        return str([j for sub in self.board for j in sub])


class Nim(GameState):
    def __init__(self, board=None, move=None, nDimensions: int = 3):
        super().__init__()
        if board is None:
            val = 1
            self.board = [val + _ * 2 for _ in range(nDimensions)]
        else:
            self.board = board
        self.k = nDimensions
        self.move = move

    def eval(self) -> float:
        nimSum = 0
        for pile in self.board:
            nimSum ^= pile
        return nimSum

    def getBaseline(self) -> Nim:
        availableMoves = []
        for x, pile in enumerate(self.board):
            if pile > 0:
                availableMoves.append((x, pile,))
        x, maxPile = availableMoves[
            Random((int)(time.time())).randint(0, len(availableMoves)-1)
        ]

        new_board = self.board.copy()
        new_board[x] = maxPile - Random((int)(time.time())).randint(1, maxPile)

        return Nim(new_board, new_board[x], self.k)

    def isTerminal(self) -> bool:
        return all(pile == 0 for pile in self.board)

    def getChildren(self) -> list[int]:
        children = []
        for i, pile in enumerate(self.board):
            if pile > 0:
                # Must take a minimum of 1 stick
                for j in range(1, pile + 1):
                    new_board = self.board.copy()
                    new_board[i] -= j
                    children.append(Nim(new_board,
                                        new_board[i],
                                        self.k))
        return children
    
    def getMove(self):
        return self.move

    def getMemoization(self) -> str:
        return str([_ for _ in self.board])
