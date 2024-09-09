from tkinter import *
from abc import abstractmethod

class Game:

    TAG_PRIM = 'primary_color'
    TAG_SEC = 'secondary_color'
    TAG_TER = 'tertiary_color'
    TAG_CON = 'contrast_color'
    TAG_MCO = 'more_contrast_color'
    TAG_ERR = 'error_color'
    color_tags = [TAG_PRIM, TAG_SEC, TAG_TER, TAG_CON, TAG_MCO, TAG_ERR]
    toplevels = []

    @abstractmethod
    def __init__(self, root, palette):
        self.button_root = root
        self.palette = palette

    def create(self, width=500, height=500, title='Game', resizable = False, pos_x=50, pos_y=50):
        self.root = Toplevel(master=self.button_root)
        self.root.title(title)
        self.root.resizable(True if resizable else False, True if resizable else False)
        self.root.protocol("WM_DELETE_WINDOW", self.kill)

        padding = 5

        self.canvas = Canvas(self.root, highlightthickness=0, background=self.palette.secondary)
        self.root.config(background = self.palette.secondary)

        self.canvas.config(height = height+ 1, width = width + 1)
        self.canvas.pack(expand=1, padx = padding, pady = padding)

        self.root.minsize(height= height + padding * 2 + 1, width = width + padding * 2 + 1)
        self.root.geometry(str(width) + 'x' + str(height) + '+' + str(pos_x) + '+' + str(pos_y))

    # Appends new toplevel to self.toplevels
    # Returns the toplevel's canvas obj
    def create_toplevel(self, width=300, height=300, title='Toplevel', closable = False, resizable=False, pos_x=100, pos_y=100):
        toplevel = Toplevel(self.root)
        toplevel.title(title)
        toplevel.geometry(str(width) + 'x' + str(height) + '+' + str(pos_x) + '+' + str(pos_y))
        toplevel.resizable(True if resizable else False, True if resizable else False)
        if closable:
            pass
        else:
            toplevel.protocol("WM_DELETE_WINDOW", lambda : None)
        tl_canvas = Canvas(toplevel, highlightthickness=0, background=self.palette.secondary)
        tl_canvas.pack(fill = BOTH, expand = 1)

        self.toplevels.append(toplevel)
        return tl_canvas

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def kill(self):
        self.root.destroy()

    @abstractmethod
    def update_colors(self):
        self.canvas.config(background=self.palette.secondary)
        self.root.config(background = self.palette.secondary)
        for i in range(len(self.color_tags)):
            for item in self.canvas.find_withtag(self.color_tags[i]):
                self.canvas.itemconfig(item, fill=self.palette.palette[i])
