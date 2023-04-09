from Games import GameState


class Agent():
    def __init__(self, depth=5):
        self.memo = {}
        self.minimaxMethod = None
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

    def __baseline(self, state: GameState, **kwargs):
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

        # Memoization
        if state.getMemoization() in self.memo.keys():
            return self.memo[state.getMemoization()]

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
                self.memo[state.getMemoization()] = value
        else:
            value = float('inf')
            for child in state.getChildren():
                value = min(value, self.__miniMaxAlphaBeta(
                    child, depth - 1, True, alpha=alpha, beta=beta))
                if value < alpha:
                    break   # alpha cut off
                beta = min(beta, value)
                self.memo[state.getMemoization()] = value

        return value

    def bestMove(self, state: GameState, depth, isMaxPlayer,
                 mode: str = "dynamic"):
        self.setMinimax(mode)

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
                if value >= best_value:
                    best_value = value
                    best_child = child
            else:
                if value < best_value:
                    best_value = value
                    best_child = child

        return best_child
