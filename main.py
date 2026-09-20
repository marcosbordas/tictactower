import os

os.environ.setdefault('KIVY_NO_ARGS', '1')

from kivy import Config

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '880')
Config.set('graphics', 'resizable', '1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from ui import theme
from ui.screens import GameScreen, HelpScreen, MenuScreen


class TicTacTowerApp(App):
    title = 'TicTacTower'

    def build(self):
        Window.clearcolor = theme.BG_TOP
        self.manager = ScreenManager()
        self.menu = MenuScreen(name='menu')
        self.game = GameScreen(name='game')
        self.help = HelpScreen(name='help')
        self.menu.on_mode = self.start_game
        self.menu.on_help = self.show_help
        self.game.on_back = self.show_menu
        self.help.on_back = self.show_menu
        self.manager.add_widget(self.menu)
        self.manager.add_widget(self.game)
        self.manager.add_widget(self.help)
        return self.manager

    def start_game(self, mode, level):
        self.game.start(mode, level)
        self.manager.current = 'game'

    def show_help(self):
        self.manager.current = 'help'

    def show_menu(self):
        self.manager.current = 'menu'


if __name__ == '__main__':
    TicTacTowerApp().run()