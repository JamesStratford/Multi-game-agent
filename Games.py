from __future__ import annotations
import random


class GameState():
    def __init__(self):
        self.board = None
        pass

    def eval(self) -> float:
        """Evaluates a gamestate and provides a score"""
        pass

    def getBaseline(self) -> GameState:
        """Returns a new gamestate with a random available move been played"""
        pass

    def isTerminal(self) -> bool:
        """Checks if the game is over"""
        pass

    def getWinner(self) -> str:
        """Returns the winner of the game"""
        pass

    def getChildren(self) -> list[GameState]:
        """Returns list of gamestates / available moves"""
        pass

    def getMove(self) -> str:
        """Returns the last played move"""
        pass

    def getMemoization(self, isMax: bool) -> str:
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
        availableMoves = self.getChildren()
        move = random.choice(availableMoves)
        new_board = move.board

        return TicTacToe(new_board, move.getMove(), self.k)

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

    def getMemoization(self, isMax: bool) -> str:
        return str([j for sub in self.board for j in sub]) + " " + str(isMax)


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
        if max(self.board) <= 1:
            if sum(self.board) == 1:
                return 10
            if sum(self.board) == 0:
                return -10

        nimSum = 0
        for pile in self.board:
            nimSum ^= pile

        return 1 if nimSum != 0 else -1

    def getBaseline(self) -> Nim:
        availableMoves = self.getChildren()
        move = random.choice(availableMoves)
        new_board = move.board

        return TicTacToe(new_board, move.getMove(), self.k)

    def isTerminal(self) -> bool:
        return all(pile == 0 for pile in self.board)

    def getWinner(self) -> str:
        if self.isTerminal():
            return self.getMove()
        else:
            return None

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

    def getMemoization(self, isMax: bool) -> str:
        return str([_ for _ in self.board]) + " " + str(isMax)


