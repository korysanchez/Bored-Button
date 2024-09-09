from tkinter import *

from Palette_Manager import PaletteManager
from GameApp import Game

class Game_Name(Game):

    def start(self):
        super().create(width=500, height=500, title='Game', resizable=False)
        #
        #   Main code
        #
        self.root.mainloop()

    def kill(self):
        super().kill()

    def update_colors(self):
        super().update_colors()



if __name__ == "__main__":
    palette_manager = PaletteManager()
    game = Game_Name(palette_manager)
    game.start()