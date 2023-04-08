from __future__ import annotations
import customtkinter as ctk
from Games import GameState, TicTacToe
from GamePlayingAgent import Agent
import threading


class AIPlayingGUI():
    def __init__(self, gamestate: GameState = None, aiPlayerOne: Agent = None,
                 aiPlayerTwo: Agent = None):
        self.gamestate = gamestate
        self.aiPlayerOne = aiPlayerOne
        self.aiPlayerTwo = aiPlayerTwo
        self.gameMutex = False
        self.loading = False

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

        self.ai1Frame = ctk.CTkFrame(master=self.buttonPanel)
        self.ai1Frame.pack(pady=10, side='top', anchor='w')
        self.ai1Frame.pack(padx=10, side='left', anchor='w')

        self.ai1Label = ctk.CTkLabel(master=self.ai1Frame,
                                     text="AI Player 1")
        self.ai1Label.pack()
        options = ['Minimax', 'Alpha Beta Pruning', 'Dynamic']
        self.ai1MethodCombo = ctk.CTkComboBox(master=self.ai1Frame,
                                              values=options,
                                              width=200)
        self.ai1MethodCombo.pack()

        self.ai2Frame = ctk.CTkFrame(master=self.buttonPanel)
        self.ai2Frame.pack(pady=10, side='top', anchor='e')
        self.ai2Frame.pack(padx=10, side='right', anchor='e')
        self.ai2Label = ctk.CTkLabel(master=self.ai2Frame,
                                     text="AI Player 2")
        self.ai2Label.pack()
        options = ['Minimax', 'Alpha Beta Pruning', 'Dynamic']
        self.ai2MethodCombo = ctk.CTkComboBox(master=self.ai2Frame,
                                              values=options,
                                              width=200)
        self.ai2MethodCombo.pack()

        self.startButton = ctk.CTkButton(master=self.buttonPanel,
                                         text="Start!",
                                         width=100,
                                         height=100,
                                         command=self.play)
        self.startButton.pack(pady=10)

        self.resetButton = ctk.CTkButton(master=self.buttonPanel,
                                         text="Reset",
                                         width=100,
                                         command=self.reset)
        self.resetButton.pack(pady=10)

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
        self.currentChr = 'X'
        self.k = 3 if gamestate is None else gamestate.k

    class XOPoint:
        def __init__(self, x, y, gui: TicTacToeGUI):
            self.x = x
            self.y = y
            self.value = None
            buttonSize = (5 * 100) / gui.k
            self.button = ctk.CTkButton(gui.play_area,
                                        text="",
                                        width=buttonSize,
                                        height=buttonSize)
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
        while not self.gamestate.isTerminal():
            if self.gamestate.move == 'X':   # AI 1
                self.display()
                self.gamestate.move = 'O'
                child = self.aiPlayerOne.bestMove(self.gamestate, 2, True,
                                                  'dynamic')
                self.gamestate.board = child.board
            else:                       # AI 2
                self.display()
                self.gamestate.move = 'X'
                child = self.aiPlayerTwo.bestMove(self.gamestate, 5, False,
                                                  'dynamic')
                self.gamestate.board = child.board

        self.display()
        self.gameMutex = False

    def play(self):
        if self.gameMutex is False:
            t = threading.Thread(target=self.__play)
            t.daemon = True
            self.loading = True
            t.start()

    def start(self):
        for x in range(self.k):
            xo_row = []
            for y in range(self.k):
                xo_row.append(self.XOPoint(x, y, self))
            self.XO_points.append(xo_row)
        self.play_area.pack(pady=10, padx=10)
        AIPlayingGUI.start(self)

    def reset(self):
        self.gamestate = TicTacToe(nDimensions=self.gamestate.k)
        for row in self.XO_points:
            for xo_point in row:
                xo_point.button.configure(text="")


if __name__ == "__main__":
    gui = TicTacToeGUI(TicTacToe(nDimensions=4), Agent(), Agent())
    gui.start()
