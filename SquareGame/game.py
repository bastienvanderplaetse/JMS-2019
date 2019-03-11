from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from tile import Tile, RED
from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<SquareGame>:
    container: None
    Container: container
""")

class SquareGame(Widget):
    def __init__(self, grid):
        super(SquareGame, self).__init__()
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        self.container = GridLayout(cols=len(grid[0]), rows=len(grid))
        self.grid = grid

        index = 0
        for row in self.grid:
            for tile in row:
                self.container.add_widget(Tile())
                index = index + 1

    # layout = GridLayout(cols=0, rows=0)
    #
    # def display_grid(self, grid):
    #     rows = len(grid)
    #     cols = len(grid[0])
    #
    #     layout = GridLayout(cols=cols, rows=rows)
    #
    #     for row in grid:
    #         for tile in row:
    #             tile = Tile(pos=(0,0), size_hint=(10,10), color=RED)
    #             layout.add_widget(tile)
