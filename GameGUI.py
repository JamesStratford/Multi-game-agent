from __future__ import annotations
import customtkinter as ctk
from Games import GameState
from GamePlayingAgent import Player, Agent, Human
import threading
import time


class AIPlayingGUI():
    event = threading.Event()

    def __init__(self, gamestate: GameState = None, playerOne: Player = None,
                 playerTwo: Player = None):
        self.gamestate = gamestate
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.gameMutex = False

        self.loading = False
        self.slowTime = False
        self.playerOneMax = True
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

        self.playerOneFrame = ctk.CTkFrame(master=self.buttonPanel,
                                           width=200,
                                           height=200)

        self.playerOneLabel = ctk.CTkLabel(master=self.playerOneFrame,
                                           text="Player X",
                                           width=200)
        self.playerOneLabel.pack()
        options = ['Baseline', 'Minimax', 'Alpha Beta Pruning', 'Dynamic']
        if type(self.playerOne) == Agent:
            self.ai1SelectedMethod = ctk.StringVar(master=self.playerOneFrame,
                                                   value="Baseline")
            self.ai1MethodCombo = ctk.CTkComboBox(
                master=self.playerOneFrame,
                values=options,
                width=200,
                variable=self.ai1SelectedMethod,
                state="readonly")
            self.ai1MethodCombo.pack()

            def setAIOneDepth(slider):
                self.playerOne.depth = int(slider)
                self.ai1DepthLabel.configure(text="Depth: = "
                                             f"{int(slider)}")

            self.ai1DepthSlider = ctk.CTkSlider(
                master=self.playerOneFrame,
                from_=1,
                to=10,
                number_of_steps=9,
                command=setAIOneDepth)
            self.ai1DepthLabel = ctk.CTkLabel(
                master=self.playerOneFrame,
                text="Depth: = "
                f"{int(self.ai1DepthSlider.get())}")
            self.ai1DepthSlider.pack()
            self.ai1DepthLabel.pack()

        self.playerOneFrame.pack(pady=10, side='top', anchor='w')
        self.playerOneFrame.pack(padx=10, side='left', anchor='w')

        self.playerTwoFrame = ctk.CTkFrame(master=self.buttonPanel,
                                           width=200,
                                           height=200)

        self.playerTwoLabel = ctk.CTkLabel(master=self.playerTwoFrame,
                                           text="Player O",
                                           width=200)
        self.playerTwoLabel.pack()

        if type(self.playerTwo) == Agent:
            self.ai2SelectedMethod = ctk.StringVar(
                master=self.playerTwoFrame,
                value="Baseline")
            self.ai2MethodCombo = ctk.CTkComboBox(
                master=self.playerTwoFrame,
                values=options,
                width=200,
                variable=self.ai2SelectedMethod,
                state="readonly")
            self.ai2MethodCombo.pack()

            def setAITwoDepth(slider):
                self.playerTwo.depth = int(slider)
                self.ai2DepthLabel.configure(text="Depth: = "
                                             f"{int(slider)}")

            self.ai2DepthSlider = ctk.CTkSlider(
                master=self.playerTwoFrame,
                from_=1,
                to=10,
                number_of_steps=9,
                command=setAITwoDepth)
            self.ai2DepthLabel = ctk.CTkLabel(
                master=self.playerTwoFrame,
                text="Depth: = "
                f"{int(self.ai2DepthSlider.get())}")
            self.ai2DepthSlider.pack()
            self.ai2DepthLabel.pack()

        self.playerTwoFrame.pack(pady=10, side='top', anchor='e')
        self.playerTwoFrame.pack(padx=10, side='right', anchor='e')

        self.startingPlayer = ctk.StringVar(value='X')

        # Human player augmentation Hook
        self._humanPlayerOptionsGUIHook()

        def changeStartingPlayer():
            if self.gameMutex is False:
                self.gamestate.move = self.startingPlayer.get()

        self.startMoveAIOne = ctk.CTkRadioButton(
            master=self.playerOneFrame,
            variable=self.startingPlayer,
            value='X',
            text="Starting",
            command=changeStartingPlayer)
        self.startMoveAITwo = ctk.CTkRadioButton(
            master=self.playerTwoFrame,
            variable=self.startingPlayer,
            value='O',
            text="Starting",
            command=changeStartingPlayer)
        self.startMoveAIOne.pack()
        self.startMoveAITwo.pack()

        self.startButton = ctk.CTkButton(
            master=self.buttonPanel,
            text="Start!",
            width=80,
            height=80,
            command=self.play)
        self.startButton.pack(pady=5)

        self.resetButton = ctk.CTkButton(
            master=self.buttonPanel,
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

    def hasHumanPlayer(self):
        return type(self.playerOne) == Human or type(self.playerTwo) == Human

    def display(self):
        pass

    def _humanPlayerOptionsGUIHook(self):
        pass

    def _play(self):
        self.gameMutex = True

        def getMode():
            methods = ['baseline', 'minimax', 'alphabeta', 'dynamic']
            aiOneMode = None

            if type(self.playerOne) == Agent:
                aiOneModeStr = self.ai1SelectedMethod.get()
                if aiOneModeStr == 'Baseline':
                    aiOneMode = methods[0]
                elif aiOneModeStr == 'Minimax':
                    aiOneMode = methods[1]
                elif aiOneModeStr == 'Alpha Beta Pruning':
                    aiOneMode = methods[2]
                else:
                    aiOneMode = methods[3]

            aiTwoMode = None
            if type(self.playerTwo) == Agent:
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

        def playersTurn(player: str):
            def threadResult(result: dict, player: str):
                """
                Acquire move via threading to prevent lagging GUI.
                Unfortunately Python doesn't have true threading so
                it still lags. But at least the GUI is responsive
                """
                # This was the weirdest bit of code I have written
                result['result'] = \
                    self.playerOne.getNextMove(
                        state=self.gamestate,
                        depth=self.playerOne.depth,
                        mode=getMode()[0]
                ) if player == "X" else \
                    self.playerTwo.getNextMove(
                        state=self.gamestate,
                        depth=self.playerTwo.depth,
                        mode=getMode()[1]
                )

            result = {'result': self.gamestate}

            child = self.gamestate

            if self.gamestate.isTerminal():
                return self.gamestate

            if player == "X" and type(self.playerOne) == Agent:
                self.gamestate.move = 'O'

                t = threading.Thread(
                    target=threadResult,
                    args=[result, player]
                )
                t.start()
                t.join()
                AIPlayingGUI.event.clear()

                child = result['result']
            elif player == "O" and type(self.playerTwo) == Agent:
                self.gamestate.move = 'X'

                t = threading.Thread(
                    target=threadResult,
                    args=[result, player]
                )
                t.start()
                t.join()
                AIPlayingGUI.event.clear()

                child = result['result']
            elif type(self.playerOne) == Human or \
                    type(self.playerTwo) == Human:
                # Human player handler. Refer to descendant game GUI class
                # for way to handle
                if player == "X":
                    self.playerOne.turn = True
                elif player == "O":
                    self.playerTwo.turn = True
                # time.sleep(0.5)

            return child

        while not self.gamestate.isTerminal():
            if self.slowTime or self.hasHumanPlayer():
                if self.gamestate.move == 'X':
                    self.statusText.configure(text="Loading...\nPlayer X turn")
                else:
                    self.statusText.configure(text="Loading...\nPlayer O turn")

            if self.gamestate.move == 'X':      # AI 1
                if type(self.playerOne) == Human:
                    AIPlayingGUI.event.set()
                    child = playersTurn("X")
                    AIPlayingGUI.event.wait()
                else:
                    child = playersTurn("X")
                self.gamestate.board = child.board
            else:                               # AI 2
                if type(self.playerTwo) == Human:
                    AIPlayingGUI.event.set()
                    child = playersTurn("O")
                    AIPlayingGUI.event.wait()
                else:
                    child = playersTurn("O")
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
            t = threading.Thread(target=self._play)
            t.daemon = True
            t.start()
            self.loading = True
            self.statusText.configure(text="Loading...")

    def reset(self):
        pass

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.quit()