class TigerAndDogs(GameState):
    def __init__(
            self, board=None, move=None,
            nDimensions: int = 5, dogsKilled=0
    ):
        super().__init__()
        if board is None:
            self.board = [[' ' for _ in range(nDimensions)]
                          for _ in range(nDimensions)]
            for x in range(nDimensions):
                for y in range(nDimensions):
                    if x == 0 or x == nDimensions-1:
                        self.board[x][y] = "O"
                    if y == 0 or y == nDimensions-1:
                        self.board[x][y] = "O"
            self.board[int(nDimensions/2)][int(nDimensions/2)] = "X"
        else:
            self.board = board
        self.k = nDimensions
        self.move = move
        self.tigerWin = False
        self.dogsKilled = dogsKilled

    def tigerSurrounded(self):
        for row in range(self.k):
            for col in range(self.k):
                if self.board[row][col] == "X":
                    moves = self.__getMoves(self.board, row, col, "X")
                    if len(moves) == 0:
                        return True
        return False

    def eval(self) -> float:
        """ChatGPT helped in developing this evaluation function"""
        def numberOfFreeDogs():
            def dogsNotProtectingAnotherDog():
                dogsPos = findPositions("O")

                dogs_protecting = set()
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                              (1, 1), (-1, 1), (-1, -1), (1, -1)]

                for dog in dogsPos:
                    for dx, dy in directions:
                        row, col = dog[0] + dx, dog[1] + dy
                        if 0 <= row < self.k and 0 <= col < self.k:
                            if self.board[row][col] == "O":
                                for dx2, dy2 in directions:
                                    row2, col2 = row + dx2, col + dy2
                                    if 0 <= row2 < self.k and 0 <= col2 \
                                            < self.k:
                                        if self.board[row2][col2] == "X":
                                            dogs_protecting.add(dog)
                                            break

                return len(dogsPos) - len(dogs_protecting)

            return dogsNotProtectingAnotherDog()
            # Dogs that can move without tiger killing friends

        def findPositions(player: str):
            out = []
            for row in range(self.k):
                for col in range(self.k):
                    if self.board[row][col] == player:
                        out.append((row, col,))
            return out

        def distanceToTiger():

            def manhattanDistance(p1, p2):
                return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

            def sumDistToTiger():
                dog_positions = findPositions("O")
                tiger_positions = findPositions("X")

                total_distance = 0
                for dog in dog_positions:
                    min_distance = min(manhattanDistance(dog, tiger)
                                       for tiger in tiger_positions)
                    total_distance += min_distance

                return total_distance

            return sumDistToTiger()

        def score():
            D = self.__getLivingDogs()
            T = self.__getLivingTigers()
            S = int(self.tigerSurrounded())
            A = numberOfFreeDogs()
            DT = distanceToTiger()

            w_D = 1
            w_T = 1
            w_S = 10
            w_A = 0.5
            w_DT = -0.5

            evaluation_score = w_D * D - w_T * T - w_S * S + \
                w_A * A + w_DT * DT
            return evaluation_score

        return score()

    def getBaseline(self) -> Nim:
        availableMoves = self.getChildren()
        move = random.choice(availableMoves)
        new_board = move.board

        return TigerAndDogs(new_board, move.getMove(), self.k, self.dogsKilled)

    def __getLivingDogs(self):
        livingDogs = sum(1 for row in self.board
                         for cell in row if cell == "O")
        return livingDogs

    def __getLivingTigers(self):
        livingTigers = sum(1 for row in self.board
                           for cell in row if cell == "X")
        return livingTigers

    def isTerminal(self) -> bool:
        # Dogs lose
        livingDogs = self.__getLivingDogs()
        if livingDogs <= self.k*3+1 - 6:  # 6 dead dogs
            self.tigerWin = True
            return True

        # Tiger loses
        return self.tigerSurrounded()

    def getWinner(self) -> str:
        if self.isTerminal():
            return "X" if self.tigerWin else "O"
        else:
            return None

    def __getMoves(self, board, x, y, currMove) -> list[tuple[int]]:
        moves = []
        # piece = board[x][y]
        # if piece == "T":
        for x_ in range(-1, 2):
            for y_ in range(-1, 2):
                if x+x_ >= self.k:
                    __x = self.k-1
                elif x+x_ < 0:
                    __x = 0
                else:
                    __x = x+x_

                if y+y_ >= self.k:
                    __y = self.k-1
                elif y+y_ < 0:
                    __y = 0
                else:
                    __y = y+y_

                if board[__x][__y] == " ":
                    # or (__x, __y,) == (x, y,):
                    moves.append((__x, __y,))
        # elif piece == "D":
        #    pass
        return moves

    def __getLine(self, board, tigerPos, dogPos):
        """ChatGPT helped me solve getting the relative lines in this func"""
        line = []
        correspondingPositions = []
        tigerX, tigerY = tigerPos
        dogX, dogY = dogPos

        dx = dogX - tigerX
        # if x == 0 vertical
        dy = dogY - tigerY
        # if y == 0 horizontal

        # if both !=, diagonal
        # if x > 0, left-to-right diag
        # if x < 0, right-to-left diag
        if dx != 0 and dy != 0:
            if dx < 0:
                x, y = tigerX, tigerY
                while x >= 0 and y >= 0:
                    x -= 1
                    y -= 1
                while x < len(board) and y < len(board):
                    line.append(board[x][y])
                    correspondingPositions.append((x, y,))
                    x += 1
                    y += 1
            elif dx > 0:
                x, y = tigerX, tigerY
                while x <= self.k-1 and y > 0:
                    x += 1
                    y -= 1
                while 0 <= x < len(board) and 0 <= y < len(board):
                    line.append(board[x][y])
                    correspondingPositions.append((x, y,))
                    x -= 1
                    y += 1
        elif dx == 0 and dy != 0:
            x = tigerX
            y = 0
            while y < len(board):
                line.append(board[x][y])
                correspondingPositions.append((x, y,))
                y += 1
        elif dx != 0 and dy == 0:
            x = 0
            y = tigerY
            while x < len(board):
                line.append(board[x][y])
                correspondingPositions.append((x, y,))
                x += 1

        return (line, correspondingPositions,)

    def getChildren(self):
        def tigerKillDogs(board, toMove: tuple):
            def killDogs(linePos):
                dogsKilled = 0
                line, pos = linePos
                for i in range(1, len(line) - 1):
                    if line[i] == "X" \
                       and (line[i - 1], line[i + 1]) == ("O", "O"):
                        board[pos[i-1][0]][pos[i-1][1]] = " "
                        board[pos[i+1][0]][pos[i+1][1]] = " "
                        dogsKilled = 2
                        self.dogsKilled += 2
                        break
                return dogsKilled

            deadDogs = 0
            x, y = toMove
            for x_ in range(-1, 2):
                for y_ in range(-1, 2):
                    if x+x_ >= self.k:
                        __x = self.k-1
                    elif x+x_ < 0:
                        __x = 0
                    else:
                        __x = x+x_

                    if y+y_ >= self.k:
                        __y = self.k-1
                    elif y+y_ < 0:
                        __y = 0
                    else:
                        __y = y+y_

                    if board[__x][__y] == "O":
                        linePos = self.__getLine(board, toMove, (__x, __y,))
                        line, pos = linePos
                        if not any(line[i] == line[i + 1] == "O" for i in
                                   range(len(line) - 1)):
                            if sum(1 for x in line if x == "O") > 1:
                                deadDogs = killDogs(linePos)
            return (board, deadDogs,)

        children = []
        for row in range(self.k):
            for col in range(self.k):
                currMove = "O" if self.move == "X" else "X"
                if self.board[row][col] == currMove:
                    for move in self.__getMoves(
                        self.board, row, col, currMove
                    ):
                        new_board = [row.copy() for row in self.board]
                        new_board[row][col] = " "
                        new_board[move[0]][move[1]] = currMove
                        if currMove == "X":
                            deadDogs = tigerKillDogs(
                                new_board, move)
                            new_board = [row.copy() for row in deadDogs[0]]
                            children.append(
                                TigerAndDogs(new_board, self.move, self.k,
                                             deadDogs[1])
                            )
                        else:
                            children.append(
                                TigerAndDogs(new_board, self.move, self.k,
                                             self.dogsKilled)
                            )

        return children

    def getMove(self):
        return self.move

    def getMemoization(self, isMax: bool) -> str:
        return str([j for sub in self.board for j in sub]) + " " + str(isMax)
