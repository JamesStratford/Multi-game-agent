from __future__ import annotations

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

    class XOPoint:
        def __init__(self, x, y, gui: TicTacToeGUI):
            self.x = x
            self.y = y
            buttonSz = (5 * 100) / gui.k
            self.button = ctk.CTkButton(gui.play_area,
                                        text="",
                                        width=buttonSz,
                                        height=buttonSz,
                                        font=ctk.CTkFont(size=int(buttonSz/2)))
            self.button.grid(row=x, column=y, pady=2, padx=2)

        def set(self, char):
            self.button.configure(text=char)

    def display(self):
        for x, row in enumerate(self.gamestate.board):
            for y, col in enumerate(row):
                self.XO_points[x][y].set(col)

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
