from __future__ import annotations

import customtkinter as ctk
from GameGUI import AIPlayingGUI
from Games import TigerAndDogs
from GamePlayingAgent import Player, Human


class TigerAndDogsGUI(AIPlayingGUI):
    """
    Code modified from this resource:
    https://devdojo.com/jothin-kumar/tic-tac-toe-with-python-tkinter-part-1
    """

    def __init__(self, gamestate: TigerAndDogs = None,
                 playerOne: Player = None,
                 playerTwo: Player = None
                 ):
        super().__init__(gamestate=gamestate, playerOne=playerOne,
                         playerTwo=playerTwo)
        self.play_area = ctk.CTkFrame(self.frame, width=self.windowWidth/2,
                                      height=self.windowHeight/2)
        self.tiles: list[list[self.Tile]] = []
        self.k = 3 if gamestate is None else gamestate.k
        self.highlightedTile = None
        self.availMoves = None

    class Tile:
        def __init__(self, x, y, gui: TigerAndDogsGUI):
            self.x = x
            self.y = y
            buttonSz = (5 * 100) / gui.k
            self.highlighted = False
            self.disableHighlight = False
            self.availableMove = False

            def tileClicked():
                """Human player handler"""
                if type(gui.playerOne) != Human and \
                        type(gui.playerTwo) != Human:
                    return
                
                if gui.gamestate.isTerminal():
                    return

                def startMove():
                    gui.highlightedTile = self
                    self.highlighted = True
                    gui.display()

                    gui.availMoves = gui.gamestate.getAvailableMoves(
                        gui.gamestate.board,
                        self.x,
                        self.y
                    )
                    for moves in gui.availMoves:
                        gui.tiles[moves[0]][moves[1]].availableMove = True

                def cancelMove():
                    gui.highlightedTile = None
                    self.highlighted = False
                    self.disableHighlight = True
                    gui.display()

                    gui.availMoves = gui.gamestate.getAvailableMoves(
                        gui.gamestate.board,
                        self.x,
                        self.y
                    )
                    for moves in gui.availMoves:
                        gui.tiles[moves[0]][moves[1]].availableMove = False

                def executeMove(player: str):
                    if (self.x, self.y,) in gui.availMoves:
                        x = gui.highlightedTile.x
                        y = gui.highlightedTile.y
                        gui.highlightedTile.highlighted = False
                        gui.highlightedTile.disableHighlight = True
                        gui.highlightedTile = None

                        gui.display()
                        newBoard = gui.gamestate.board.copy()
                        newBoard[x][y] = " "
                        newBoard[self.x][self.y] = player
                        newBoard = gui.gamestate.board.copy()
                        gui.gamestate.tigerKillDogs(newBoard, (self.x, self.y))
                        gui.gamestate.board = newBoard
                        if player == "X":
                            gui.playerOne.turn = False
                        else:
                            gui.playerTwo.turn = False
                        gui.gamestate.move = "X" if player == "O" else "O"
                    AIPlayingGUI.event.clear()

                move = "X" if gui.gamestate.move == "X" else "O"
                if move == "X" and type(gui.playerOne) == Human:
                    if gui.highlightedTile is None and \
                            gui.gamestate.board[self.x][self.y] == "X":
                        startMove()
                    elif gui.highlightedTile is not None and \
                            gui.highlightedTile == self:
                        cancelMove()
                    elif gui.highlightedTile is not None and \
                            gui.gamestate.board[self.x][self.y] == " ":
                        executeMove("X")
                elif move == "O" and type(gui.playerTwo) == Human:
                    if gui.highlightedTile is None and \
                            gui.gamestate.board[self.x][self.y] == "O":
                        startMove()
                    elif gui.highlightedTile is not None and \
                            gui.highlightedTile == self:
                        cancelMove()
                    elif gui.highlightedTile is not None and \
                            gui.gamestate.board[self.x][self.y] == " ":
                        executeMove("O")

            self.button = ctk.CTkButton(
                gui.play_area,
                text="",
                width=buttonSz,
                height=buttonSz,
                font=ctk.CTkFont(size=int(buttonSz/2)),
                command=tileClicked
            )

            self.button.grid(row=x, column=y, pady=2, padx=2)

        def set(self, char):
            self.button.configure(text=char)

    def display(self):
        for x, row in enumerate(self.gamestate.board):
            for y, col in enumerate(row):
                if self.tiles[x][y].highlighted:
                    self.tiles[x][y].button.configure(
                        fg_color=("black", "azure")
                    )
                if self.tiles[x][y].disableHighlight:
                    self.tiles[x][y].button.configure(
                        fg_color=('#3a7ebf', '#1f538d')
                    )
                    self.tiles[x][y].disableHighlight = False
                self.tiles[x][y].set(col)

    def start(self):
        for x in range(self.k):
            xo_row = []
            for y in range(self.k):
                xo_row.append(self.Tile(x, y, self))
            self.tiles.append(xo_row)
        self.play_area.pack(pady=10, padx=10)
        AIPlayingGUI.start(self)

    def reset(self):
        self.gamestate.endGame()
        self.display()
        self.gamestate = TigerAndDogs(move=self.startingPlayer.get(),
                                      nDimensions=self.gamestate.k)
        self.display()
        # for row in self.tiles:
        #     for tile in row:
        #         tile.button.configure(text="")
        # self.statusText.configure(text="")
