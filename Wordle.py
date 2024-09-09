from tkinter import *
import random, time, os
from Palette_Manager import PaletteManager
from GameApp import Game

#   TO DO:
#       Could use a better dictionary, couldn't find the original Wordle dictionary
#       I believe that multiple letters in the wrong position will incorectly mark both as wrong position
#       i.e. Word is GOODS. Guess: ODDLY, both D's will be marked as in the word, but the wrong spot.
#            The correct process will mark only the 1st D as in the wrong spot, and the 2nd D as not in the word


class Wordle(Game):

    def start(self):
        super().create(title='Wordle', width=500, height=600, resizable = True)
        self.words = open("./Resources/allFiveWords.txt", 'r').read().splitlines()
        self.valid_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.letters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
        
        self.active_tile = 0
        self.final_letter = False
        self.guess_num = 1

        self.won = False
        self.create_board()
        self.create_keyboard()

        self.root.bind("<Return>", self.check_word)
        self.root.bind("<Key>", self.enter_letter)
        self.root.bind("<BackSpace>", self.remove_letter)

        self.mystery_word = random.choice(self.words)

        self.root.mainloop()

    def reset(self, win_condition):
        self.won = True if win_condition else False
        self.root.unbind("<BackSpace>")
        self.root.unbind("<Return>")
        self.root.unbind("<Key>")

        if win_condition:
            k0 = self.canvas.create_rectangle(125, 275, 375, 325, fill = self.palette.primary, outline = self.palette.secondary, tags=self.TAG_PRIM)
            k1 = self.canvas.create_text(250, 300, font = ('Consolas', 50), text = 'You Win!', fill = self.palette.secondary, tags=self.TAG_SEC)
        else:
            k0 = self.canvas.create_rectangle(50, 250, 450, 352, fill = self.palette.primary, outline = self.palette.secondary, tags = self.TAG_PRIM)
            k1 = self.canvas.create_text(250, 275, font = ('Consolas', 50), text = 'You Lose!', fill = self.palette.secondary, tags=self.TAG_SEC)
            k2 = self.canvas.create_text(250, 325, font = ('Consolas', 50), text = 'Word was ' + self.mystery_word, fill = self.palette.secondary, tags=self.TAG_SEC)
        self.canvas.update()
        time.sleep(2)
        for i in range(len(self.tiles)):
            self.canvas.itemconfig(i+1, fill = self.palette.primary)
            self.canvas.itemconfig(i + 31, text = '')
        self.active_tile = -1
        for i in range(1, 57, 2):
            self.tl_canvas.itemconfig(i, fill = self.palette.primary, tags=self.TAG_PRIM)
        self.mystery_word = random.choice(self.words)
        self.root.bind("<BackSpace>", self.remove_letter)
        self.root.bind("<Return>", self.check_word)
        self.root.bind("<Key>", self.enter_letter)
        self.won = False
        self.canvas.delete(k0)
        self.canvas.delete(k1)
        if not win_condition:
            self.canvas.delete(k2)
        self.guess_num = 1
    def create_board(self):
        self.tiles = []
        for y in range(0, 600, 100):
            for x in range(0, 500, 100):
                tile = self.canvas.create_rectangle(x + 1, y + 1, x+99, y+99, fill=self.palette.primary, outline='', tags=self.TAG_PRIM)
                self.tiles.append(tile)
        for y in range(0, 600, 100):
            for x in range(0, 500, 100):
                text = self.canvas.create_text(x + 50, y + 50, font = ('Consolas', 100), text = '', fill = self.palette.secondary, tags=self.TAG_SEC)
    def check_word(self, event=None):
        guess = ''
        won = False
        for i in range(5, 0, -1):
            guess = guess + str(self.canvas.itemcget(self.active_tile + 32 - i, 'text'))
        if self.final_letter and self.guess_num <= 6 and str.lower(guess) in self.words:
            correct = 0
            for i in range(5, 0, -1):
                letter = str(self.canvas.itemcget(self.active_tile + 32 - i, 'text'))
                if str.lower(letter) == self.mystery_word[5 - i]:
                    self.canvas.itemconfig(self.active_tile - i + 2, fill = self.palette.contrast, tags=self.TAG_CON)
                    correct += 1
                    self.keyboard_right_spot(letter)
                elif str.lower(letter) in self.mystery_word:
                    self.canvas.itemconfig(self.active_tile - i + 2, fill = self.palette.tertiary, tags=self.TAG_TER)
                    self.keyboard_wrong_spot(letter)
                else:
                    self.keyboard_block(letter)
            self.guess_num += 1
            if correct == 5:
                self.reset(win_condition=True)
            self.active_tile += 1
            self.final_letter = False
        elif self.final_letter and self.guess_num <= 6 and str.lower(guess) not in self.words:
            for i in range(5, 0, -1):
                self.canvas.itemconfig(self.active_tile - i + 2, fill = self.palette.error, tags=self.TAG_ERR)
            self.canvas.update()
            time.sleep(0.15)
            for i in range(5, 0, -1):
                self.canvas.itemconfig(self.active_tile - i + 2, fill = self.palette.primary, tags=self.TAG_PRIM)
            self.canvas.update()
        if self.guess_num > 6 and not won:
            self.guess_num += 1
            self.reset(win_condition=False)
            self.active_tile += 1
            self.final_letter = False
    def enter_letter(self, event=None):
        if (str.upper(event.keysym) in self.letters) and self.active_tile <= self.guess_num * 5 + 1 and not self.final_letter:
            self.canvas.itemconfig(self.active_tile + 31, text=str.upper(event.keysym))
            if (self.active_tile + 1) % 5 == 0:
                self.final_letter = True
            else:
                self.active_tile += 1
    def remove_letter(self, event=None):
        if self.active_tile + 1 != 5 * (self.guess_num-1) + 1 and ((self.active_tile) % 5) != 0:
            if self.final_letter:
                self.final_letter = False
            else:
                self.active_tile -= 1
            self.canvas.itemconfig(self.active_tile + 31, text = '')
    
    #keyboard functions 
    def create_keyboard(self):
        self.tl_canvas = super().create_toplevel(width=800, height=240, pos_x=600, pos_y=200, title='Keyboard')
        self.canvas_texts = []
        row_lengths = [10, 9, 7]
        size, inset, x_offset, letter = 80, 2, 0, 0
        for row in range(3):
            x_offset += 20 * row
            for x in range(row_lengths[row]):
                text = self.tl_canvas.create_rectangle(x*size+inset+x_offset, row*size+inset, x*size+size-inset+x_offset, row*size+size-inset, fill=self.palette.primary, outline = '', tags=self.TAG_PRIM)
                self.tl_canvas.create_text(x*size+inset+x_offset+38, row*size+inset+38, fill=self.palette.secondary, text=self.letters[letter], font=('Consolas', 70), tags=self.TAG_SEC)
                self.canvas_texts.append(text)
                letter += 1
    def keyboard_block(self, n):
        self.tl_canvas.itemconfig(self.canvas_texts[self.letters.index(str.upper(n))], fill = self.palette.secondary, tags=self.TAG_SEC)
    def keyboard_wrong_spot(self, n):
        self.tl_canvas.itemconfig(self.canvas_texts[self.letters.index(str.upper(n))], fill = self.palette.tertiary, tags=self.TAG_TER)
    def keyboard_right_spot(self, n):
        self.tl_canvas.itemconfig(self.canvas_texts[self.letters.index(str.upper(n))], fill = self.palette.contrast, tags=self.TAG_CON)

    def update_colors(self):
        super().update_colors()
        self.tl_canvas.config(background=self.palette.secondary)
        for i in range(len(self.color_tags)):
            for item in self.tl_canvas.find_withtag(self.color_tags[i]):
                self.tl_canvas.itemconfig(item, fill=self.palette.palette[i])

if __name__ == "__main__":
    palette_manager = PaletteManager()
    game = Wordle(palette_manager)
    game.start()