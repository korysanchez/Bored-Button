from tkinter import *
import random
from Palette_Manager import PaletteManager
from GameApp import Game


#   TO DO:
#       Add reset function
#


class Color_Fill(Game):

    def start(self):
        self.tile_size = 80
        self.tile_count_x = random.randint(5, 12)
        self.tile_count_y = random.randint(5, 8)
        self.tiles = []
        self.active_tiles = []
        self.moves = 0
        self.colors = self.palette.palette

        super().create(width=self.tile_count_x * self.tile_size, height=self.tile_count_y * self.tile_size, title='Color Fill')
        self.inset = 10
        self.tl_canvas = super().create_toplevel(width=len(self.colors) * self.tile_size - (len(self.colors) - 1) * self.inset, height=self.tile_size, pos_x=200, pos_y=700, title='Colors')
        self.create_board()

        self.root.mainloop()

    def create_board(self):
        for y in range(0, self.tile_count_y):
            for x in range(0, self.tile_count_x):
                color = random.choice(self.colors)
                tile = self.canvas.create_rectangle(x * self.tile_size, y * self.tile_size, x * self.tile_size + self.tile_size, y * self.tile_size + self.tile_size, fill = color, outline = color)
                self.tiles.append(tile)
        self.active_tiles.append(self.tiles[0])
        self.change_color(None, self.canvas.itemcget(self.tiles[0], 'fill'))

        for i in range(len(self.colors)):
            button = self.tl_canvas.create_rectangle(i * self.tile_size + self.inset - self.inset * i, self.inset, i * self.tile_size + self.tile_size - self.inset - self.inset * i, self.tile_size - self.inset,  fill = self.colors[i], outline = '')
            #button = self.tl_canvas.create_rectangle(self.inset, i * self.tile_size + self.inset - self.inset * i, self.tile_size - self.inset, i * self.tile_size + self.tile_size - self.inset - self.inset * i,  fill = self.colors[i], outline = '')
            self.tl_canvas.tag_bind(button, "<Button-1>", lambda event, color = self.colors[i] : self.change_color(event, color))
            

    def check_board(self):
        if len(self.tiles) == len(self.active_tiles):
            self.canvas.create_rectangle(int(self.tile_count_x * self.tile_size / 2 + self.tile_size / 4 - 200), int(self.tile_count_y * self.tile_size / 2 - self.tile_size / 4 - 50), int(self.tile_count_x * self.tile_size / 2 + self.tile_size / 4 + 200), int(self.tile_count_y * self.tile_size / 2 + self.tile_size / 4 + 50), fill = self.palette.secondary)
            self.canvas.create_text(int(self.tile_count_x * self.tile_size / 2 + self.tile_size / 4), int(self.tile_count_y * self.tile_size / 2 + self.tile_size / 4 - 50), font = ("Consolas", 50), fill = self.palette.primary, text = "You won in ")
            self.canvas.create_text(int(self.tile_count_x * self.tile_size / 2 + self.tile_size / 4), int(self.tile_count_y * self.tile_size / 2 + self.tile_size / 4), font = ("Consolas", 50), fill = self.palette.primary, text = str(self.moves) + " moves!")

    def change_color(self, event, color):
        self.moves += 1
        added = False
        for activeTile in self.active_tiles:
            if color != 'white':
                self.canvas.itemconfig(activeTile, fill = color, outline = 'white', width = 2)
            else:
                self.canvas.itemconfig(activeTile, fill = color, outline = 'black', width = 2)
            #left
            if (activeTile - 1) % self.tile_count_x != 0 and activeTile - 1 not in self.active_tiles and self.canvas.itemcget(activeTile - 1, 'fill') == color:
                self.active_tiles.append(activeTile - 1)
                added = True
            #right
            if (activeTile) % self.tile_count_x != 0 and activeTile + 1 not in self.active_tiles and self.canvas.itemcget(activeTile + 1, 'fill') == color:
                self.active_tiles.append(activeTile + 1)
                added = True
            #up
            if activeTile - self.tile_count_x > 0 and activeTile - self.tile_count_x not in self.active_tiles and self.canvas.itemcget(activeTile - self.tile_count_x, 'fill') == color:
                self.active_tiles.append(activeTile - self.tile_count_x)
                added = True
            #down
            if activeTile + self.tile_count_x <= self.tile_count_y * self.tile_count_x and activeTile + self.tile_count_x not in self.active_tiles and self.canvas.itemcget(activeTile + self.tile_count_x, 'fill') == color:
                self.active_tiles.append(activeTile + self.tile_count_x)
                added = True
            
            if added:
                self.moves -= 1
                self.change_color(None, color)
        self.check_board()
    



if __name__ == "__main__":
    palette_manager = PaletteManager(2)
    game = Color_Fill(palette_manager)
    game.start()