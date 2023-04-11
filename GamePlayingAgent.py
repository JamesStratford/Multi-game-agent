from Games import GameState


class Player():
    def __init__(self) -> None:
        pass

    def getNextMove(self, **kwargs):
        pass


class Human(Player):
    def __init__(self) -> None:
        super().__init__()
        self.turn = False

    def getNextMove(self, state: GameState, **kwargs):
        while self.turn is True:
            pass
        return state


class Agent(Player):
    def __init__(self, depth=5, maxPlayer=True):
        super().__init__()
        self.memo = {}
        self.minimaxMethod = None
        self.__maxPlayer = maxPlayer
        self.depth = depth

    def setMinimax(self, mode: str = "alphabeta"):
        """
        'minimax' for basic minimax
        'alphabeta' for alpha beta pruning minimax
        'dynamic' for AB minimax using memoization
        """
        if mode == "baseline":
            self.minimaxMethod = self.__baseline
        elif mode == "minimax":
            self.minimaxMethod = self.__miniMax
        elif mode == "alphabeta":
            self.minimaxMethod = self.__miniMaxAlphaBeta
        elif mode == "dynamic":
            self.minimaxMethod = self.__miniMaxABDynamic

    def __baseline(self, state: GameState, **kwargs) -> GameState:
        return state.getBaseline()

    def __miniMax(self, state: GameState, depth: int,
                  isMaxPlayer: bool, **kwargs):
        if depth == 0 or state.isTerminal():
            return state.eval()

        if isMaxPlayer:
            value = float('-inf')
            for child in state.getChildren():
                value = max(value, self.__miniMax(
                    child, depth - 1, False))
        else:
            value = float('inf')
            for child in state.getChildren():
                value = min(value, self.__miniMax(
                    child, depth - 1, True))

        return value

    def __miniMaxAlphaBeta(self, state: GameState, depth: int,
                           isMaxPlayer: bool, **kwargs):
        if depth == 0 or state.isTerminal():
            return state.eval()

        alpha = kwargs['alpha']
        beta = kwargs['beta']

        if isMaxPlayer:
            value = float('-inf')
            for child in state.getChildren():
                value = max(value, self.__miniMaxAlphaBeta(
                    child, depth - 1, False, alpha=alpha, beta=beta))
                if value > beta:
                    break   # beta cut off
                alpha = max(alpha, value)
        else:
            value = float('inf')
            for child in state.getChildren():
                value = min(value, self.__miniMaxAlphaBeta(
                    child, depth - 1, True, alpha=alpha, beta=beta))
                if value < alpha:
                    break   # alpha cut off
                beta = min(beta, value)

        return value

    def __miniMaxABDynamic(self, state: GameState, depth: int,
                           isMaxPlayer: bool, **kwargs):
        if depth == 0 or state.isTerminal():
            return state.eval()

        alpha = kwargs['alpha']
        beta = kwargs['beta']

        if isMaxPlayer:
            value = float('-inf')
            for child in state.getChildren():
                if child.getMemoization(isMaxPlayer) in self.memo:
                    value = self.memo[child.getMemoization(isMaxPlayer)]
                else:
                    value = max(value, self.__miniMaxABDynamic(
                        child,
                        depth - 1,
                        not isMaxPlayer,
                        alpha=alpha,
                        beta=beta)
                    )
                    if value > beta:
                        break   # beta cut off
                    alpha = max(alpha, value)
                    self.memo[child.getMemoization(not isMaxPlayer)] = value
        else:
            value = float('inf')
            for child in state.getChildren():
                if child.getMemoization(not isMaxPlayer) in self.memo:
                    value = self.memo[child.getMemoization(not isMaxPlayer)]
                else:
                    value = min(value, self.__miniMaxABDynamic(
                        child,
                        depth - 1,
                        isMaxPlayer,
                        alpha=alpha,
                        beta=beta)
                    )
                    if value < alpha:
                        break   # alpha cut off
                    beta = min(beta, value)
                    self.memo[child.getMemoization(isMaxPlayer)] = value

        return value

    def getNextMove(self, state: GameState, depth,
                    mode: str = "dynamic"):
        self.setMinimax(mode)
        isMaxPlayer = self.__maxPlayer

        alpha = float('-inf')
        beta = float('inf')
        best_value = float('-inf') if isMaxPlayer else float('inf')
        best_child = None

        if mode == 'baseline':
            return self.minimaxMethod(state)

        for child in state.getChildren():
            value = self.minimaxMethod(state=child, depth=depth - 1,
                                       isMaxPlayer=not isMaxPlayer,
                                       alpha=alpha, beta=beta)

            if isMaxPlayer:
                if value > best_value:
                    best_value = value
                    best_child = child
            else:
                if value < best_value:
                    best_value = value
                    best_child = child

        return best_child
