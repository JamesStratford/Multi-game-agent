from __future__ import annotations
import customtkinter as ctk
from GameGUI import AIPlayingGUI
from Games import Nim
from GamePlayingAgent import Agent


class NimGUI(AIPlayingGUI):
    def __init__(self, gamestate: Nim = None, aiPlayerOne: Agent = None,
                 aiPlayerTwo: Agent = None):
        super().__init__(gamestate=gamestate, playerOne=aiPlayerOne,
                         playerTwo=aiPlayerTwo)
        self.play_area = ctk.CTkFrame(self.frame,
                                      width=self.windowWidth/2,
                                      height=self.windowHeight/2)
        self.piles: list[self.Pile] = []
        self.k = 3 if gamestate is None else gamestate.k
        self.playerOneMax = False

    class Pile:
        def __init__(self, x, gui: NimGUI):
            self.x = x
            buttonSz = (5 * 100) / gui.k
            self.button = ctk.CTkButton(gui.play_area,
                                        text="",
                                        width=gui.windowWidth/2,
                                        height=buttonSz,
                                        font=ctk.CTkFont(size=int(buttonSz/2)))
            self.button.grid(row=x, column=1, pady=2, padx=2)

        def set(self, sticks):
            self.button.configure(text=sticks)

    def display(self):
        for x, row in enumerate(self.gamestate.board):
            self.piles[x].set(' | ' * row)

    def start(self):
        for x in range(self.k):
            self.piles.append(self.Pile(x, self))
        self.play_area.pack(pady=10, padx=10)
        self.display()
        AIPlayingGUI.start(self)

    def reset(self):
        self.gamestate = Nim(move=self.startingPlayer.get(),
                             nDimensions=self.gamestate.k)
        self.display()
        self.statusText.configure(text="")
