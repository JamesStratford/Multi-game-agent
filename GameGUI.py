from __future__ import annotations
import customtkinter as ctk
from Games import GameState, TicTacToe
from GamePlayingAgent import Agent
import threading
import time


class AIPlayingGUI():
    def __init__(self, gamestate: GameState = None, aiPlayerOne: Agent = None,
                 aiPlayerTwo: Agent = None):
        self.gamestate = gamestate
        self.aiPlayerOne = aiPlayerOne
        self.aiPlayerTwo = aiPlayerTwo
        self.gameMutex = False
        self.loading = False
        self.slowTime = False
        self.__initGUI()

    def __initGUI(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.windowWidth = 800
        self.windowHeight = 800
        self.root = ctk.CTk()
        self.root.resizable(False, False)
        self.root.title("Game AI Player")
        self.root.geometry(f"{self.windowWidth}x{self.windowHeight}")
        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.buttonPanel = ctk.CTkFrame(master=self.root)
        self.buttonPanel.pack(pady=10, padx=60, fill="both", expand=True,
                              anchor='s')
        self.statusText = ctk.CTkLabel(master=self.buttonPanel,
                                       text="")
        self.statusText.pack(anchor='n')

        self.ai1Frame = ctk.CTkFrame(master=self.buttonPanel)

        self.ai1Label = ctk.CTkLabel(master=self.ai1Frame,
                                     text="AI Player 1")
        self.ai1Label.pack()
        options = ['Minimax', 'Alpha Beta Pruning', 'Dynamic']
        self.ai1MethodCombo = ctk.CTkComboBox(master=self.ai1Frame,
                                              values=options,
                                              width=200)
        self.ai1MethodCombo.pack()

        def setAIOneDepth(slider):
            self.aiPlayerOne.depth = int(slider)
            self.ai1DepthLabel.configure(text="Depth: = "
                                         f"{int(slider)}")

        self.ai1DepthSlider = ctk.CTkSlider(master=self.ai1Frame,
                                            from_=1,
                                            to=10,
                                            number_of_steps=9,
                                            command=setAIOneDepth)
        self.ai1DepthLabel = ctk.CTkLabel(master=self.ai1Frame,
                                          text="Depth: = "
                                          f"{int(self.ai1DepthSlider.get())}")
        self.ai1DepthSlider.pack()
        self.ai1DepthLabel.pack()

        self.ai1Frame.pack(pady=10, side='top', anchor='w')
        self.ai1Frame.pack(padx=10, side='left', anchor='w')

        self.ai2Frame = ctk.CTkFrame(master=self.buttonPanel)

        self.ai2Label = ctk.CTkLabel(master=self.ai2Frame,
                                     text="AI Player 2")
        self.ai2Label.pack()
        self.ai2MethodCombo = ctk.CTkComboBox(master=self.ai2Frame,
                                              values=options,
                                              width=200)
        self.ai2MethodCombo.pack()

        def setAITwoDepth(slider):
            self.aiPlayerTwo.depth = int(slider)
            self.ai2DepthLabel.configure(text="Depth: = "
                                         f"{int(slider)}")

        self.ai2DepthSlider = ctk.CTkSlider(master=self.ai2Frame,
                                            from_=1,
                                            to=10,
                                            number_of_steps=9,
                                            command=setAITwoDepth)
        self.ai2DepthLabel = ctk.CTkLabel(master=self.ai2Frame,
                                          text="Depth: = "
                                          f"{int(self.ai2DepthSlider.get())}")
        self.ai2DepthSlider.pack()
        self.ai2DepthLabel.pack()
        self.ai2Frame.pack(pady=10, side='top', anchor='e')
        self.ai2Frame.pack(padx=10, side='right', anchor='e')

        self.startButton = ctk.CTkButton(master=self.buttonPanel,
                                         text="Start!",
                                         width=80,
                                         height=80,
                                         command=self.play)
        self.startButton.pack(pady=5)

        self.resetButton = ctk.CTkButton(master=self.buttonPanel,
                                         text="Reset",
                                         width=80,
                                         command=self.reset)
        self.resetButton.pack(pady=5)

        def slowTime():
            self.slowTime = self.slowTimeCheckBox.get()
        self.slowTimeCheckBox = ctk.CTkCheckBox(master=self.buttonPanel,
                                                width=80,
                                                text="Slow Time",
                                                command=slowTime)
        self.slowTimeCheckBox.pack()

    def display(self):
        pass

    def play(self):
        pass

    def reset(self):
        pass

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.quit()


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

        self.startMove = ctk.StringVar(value="X")

        def changeStartingPlayer():
            if self.gameMutex is False:
                self.gamestate.move = self.startMove.get()

        self.startMoveAIOne = ctk.CTkRadioButton(master=self.ai1Frame,
                                                 variable=self.startMove,
                                                 value='X',
                                                 text="Starting",
                                                 command=changeStartingPlayer)
        self.startMoveAITwo = ctk.CTkRadioButton(master=self.ai2Frame,
                                                 variable=self.startMove,
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
            buttonSize = (5 * 100) / gui.k
            self.button = ctk.CTkButton(gui.play_area,
                                        text="",
                                        width=buttonSize,
                                        height=buttonSize,
                                        font=ctk.CTkFont(size=20))
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
        methods = ['minimax', 'alphabeta', 'dynamic']
        aiOneModeStr = self.ai1MethodCombo.get()
        if aiOneModeStr == 'Minimax':
            aiOneMode = methods[0]
        elif aiOneModeStr == 'Alpha Beta Pruning':
            aiOneMode = methods[1]
        else:
            aiOneMode = methods[2]

        aiTwoModeStr = self.ai2MethodCombo.get()
        if aiTwoModeStr == 'Minimax':
            aiTwoMode = methods[0]
        elif aiTwoModeStr == 'Alpha Beta Pruning':
            aiTwoMode = methods[1]
        else:
            aiTwoMode = methods[2]

        while not self.gamestate.isTerminal():
            if self.gamestate.move == 'X':   # AI 1
                self.gamestate.move = 'O'
                child = self.aiPlayerOne.bestMove(self.gamestate,
                                                  self.aiPlayerOne.depth,
                                                  True,
                                                  aiOneMode)
                self.gamestate.board = child.board
            else:                       # AI 2
                self.gamestate.move = 'X'
                child = self.aiPlayerTwo.bestMove(self.gamestate,
                                                  self.aiPlayerTwo.depth,
                                                  False,
                                                  aiTwoMode)
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
        self.gamestate = TicTacToe(move=self.startMove,
                                   nDimensions=self.gamestate.k)
        for row in self.XO_points:
            for xo_point in row:
                xo_point.button.configure(text="")
        self.statusText.configure(text="")


if __name__ == "__main__":
    gui = TicTacToeGUI(TicTacToe(move='X', nDimensions=3), Agent(), Agent())
    gui.start()
