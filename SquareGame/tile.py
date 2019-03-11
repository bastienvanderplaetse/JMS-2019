from kivy.uix.togglebutton import ToggleButton

class Tile(ToggleButton):
    def __init__(self, index, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.id = str(index)
