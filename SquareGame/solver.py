from kivy.app import App
from utils import load_grid
from kivy.uix.label import Label
import sys
from kivy.uix.gridlayout import GridLayout
from tile import Tile
from kivy.core.window import Window
from neuroevolution import NEAT
from copy import deepcopy
import numpy as np
import time

class SquareApp(App):
    def __init__(self, filename):
        super(SquareApp, self).__init__()

        self.true_grid = load_grid(filename)
        self.predict_grid = []
        for row in self.true_grid:
            r = [0] * len(row)
            self.predict_grid.append(r)
        self.filename = filename
        self.neat = NEAT(output_size=1)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':
            while True:
                output, score = self.evaluate_generation()
                self.update_grid(output)
                if score == 25:
                    break
                if score == 17:
                    break

        return True

    def evaluate_generation(self):
        scores = []
        outputs = []
        rows = len(self.predict_grid)
        cols = len(self.predict_grid[0])
        while not self.neat.generation_finished():
            score = 0
            predictions = deepcopy(self.predict_grid)
            self.neat.prepare_next()
            for i in range(rows):
                for j in range(cols):
                    output = self.neat.feed([i,j])[0]
                    predictions[i][j] = output
                    if output == self.true_grid[i][j]:
                        score = score + 1
            self.neat.fitness(score)
            scores.append(score)
            outputs.append(predictions)

        self.neat.next_generation()

        index = np.argmax(scores)

        return outputs[index], max(scores)

    def menu(self):
        menu = GridLayout(cols=3, rows=1)
        menu.add_widget(Label(text=self.filename))

        return menu

    def update_grid(self, predict):
        self.grid.clear_widgets()
        # self.grid = GridLayout(cols=cols, rows=rows, spacing=3, padding=3)
        cols = len(self.predict_grid[0])
        rows = len(self.predict_grid)
        width = (Window.width-5) / cols
        height = (Window.height-5) / rows
        index = 0
        for row in predict:
            for t in row:
                if t == 1:
                    state = 'down'
                else:
                    state = 'normal'
                tile = Tile(index, size_hint=[None, None], width=width, height=height, state=state)
                self.grid.add_widget(tile)

    def grid_layout(self):
        cols = len(self.predict_grid[0])
        rows = len(self.predict_grid)
        width = (Window.width-5) / cols
        height = (Window.height-5) / rows

        self.grid = GridLayout(cols=cols, rows=rows, spacing=3, padding=3)

        index = 0
        for row in self.predict_grid:
            for t in row:
                if t == 1:
                    state = 'down'
                else:
                    state = 'normal'
                tile = Tile(index, size_hint=[None, None], width=width, height=height, state=state)
                self.grid.add_widget(tile)

        return self.grid

    def build(self):
        base = GridLayout(cols=1, rows=2, row_force_default=True, row_default_height=30)

        base.add_widget(self.menu())
        base.add_widget(self.grid_layout())

        base._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        base._keyboard.bind(on_key_down=self._on_keyboard_down)

        return base

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = './levels/basic'
    else:
        filename = sys.argv[1]
    SquareApp(filename).run()
