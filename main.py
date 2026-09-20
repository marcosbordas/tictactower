import os

os.environ.setdefault('KIVY_NO_ARGS', '1')

from kivy import Config

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '880')
Config.set('graphics', 'resizable', '1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from ui.screens import GameScreen, MenuScreen


class TicTacTowerApp(App):
    title = 'TicTacTower'

    def build(self):
        self.manager = ScreenManager()
        self.menu = MenuScreen(name='menu')
        self.game = GameScreen(name='game')
        self.menu.on_mode = self.start_game
        self.game.on_back = self.show_menu
        self.manager.add_widget(self.menu)
        self.manager.add_widget(self.game)
        return self.manager

    def start_game(self, mode, level):
        self.game.start(mode, level)
        self.manager.current = 'game'

    def show_menu(self):
        self.manager.current = 'menu'


if __name__ == '__main__':
    TicTacTowerApp().run()