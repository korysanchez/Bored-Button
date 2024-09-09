from tkinter import *
import random, time
from Palette_Manager import PaletteManager
from GameApp import Game


#   TO DO:
#       Create win / loss screen
#               ^-----|---> If any tile is power ^ 11, indicate a win, but allow the game to continue
#                     '>    Calculate that no move is possible, not just that all tiles != 0


class Twenty_Forty_Eight(Game):

    def start(self):
        self.size = 150
        self.power = 2
        super().create(width=self.size * 4, height=self.size * 4, title='2048', resizable=True)
        
        self.board = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        self.won = False
        
        self.create_board()
        self.paint()

        self.root.bind("<Left>", self.combine)
        self.root.bind('<Right>', self.combine)
        self.root.bind('<Up>', self.combine)
        self.root.bind('<Down>', self.combine)

        self.root.mainloop()

    def reset(self, win_condition):
        if win_condition:
            k0 = self.canvas.create_rectangle(125, 275, 375, 325, fill = self.palette.primary, outline = self.palette.secondary, tags=self.TAG_PRIM)
            k1 = self.canvas.create_text(250, 300, font = ('Consolas', 50), text = 'You Win!', fill = self.palette.secondary, tags=self.TAG_SEC)
        else:
            k0 = self.canvas.create_rectangle(50, 250, 450, 352, fill = self.palette.primary, outline = self.palette.secondary, tags = self.TAG_PRIM)
            k1 = self.canvas.create_text(250, 275, font = ('Consolas', 50), text = 'You Lose!', fill = self.palette.secondary, tags=self.TAG_SEC)
            k2 = self.canvas.create_text(250, 325, font = ('Consolas', 50), text = 'Word was ' + self.mystery_word, fill = self.palette.secondary, tags=self.TAG_SEC)
        self.canvas.update()
        time.sleep(2)
        self.canvas.delete(k0)
        self.canvas.delete(k1)
        if not win_condition:
            self.canvas.delete(k2)
        self.guess_num = 1
    
    def create_board(self):
        available = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 0:
                    available.append((y, x))
        if (len(available) <= 0):
            self.reset(win_condition=False)
        else:
            choice = random.randint(0, len(available)-1)
            if random.choice([0, 1, 1]) == 0:
                self.board[available[choice][0]][available[choice][1]] = self.power * self.power
            else:
                self.board[available[choice][0]][available[choice][1]] = self.power
    def paint(self):
        self.canvas.delete("all")
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] % self.power != 0:
                    self.board[y][x] += 1
                if self.board[y][x] != 0:
                    self.canvas.create_rectangle(x * self.size + 3, y * self.size + 3, x * self.size + self.size - 3, y * self.size + self.size - 3, fill = self.palette.primary, outline='', tags=self.TAG_PRIM)
                    text_size = 50 
                    #text_size = 18 + min(int(math.log2(self.board[y][x]) * 4), 50)
                    #    ^ Scales text size according to power
                    self.canvas.create_text(x * self.size + int(self.size / 2), y * self.size+ int(self.size / 2), text = self.board[y][x], font = ("Consolas", text_size), fill = self.palette.secondary, tags=self.TAG_SEC)
        self.canvas.update()
    
    def combine(self, event):
        self.shift_occurred = False
        for i in range(4):
            if event.keysym == 'Left':
                self.shift_left(i, 1)
            if event.keysym == 'Right':
                self.shift_right(i, 2)
            if event.keysym == 'Up':
                self.shift_up(1, i)
            if event.keysym == 'Down':
                self.shift_down(2, i)
        if self.shift_occurred:
            self.create_board()
            self.paint()

    
    def shift_left(self, y, x):
        if x >= 1 and x <= 3:
            if self.board[y][x] != 0:
                if self.board[y][x-1] == self.board[y][x]:
                    self.board[y][x-1] = self.board[y][x-1] * self.power - 1
                    self.board[y][x] = 0
                    self.shift_occurred = True
                elif self.board[y][x-1] == 0:
                    self.board[y][x-1] = self.board[y][x]
                    self.board[y][x] = 0
                    self.shift_occurred = True
                    self.shift_left(y, x - 1)
                self.shift_left(y, x + 1)
            else:
                self.shift_left(y, x + 1)
    
    def shift_right(self, y, x):
        if x >= 0 and x <= 2:
            if self.board[y][x] != 0:
                if self.board[y][x+1] == self.board[y][x]:
                    self.board[y][x+1] = self.board[y][x+1] * self.power - 1
                    self.board[y][x] = 0
                    self.shift_occurred = True
                elif self.board[y][x+1] == 0:
                    self.board[y][x+1] = self.board[y][x]
                    self.board[y][x] = 0
                    self.shift_occurred = True
                    self.shift_right(y, x + 1)
                self.shift_right(y, x - 1)
            else:
                self.shift_right(y, x - 1)
    
    def shift_down(self, y, x):
        if y >= 0 and y <= 2:
            if self.board[y][x] != 0:
                if self.board[y+1][x] == self.board[y][x]:
                    self.board[y+1][x] = self.board[y+1][x] * self.power - 1
                    self.board[y][x] = 0
                    self.shift_occurred = True
                elif self.board[y+1][x] == 0:
                    self.board[y+1][x] = self.board[y][x]
                    self.board[y][x] = 0
                    self.shift_occurred = True
                    self.shift_down(y + 1, x)
                self.shift_down(y - 1, x)
            else:
                self.shift_down(y - 1, x)

    def shift_up(self, y, x):
        if y >= 1 and y <= 3:
            if self.board[y][x] != 0:
                if self.board[y-1][x] == self.board[y][x]:
                    self.board[y-1][x] = self.board[y-1][x] * self.power - 1
                    self.board[y][x] = 0
                    self.shift_occurred = True
                elif self.board[y-1][x] == 0:
                    self.board[y-1][x] = self.board[y][x]
                    self.board[y][x] = 0
                    self.shift_occurred = True
                    self.shift_up(y-1, x)
                self.shift_up(y+1, x)
            else:
                self.shift_up(y+1, x)



if __name__ == "__main__":
    palette_manager = PaletteManager()
    game = Twenty_Forty_Eight(palette_manager)
    game.start()