from __future__ import annotations
import customtkinter as ctk
from GameGUI import AIPlayingGUI
from Games import Nim
from GamePlayingAgent import Player, Human


class NimGUI(AIPlayingGUI):
    def __init__(self, gamestate: Nim = None, aiPlayerOne: Player = None,
                 aiPlayerTwo: Player = None):
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

            def tileClicked():
                """Human player handler"""

                move = "X" if gui.gamestate.move == "X" else "O"
                if gui.gamestate.board[self.x] > 0:
                    if move == "X" and type(gui.playerOne) == Human:
                        if int(gui.playerOneNumToRemove.get()) > 0:
                            gui.playerOne.turn = False
                            gui.gamestate.move = "O"
                            newBoard = gui.gamestate.board.copy()
                            newBoard[self.x] = max(
                                newBoard[self.x]
                                - int(gui.playerOneNumToRemove.get()), 0
                            )
                            gui.gamestate.board = newBoard
                    elif move == "O" and type(gui.playerTwo) == Human:
                        if int(gui.playerTwoNumToRemove.get()) > 0:
                            gui.playerTwo.turn = False
                            gui.gamestate.move = "X"
                            newBoard = gui.gamestate.board.copy()
                            newBoard[self.x] = max(
                                newBoard[self.x]
                                - int(gui.playerTwoNumToRemove.get()), 0
                            )
                            gui.gamestate.board = newBoard

            self.button = ctk.CTkButton(gui.play_area,
                                        text="",
                                        width=gui.windowWidth/2,
                                        height=buttonSz,
                                        font=ctk.CTkFont(size=int(buttonSz/2)),
                                        command=tileClicked)
            self.button.grid(row=x, column=1, pady=2, padx=2)

        def set(self, sticks):
            self.button.configure(text=sticks)

    def display(self):
        for x, row in enumerate(self.gamestate.board):
            self.piles[x].set(' | ' * row)

    def _humanPlayerOptionsGUIHook(self):
        """
        Solution source:
        https://stackoverflow.com/questions/8959815/
        restricting-the-value-in-tkinter-entry-widget
        """
        def callback(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        vcmd = (self.playerOneFrame.register(callback))

        if type(self.playerOne) == Human:
            self.playerOneNumToRemove = ctk.StringVar(
                master=self.playerOneFrame,
                value="1")
            ctk.CTkLabel(master=self.playerOneFrame,
                         text="Number of sticks to remove:") \
                .pack()
            ctk.CTkEntry(master=self.playerOneFrame,
                         textvariable=self.playerOneNumToRemove,
                         validate='all',
                         validatecommand=(vcmd, '%P')) \
                .pack()
        if type(self.playerTwo) == Human:
            self.playerTwoNumToRemove = ctk.StringVar(
                master=self.playerTwoFrame,
                value="1")
            ctk.CTkLabel(master=self.playerTwoFrame,
                         text="Number of sticks to remove:") \
                .pack()
            ctk.CTkEntry(master=self.playerTwoFrame,
                         textvariable=self.playerTwoNumToRemove,
                         validate='all',
                         validatecommand=(vcmd, '%P')) \
                .pack()

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
