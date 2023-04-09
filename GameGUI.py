from __future__ import annotations
import customtkinter as ctk
from Games import GameState
from GamePlayingAgent import Agent


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
        options = ['Baseline', 'Minimax', 'Alpha Beta Pruning', 'Dynamic']
        self.ai1SelectedMethod = ctk.StringVar(master=self.ai1Frame,
                                               value="Baseline")
        self.ai1MethodCombo = ctk.CTkComboBox(master=self.ai1Frame,
                                              values=options,
                                              width=200,
                                              variable=self.ai1SelectedMethod,
                                              state="readonly")
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
        self.ai2SelectedMethod = ctk.StringVar(master=self.ai2Frame,
                                               value="Baseline")
        self.ai2MethodCombo = ctk.CTkComboBox(master=self.ai2Frame,
                                              values=options,
                                              width=200,
                                              variable=self.ai2SelectedMethod,
                                              state="readonly")
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

