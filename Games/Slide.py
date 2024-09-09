from tkinter import *
import random
from PIL import Image, ImageTk
from Palette_Manager import PaletteManager
from GameApp import Game


#   TO DO: 
#       Not working with button??
#       Mathematically can generate unsolvably. Tackling this would be fun
#       Issue where pyimages automatically bind to the main root (button root)
#       Check for complete function does not always work
#       When I'm not as lazy finish implementing the squares. It should honestly be easier


class Slide(Game):

    def start(self):
        self.width, self.height = 750, 750
        super().create(width=self.width, height=self.height, title='Slide', resizable=True)

        self.countx, self.county = 4, 4
        self.empty_image_id = 0
        self.empty_image = 0

        #self.create_squares()
        self.create_images(Image.open("./Resources/moon.jpg"))

        self.root.mainloop()
    
    def check_complete(self):
        check_num = 1
        incorrect = False
        inLocation = False
        for y in range(self.county):
            for x in range(self.countx):
                ko = self.canvas.find_closest(int(x * self.tile_size_x + self.tile_size_x / 2), int(y * self.tile_size_y + self.tile_size_y / 2))
                num = int(''.join(x for x in self.canvas.itemcget(ko, "image") if x.isdigit()))
                if check_num == 2 and num == self.empty_image_id:
                    inLocation = True
                if num is not self.empty_image_id:
                    if num is not check_num:
                        incorrect = True
                        break
                    check_num = check_num + 1
        if not incorrect and inLocation:
            self.canvas.delete('all')
            self.canvas.create_image(self.width / 2, self.height / 2, image=self.full_image)
    def swap(self, event, id):
        c = self.canvas.coords(id)
        touching_tiles = self.canvas.find_overlapping(c[0] - 5, c[1] - self.tile_size_y / 2 - 5, c[0] + 5, c[1] + self.tile_size_y / 2 + 5) + self.canvas.find_overlapping(c[0] - self.tile_size_x / 2 - 5, c[1] - 5, c[0] + self.tile_size_x / 2 + 5, c[1] + 5)
        if self.empty_image in touching_tiles:
            c0 = self.canvas.coords(self.empty_image)
            self.canvas.coords(self.empty_image, self.canvas.coords(id))
            self.canvas.coords(id, c0)
            self.check_complete()
    '''def swap_square(self, event, square, text):
        c = self.canvas.coords(square)
        touching_tiles = self.canvas.find_overlapping(c[0] - 5, c[1] - self.tile_size_y / 2 - 5, c[0] + 5, c[1] + self.tile_size_y / 2 + 5) + self.canvas.find_overlapping(c[0] - self.tile_size_x / 2 - 5, c[1] - 5, c[0] + self.tile_size_x / 2 + 5, c[1] + 5)
        if self.empty_image in touching_tiles:
            c0 = self.canvas.coords(self.empty_image)
            self.canvas.coords(self.empty_image, self.canvas.coords(id))
            self.canvas.coords(id, c0)
            self.check_complete()
    def create_squares(self):
        self.tile_size_x = int(self.width / self.countx)
        self.tile_size_y = int(self.height / self.county)
        # Images must be stored otherwise get garbage collected
        self.square_text = []
        for y in range(self.county):
            for x in range(self.countx):
                if x + y != self.countx-1 + self.county-1:
                    square = self.canvas.create_rectangle(x*self.tile_size_x+1, y*self.tile_size_y+1, x * self.tile_size_x + self.tile_size_x - 1, y * self.tile_size_y + self.tile_size_y - 1, outline='', fill=self.palette.primary, tags=self.TAG_PRIM)
                    text = self.canvas.create_text(x*self.tile_size_x+1 + self.tile_size_x/2, y*self.tile_size_y+1 + self.tile_size_y/2, text=y*self.countx + x, font=("Consolas", 50), anchor='center')
                    self.square_text.append((square, text))
        
        random.shuffle(self.square_text)
        
        c = 0
        for y in range(self.county):
            for x in range(self.countx):
                if x + y != self.countx-1 + self.county-1:
                    self.canvas.moveto(self.square_text[c][0], x*self.tile_size_x+1, y*self.tile_size_y+1)
                    self.canvas.moveto(self.square_text[c][1], x*self.tile_size_x+1 + self.tile_size_x/2, y*self.tile_size_y+1 + self.tile_size_y/2)
                    self.canvas.tag_bind(self.square_text[c][0], "<Button-1>", lambda event, square = square, text=text: self.swap_square(event, square, text))
                    self.canvas.tag_bind(self.square_text[c][1], "<Button-1>", lambda event, square = square, text=text: self.swap_square(event, square, text))
                    c += 1'''
    def create_images(self, img):
        img = img.resize((min(img.width, self.width), min(img.height, self.height)), Image.LANCZOS)
        self.tile_size_x = int(img.width / self.countx)
        self.tile_size_y = int(img.height / self.county)
        # Images must be stored otherwise get garbage collected
        self.imgs = []
        for y in range(self.county):
            for x in range(self.countx):
                tk = ImageTk.PhotoImage(img.crop([x * self.tile_size_x + 1, y * self.tile_size_y + 1, x * self.tile_size_x + self.tile_size_x - 1, y * self.tile_size_y + self.tile_size_y - 1]))
                self.imgs.append(tk)
        full_image = ImageTk.PhotoImage(img.crop([0, 0, self.countx * self.tile_size_x, self.county * self.tile_size_y]))
        self.imgs[len(self.imgs)-1] = 0
        random.shuffle(self.imgs)
        c = 0
        for y in range(self.county):
            for x in range(self.countx):
                if self.imgs[c] != 0:
                    id = self.canvas.create_image(int(x * self.tile_size_x + self.tile_size_x / 2), int(y * self.tile_size_y + self.tile_size_y / 2), image=self.imgs[c])
                    self.canvas.tag_bind(id, "<Button-1>", lambda event, id = id: self.swap(event, id))
                else:
                    new_img = Image.new(mode="RGB", size=(int(self.tile_size_x), int(self.tile_size_y)))
                    fp = "./Resources/blank.png"
                    new_img.save(fp)
                    self.empty_image = self.canvas.create_image(int(x * self.tile_size_x + self.tile_size_x / 2), int(y * self.tile_size_y + self.tile_size_y / 2), image=ImageTk.PhotoImage((Image.open(fp))))
                    self.empty_image_id = int(''.join(x for x in self.canvas.itemcget(self.empty_image, "image") if x.isdigit()))
                c += 1




if __name__ == "__main__":
    palette_manager = PaletteManager()
    game = Slide(palette_manager)
    game.start()