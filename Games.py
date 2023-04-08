from __future__ import annotations


class GameState():
    def __int__(self):
        self.board = None
        pass

    def eval(self) -> float:
        pass

    def isTerminal(self) -> bool:
        pass

    def getChildren(self) -> list[GameState]:
        pass

    def getMove(self) -> str:
        pass


class TicTacToe(GameState):
    memo = {}

    def __init__(self, board=None, move=None, nDimensions: int = 3):
        super().__init__()
        if board is None:
            self.board = [[' ' for _ in range(nDimensions)]
                          for _ in range(nDimensions)]
        else:
            self.board = board
        self.k = nDimensions
        self.move = move

    def eval(self) -> float:
        def count(player):
            opponent = "O" if player == "X" else "X"
            playerScore = 0
            opponentScore = 0

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

            for line in generateLines(self.k):
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
                elif playerCount == self.k - 1 and opponentCount == 0:
                    playerScore += 3
                # Opponent about to win / block them
                elif opponentCount == self.k - 1 and playerCount == 0:
                    opponentScore += 3
                # Keep trying to fill the winnable lines
                elif playerCount >= 1 and opponentCount == 0:
                    playerScore += 1
                elif opponentCount >= 1 and playerCount == 0:
                    opponentScore += 1

            return playerScore - opponentScore
        return count("X") - count("O")

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

    def getChildren(self):
        children = []
        for row in range(self.k):
            for col in range(self.k):
                if self.board[row][col] == ' ':
                    new_board = [row.copy() for row in self.board]
                    # self.move = 'X' if self.move == 'O' else 'O'
                    new_board[row][col] = 'X' if self.move == 'O' else 'O'

                    children.append(TicTacToe(new_board, new_board[row][col],
                                              self.k))
        return children

    def getMove(self):
        return self.move
