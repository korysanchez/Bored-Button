from tkinter import *
from Palette_Manager import PaletteManager
from random import shuffle
from time import sleep


from Games.Wordle import Wordle
from Games.Minesweeper import Minesweeper
from Games.Twenty_Forty_Eight import Twenty_Forty_Eight
from Games.Slide import Slide
from Games.Color_Fill import Color_Fill

class BoredButton:

    current_game = -1
    color_tl = None
    def __init__(self, palette_manager):
        self.root = Tk()
        self.root.title('Bored Button')
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.user_exit)
        self.root.geometry('200x200+1200+650')


        self.palette_manager = palette_manager
        self.button_color = self.palette_manager.primary

        self.canvas = Canvas(self.root, highlightthickness = 0, background = '#2b2b2b')
        self.canvas.pack(fill = BOTH, expand = 1)

        self.button = self.canvas.create_oval(20, 20, 180, 180, fill = self.button_color, outline = '')
        self.canvas.tag_bind(self.button, "<Button-1>", self.button_press)

        self.color_config = Button(self.canvas, text='Colors', width=1, height=1, font=("Consolas", 10), command=self.color_configure)
        self.color_config.place(x=200, y=200)




        self.root.bind("<Enter>", self.mouse_enter)
        self.root.bind("<Leave>", self.mouse_exit)
    def run(self, games):
        self.games = games
        shuffle(self.games)
        self.root.mainloop()
    def get_root(self):
        return self.root
    # User events
    def mouse_enter(self, event=None):
        self.color_config.place_configure(x=0, y=0)
    def mouse_exit(self, event=None):
        self.color_config.place_configure(x=200, y=200)
    def user_exit(self, event=None):
        self.games[self.current_game].kill()
        self.root.destroy()

    # Running game logic
    def button_press(self, event=None):
        #Button press animation--------
        self.canvas.itemconfig(self.button, fill = '#2b2b2b')
        self.canvas.update()
        sleep(0.01)
        self.canvas.itemconfig(self.button, fill = self.button_color)

        #Run next game-----------------
        try:
            self.games[self.current_game].kill()
        except:
            pass
        self.current_game += 1
        if self.current_game > len(self.games)-1:
            shuffle(self.games)
            self.current_game = 0
        self.games[self.current_game].start()

    # Color changing
    def remove_tl(self, event=None):
        self.color_tl.destroy()
        self.color_tl = None
    def change_col(self, _, num):
        self.palette_manager.set_palette(num)
        self.button_color = self.palette_manager.primary
        self.canvas.itemconfig(self.button, fill=self.button_color)
        try:
            self.games[self.current_game].update_colors()
        except:
            pass
    def color_configure(self, event=None):
        if self.color_tl == None:
            y_height, x_width = 20, 96 
            self.color_tl = Toplevel(self.root, background='#2b2b2b')
            self.color_tl.title('Colors')
            self.color_tl.resizable(False, False)
            height = (self.palette_manager.palette_count+1) * y_height+2
            self.color_tl.geometry('200x'+ str(height) +'+1200+'+str(620-height))
            self.color_tl.protocol("WM_DELETE_WINDOW", self.remove_tl)

            canvas = Canvas(self.color_tl, highlightthickness=0, bg='#2b2b2b')
            canvas.pack(expand=1, fill=BOTH, padx=2, pady=2)


            for i in range(self.palette_manager.palette_count):
                y = i*y_height + 2*i + 1
                for j in range(2):
                    x = j*x_width+1
                    change_color = canvas.create_rectangle(x, y, x+x_width, y+y_height, fill=self.palette_manager.palettes[i][j], outline='')
                    canvas.tag_bind(change_color, "<Button-1>", lambda event, num=i: self.change_col(event, num))

            self.color_tl.mainloop()


if __name__ == '__main__':
    pm = PaletteManager()
    button = BoredButton(pm)
    r = button.get_root()

    games = [Wordle(r, pm), Minesweeper(r, pm), Twenty_Forty_Eight(r, pm), Slide(r, pm), Color_Fill(r, pm), Word_Hunt(r, pm)]
    button.run(games)

