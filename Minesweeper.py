from tkinter import *
import random, time, os
from Palette_Manager import PaletteManager
from GameApp import Game


#   TO DO:
#       Calculate mines AFTER the first click to avoid instant losses
#


class Minesweeper(Game):

    def start(self):
        self.tile_size = 40
        self.tile_count_x, self.tile_count_y, = random.randint(14,26), random.randint(8,20)
        self.mine_count = int(self.tile_count_x * self.tile_count_y / random.randint(4, 5))
        super().create(width=self.tile_size * self.tile_count_x + 1, height=self.tile_size * self.tile_count_y + 1, title='Minesweeper', resizable=True)
        self.create_board()
        self.root.mainloop()

    def create_board(self):
        self.texts, self.covers = [], []
        for y in range(self.tile_count_y):
            for x in range(self.tile_count_x):
                text = self.canvas.create_text(x*self.tile_size + self.tile_size/2, y*self.tile_size + self.tile_size/2, text='0', fill=self.palette.primary, font = ("consolas", self.tile_size), tags=('text', self.TAG_PRIM))
                self.texts.append(text)
        self.mines = random.choices(self.texts, k = self.mine_count)
        for i in self.mines:
            self.canvas.itemconfig(i, tags = ('mine'))
            self.canvas.itemconfig(i, text='9')
        for i in range(self.texts[0], len(self.texts) + self.texts[0]):
            if self.canvas.itemcget(i, 'text') != '9':
                c = self.canvas.coords(i)
                surrounding_texts = self.canvas.find_overlapping(c[0] - self.tile_size, c[1] - self.tile_size, c[0] + self.tile_size, c[1] + self.tile_size)
                surrounding_mines = 0
                for text in surrounding_texts:
                    if 'mine' in self.canvas.gettags(text):
                        surrounding_mines = surrounding_mines + 1
                self.canvas.itemconfig(i, text = str(surrounding_mines))
        for y in range(self.tile_count_y):
            for x in range(self.tile_count_x):
                cover = self.canvas.create_rectangle(x*self.tile_size + 1, y*self.tile_size + 1, x*self.tile_size + self.tile_size, y*self.tile_size + self.tile_size, fill=self.palette.primary, outline='', tags=self.TAG_PRIM)
                self.canvas.tag_bind(cover, "<Button-1>", lambda event, cover = cover: self.click_no_mine(event, cover))
                self.canvas.tag_bind(cover, "<Button-2>", lambda event, cover = cover: self.flag(event, cover))
                self.covers.append(cover)
        
    def checkZeros(self, text):
        c = self.canvas.coords(text)
        surrounding_texts = self.canvas.find_overlapping(c[0] - self.tile_size, c[1] - self.tile_size, c[0] + self.tile_size, c[1] + self.tile_size)
        self.canvas.delete(text)
        self.covers.remove(text + self.tile_count_x * self.tile_count_y)
        self.canvas.delete(text + self.tile_count_x * self.tile_count_y)
        self.canvas.update()
        time.sleep(0.001)
        for tex in surrounding_texts:
            if 'text' in self.canvas.gettags(tex) and self.canvas.itemcget(tex, 'text') == '0':
                self.checkZeros(tex)
            elif 'text' not in self.canvas.gettags(tex):
                self.canvas.delete(tex)
    def lose_event(self, cover):
        self.canvas.itemconfig(cover, fill = 'red')
        for cover in self.covers:
            if self.canvas.itemcget(cover - self.tile_count_x * self.tile_count_y, 'text') == '9':
                self.canvas.itemconfig(cover, fill=self.palette.error, tags=self.TAG_ERR)
            self.canvas.tag_unbind('all', "<Button-1>")
            self.canvas.tag_unbind('all', "<Button-2>")
        self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2)-3, int((self.tile_size*self.tile_count_y+1)/2)-3, text = "You Lose!", font = ("Consolas", 70), fill = self.palette.primary, tags=self.TAG_PRIM)
        self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2)+3, int((self.tile_size*self.tile_count_y+1)/2)-3, text = "You Lose!", font = ("Consolas", 70), fill = self.palette.primary, tags=self.TAG_PRIM)
        self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2)-3, int((self.tile_size*self.tile_count_y+1)/2)+3, text = "You Lose!", font = ("Consolas", 70), fill = self.palette.primary, tags=self.TAG_PRIM)
        self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2)+3, int((self.tile_size*self.tile_count_y+1)/2)+3, text = "You Lose!", font = ("Consolas", 70), fill = self.palette.primary, tags=self.TAG_PRIM)
        self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2), int((self.tile_size*self.tile_count_y+1)/2), text = "You Lose!", font = ("Consolas", 70), fill = self.palette.secondary, tags=self.TAG_SEC)   
        self.canvas.update()
        time.sleep(2)
        self.canvas.delete('all')
        self.create_board()
    def click_no_mine(self, event, cover):
        if self.canvas.itemcget(cover, 'fill') != self.palette.tertiary:
            text = cover - self.tile_count_x * self.tile_count_y
            if int(self.canvas.itemcget(text, 'text')) == 9:
                self.lose_event(cover)
            elif int(self.canvas.itemcget(text, 'text')) == 0:
                self.checkZeros(text)
            else:
                self.covers.remove(cover)
                self.canvas.delete(cover)
    def flag(self, event, cover):
        if self.canvas.itemcget(cover, 'fill') == self.palette.primary:
            self.canvas.itemconfig(cover, fill = self.palette.tertiary, tags=self.TAG_TER)
        else:
            self.canvas.itemconfig(cover, fill = self.palette.tertiary, tags=self.TAG_TER)
        c = 0
        for i in self.mines:
            if self.canvas.itemcget(i + self.tile_count_x * self.tile_count_y, 'fill') == self.palette.tertiary:
                c = c + 1
        if c == self.mine_count:
            self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2)-3, int((self.tile_size*self.tile_count_y+1)/2)-3, text = "You Win!", font = ("Consolas", 70), fill = self.palette.primary, tags=self.TAG_PRIM)
            self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2)+3, int((self.tile_size*self.tile_count_y+1)/2)-3, text = "You Win!", font = ("Consolas", 70), fill = self.palette.primary, tags=self.TAG_PRIM)
            self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2)-3, int((self.tile_size*self.tile_count_y+1)/2)+3, text = "You Win!", font = ("Consolas", 70), fill = self.palette.primary, tags=self.TAG_PRIM)
            self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2)+3, int((self.tile_size*self.tile_count_y+1)/2)+3, text = "You Win!", font = ("Consolas", 70), fill = self.palette.primary, tags=self.TAG_PRIM)
            self.canvas.create_text(int((self.tile_size*self.tile_count_x+1)/2), int((self.tile_size*self.tile_count_y+1)/2), text = "You Win!", font = ("Consolas", 70), fill = self.palette.secondary, tags=self.TAG_SEC)
            self.canvas.update()
            time.sleep(2)
            self.canvas.delete('all')
            self.create_board()
    def kill(self):
        super().kill()

    def update_colors(self):
        super().update_colors()



if __name__ == "__main__":
    palette_manager = PaletteManager()
    game = Minesweeper(palette_manager)
    game.start()