from __future__ import annotations
import threading
import time
import customtkinter as ctk
from GameGUI import AIPlayingGUI
from Games import TicTacToe
from GamePlayingAgent import Agent


class TicTacToeGUI(AIPlayingGUI):
    """
    Code modified from this resource:
    https://devdojo.com/jothin-kumar/tic-tac-toe-with-python-tkinter-part-1
    """

    def __init__(self, gamestate: TicTacToe = None, aiPlayerOne: Agent = None,
                 aiPlayerTwo: Agent = None):
        super().__init__(gamestate=gamestate, aiPlayerOne=aiPlayerOne,
                         aiPlayerTwo=aiPlayerTwo)
        self.play_area = ctk.CTkFrame(self.frame, width=self.windowWidth/2,
                                      height=self.windowHeight/2)
        self.XO_points: list[list[self.XOPoint]] = []
        self.k = 3 if gamestate is None else gamestate.k
        self.ai1Label.configure(text="Player X")
        self.ai2Label.configure(text="Player O")

        self.startingPlayer = ctk.StringVar(value='X')
        self.__initGUI()

    def __initGUI(self):
        def changeStartingPlayer():
            if self.gameMutex is False:
                self.gamestate.move = self.startingPlayer.get()

        self.startMoveAIOne = ctk.CTkRadioButton(master=self.ai1Frame,
                                                 variable=self.startingPlayer,
                                                 value='X',
                                                 text="Starting",
                                                 command=changeStartingPlayer)
        self.startMoveAITwo = ctk.CTkRadioButton(master=self.ai2Frame,
                                                 variable=self.startingPlayer,
                                                 value='O',
                                                 text="Starting",
                                                 command=changeStartingPlayer)
        self.startMoveAIOne.pack()
        self.startMoveAITwo.pack()

    class XOPoint:
        def __init__(self, x, y, gui: TicTacToeGUI):
            self.x = x
            self.y = y
            self.value = None
            buttonSz = (5 * 100) / gui.k
            self.button = ctk.CTkButton(gui.play_area,
                                        text="",
                                        width=buttonSz,
                                        height=buttonSz,
                                        font=ctk.CTkFont(size=int(buttonSz/2)))
            self.button.grid(row=x, column=y, pady=2, padx=2)

        def set(self, char):
            self.button.configure(text=char)

        def reset(self):
            self.button.configure(text="")
            self.value = None

    def display(self):
        for x, row in enumerate(self.gamestate.board):
            for y, col in enumerate(row):
                self.XO_points[x][y].set(col)

    def __play(self):
        self.gameMutex = True

        def getMode():
            methods = ['baseline', 'minimax', 'alphabeta', 'dynamic']

            aiOneModeStr = self.ai1SelectedMethod.get()
            if aiOneModeStr == 'Baseline':
                aiOneMode = methods[0]
            elif aiOneModeStr == 'Minimax':
                aiOneMode = methods[1]
            elif aiOneModeStr == 'Alpha Beta Pruning':
                aiOneMode = methods[2]
            else:
                aiOneMode = methods[3]

            aiTwoModeStr = self.ai2SelectedMethod.get()
            if aiTwoModeStr == 'Baseline':
                aiTwoMode = methods[0]
            elif aiTwoModeStr == 'Minimax':
                aiTwoMode = methods[1]
            elif aiTwoModeStr == 'Alpha Beta Pruning':
                aiTwoMode = methods[2]
            else:
                aiTwoMode = methods[3]

            return (aiOneMode, aiTwoMode,)

        while not self.gamestate.isTerminal():
            if self.gamestate.move == 'X':      # AI 1
                self.gamestate.move = 'O'
                child = self.aiPlayerOne.bestMove(self.gamestate,
                                                  self.aiPlayerOne.depth,
                                                  True,
                                                  getMode()[0])
                self.gamestate.board = child.board
            else:                               # AI 2
                self.gamestate.move = 'X'
                child = self.aiPlayerTwo.bestMove(self.gamestate,
                                                  self.aiPlayerTwo.depth,
                                                  False,
                                                  getMode()[1])
                self.gamestate.board = child.board
            self.display()
            if self.slowTime:
                time.sleep(1)

        self.display()
        self.gameMutex = False
        winner = self.gamestate.getWinner()
        text = "Tie!"
        if winner is not None:
            text = f"{winner} has won!"
        self.statusText.configure(text=text)

    def play(self):
        if self.gameMutex is False:
            t = threading.Thread(target=self.__play)
            t.daemon = True
            t.start()
            self.loading = True
            self.statusText.configure(text="Loading...")

    def start(self):
        for x in range(self.k):
            xo_row = []
            for y in range(self.k):
                xo_row.append(self.XOPoint(x, y, self))
            self.XO_points.append(xo_row)
        self.play_area.pack(pady=10, padx=10)
        AIPlayingGUI.start(self)

    def reset(self):
        self.gamestate = TicTacToe(move=self.startingPlayer.get(),
                                   nDimensions=self.gamestate.k)
        for row in self.XO_points:
            for xo_point in row:
                xo_point.button.configure(text="")
        self.statusText.configure(text="")
