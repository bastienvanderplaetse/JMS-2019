from kivy.app import App
from utils import load_grid
from kivy.uix.label import Label
import sys
from kivy.uix.gridlayout import GridLayout
from tile import Tile
from kivy.core.window import Window

class SquareApp(App):
    def __init__(self, filename):
        super(SquareApp, self).__init__()
        self.grid = load_grid(filename)
        self.filename = filename

    def menu(self):
        menu = GridLayout(cols=3, rows=1)
        menu.add_widget(Label(text=self.filename))

        return menu

    def grid_layout(self):
        cols = len(self.grid[0])
        rows = len(self.grid)
        width = (Window.width-5) / cols
        height = (Window.height-5) / rows

        layout = GridLayout(cols=len(self.grid[0]), rows=len(self.grid),
            spacing=3, padding=3)

        index = 0
        for row in self.grid:
            for t in row:
                if t == 1:
                    state = 'down'
                else:
                    state = 'normal'
                tile = Tile(index, size_hint=[None, None], width=width, height=height, state=state)
                layout.add_widget(tile)

        return layout

    def build(self):
        base = GridLayout(cols=1, rows=2, row_force_default=True, row_default_height=30)

        base.add_widget(self.menu())
        base.add_widget(self.grid_layout())

        return base

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = './levels/basic'
    else:
        filename = sys.argv[1]
    SquareApp(filename).run()
