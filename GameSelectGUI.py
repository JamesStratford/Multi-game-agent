from __future__ import annotations
import customtkinter as ctk
from GamePlayingAgent import Agent, Human
from TicTacToeGUI import TicTacToeGUI
from NimGUI import NimGUI
from TigerAndDogsGUI import TigerAndDogsGUI
from Games import TicTacToe, Nim, TigerAndDogs
from multiprocessing import Pool


class GameSelectGUI():
    def __init__(self):
        self.processPool = Pool(processes=4)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.windowWidth = 800
        self.windowHeight = 400
        self.root = ctk.CTk()
        self.root.resizable(False, False)
        self.root.title("Select a Game")
        self.root.geometry(f"{self.windowWidth}x{self.windowHeight}")
        self.root.wm_iconbitmap("resources/favicon.ico")
        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.titleLabel = ctk.CTkLabel(master=self.frame,
                                       font=ctk.CTkFont(size=50),
                                       text="Select Game")
        self.titleLabel.pack()
        self.gameOptions = self.GameOptions(self.frame)

        def startGame():

            if self.gameOptions.playerOneValue.get() == "AI":
                playerOneAI = Agent(maxPlayer=True)
            else:
                playerOneAI = Human()

            if self.gameOptions.playerTwoValue.get() == "AI":
                playerTwoAI = Agent(maxPlayer=False)
            else:
                playerTwoAI = Human()

            if self.gameOptions.selectedGame.get() == 'TicTacToe':
                self.game = TicTacToe(
                    move='X',
                    nDimensions=self.gameOptions
                    .opt1Value.get())
                self.gameGUI = TicTacToeGUI(
                    self.game, playerOneAI, playerTwoAI)
            elif self.gameOptions.selectedGame.get() == 'Nim':
                self.game = Nim(
                    move='X',
                    nDimensions=self.gameOptions
                    .opt1Value.get())
                self.gameGUI = NimGUI(self.game, playerOneAI, playerTwoAI)
            elif self.gameOptions.selectedGame.get() == 'Tiger and Dogs':
                self.game = TigerAndDogs(
                    move='X',
                    nDimensions=self.gameOptions
                    .opt1Value.get())
                self.gameGUI = TigerAndDogsGUI(
                    self.game, playerOneAI, playerTwoAI)
            elif self.gameOptions.selectedGame.get() == 'X':
                pass

            # self.stop()
            self.processPool.apply_async(self.gameGUI.start())

        self.startButton = ctk.CTkButton(master=self.frame,
                                         height=100,
                                         width=100,
                                         text="Start",
                                         font=ctk.CTkFont(size=20),
                                         command=startGame)
        self.startButton.pack(pady=20, anchor="s")

    class GameOptions():
        def __init__(self, master):
            self.frame = ctk.CTkFrame(master=master,
                                      width=300,
                                      height=300)
            self.frame.pack()
            self.selectedGame = ctk.StringVar(master=self.frame,
                                              value='TicTacToe')
            games = ['TicTacToe', 'Nim', 'Tiger and Dogs', 'X']

            self.gameComboBox = ctk.CTkComboBox(master=self.frame,
                                                values=games,
                                                variable=self.selectedGame,
                                                command=self.updateOptions,
                                                state="readonly")
            self.opt1Value = ctk.IntVar(master=self.frame,
                                        value=3)
            self.opt1Label = ctk.CTkLabel(master=self.frame,
                                          text="Game Size: "
                                          f"{self.opt1Value.get()}")
            self.opt1 = ctk.CTkSlider(master=self.frame,
                                      from_=3,
                                      to=10,
                                      number_of_steps=7,
                                      variable=self.opt1Value,
                                      command=self.updateOptions)
            self.gameComboBox.pack()
            self.opt1Label.pack()
            self.opt1.pack()

            self.playerOptFrame = ctk.CTkFrame(master=self.frame)
            playerOptions = ["AI", "Human"]
            self.playerOneValue = ctk.StringVar(master=self.frame,
                                                value="AI")
            self.playerOneCombo = ctk.CTkComboBox(master=self.playerOptFrame,
                                                  values=playerOptions,
                                                  variable=self.playerOneValue,
                                                  width=100)
            self.playerTwoValue = ctk.StringVar(master=self.frame,
                                                value="AI")
            self.playerTwoCombo = ctk.CTkComboBox(master=self.playerOptFrame,
                                                  values=playerOptions,
                                                  variable=self.playerTwoValue,
                                                  width=100)
            self.playerOptFrame.pack()
            self.playerOneCombo.grid(row=0, column=0, padx=2, pady=2)
            self.playerTwoCombo.grid(row=0, column=1, padx=2, pady=2)

        def updateOptions(self, text):
            self.opt1Label.configure(text="Game Size: "
                                     f"{self.opt1Value.get()}")

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.quit()
