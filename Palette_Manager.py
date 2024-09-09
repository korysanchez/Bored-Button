class PaletteManager:
    palettes = [
    #Primary          Secondary          Tertiary          Contrast         More Contrast           Error
    ['tan',           '#964B00',        '#D79771',          'lime',           'yellow',             'red'],
    ['lime',           'black',          'green',           'blue',           'yellow',             'red'],
    ['brown',         '#964B00',        '#D79771',          'lime',           'yellow',             'red'],
    ['purple',        'blue',           '#D79771',          'lime',           'yellow',             'red'],
    ['black',         'violet',         '#D79771',         'purple',          'yellow',             'red'],
    ['black',         'yellow',         'yellow',           'lime',           'yellow',             'red'],
    ['grey',          'magenta',        '#D79771',          'lime',           'black',              'red'],
    ['blue',          'orange',         '#D79771',          'lime',           'yellow',             'red'],
    ['orangered',     'orange',         '#D79771',          'lime',           'black',              'red']
    ]
    def __init__(self, num=0):
        self.set_palette(num)
        self.palette_count = len(self.palettes)
    def prinPall(self):
        print(self)
    def set_palette(self, num):
        self.num = num

        self.palette = self.palettes[num]
        self.primary        =  self.palettes[num][0]
        self.secondary      =  self.palettes[num][1]
        self.tertiary       =  self.palettes[num][2]
        self.contrast       =  self.palettes[num][3]
        self.more_contrast  =  self.palettes[num][4]
        self.error          =  self.palettes[num][5]