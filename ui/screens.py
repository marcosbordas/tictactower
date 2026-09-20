from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

from game import ai
from game.logic import UltimateTicTacToe
from ui import theme
from ui.board import BoardWidget

HUMAN = 'X'
CPU = 'O'


def styled_button(text, primary=False, small=False, **kwargs):
    button = Button(text=text, **kwargs)
    button.background_normal = ''
    button.background_down = ''
    button.background_color = theme.ACCENT if primary else theme.CARD
    button.color = (0.06, 0.07, 0.09, 1) if primary else theme.TEXT
    button.font_size = sp(17 if not small else 13)
    button.padding = (12, 6)
    if small:
        button.size_hint_y = None
        button.height = dp(38)
    return button


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_mode = None
        root = BoxLayout(orientation='vertical',
                         padding=[dp(22), dp(46), dp(22), dp(18)],
                         spacing=dp(14))
        root.add_widget(Label(text='TIC TAC TOWER', font_size=sp(42), bold=True, color=theme.TEXT))
        root.add_widget(Label(text='Ultimate Tic-Tac-Toe 9x9', font_size=sp(17), color=theme.ACCENT))
        root.add_widget(Label(text='Gana 3 mini-tableros en linea', font_size=sp(13), color=theme.MUTED))
        root.add_widget(Widget())
        root.add_widget(styled_button('Contra la CPU', primary=True, on_release=self._play_cpu))
        root.add_widget(self._difficulty_row())
        root.add_widget(styled_button('2 Jugadores (mismo telefono)', on_release=self._play_pvp))
        root.add_widget(Widget())
        root.add_widget(Label(text='por Marcos Bordas Gonzalez', font_size=sp(12), color=theme.MUTED))
        root.add_widget(styled_button('Salir', small=True, on_release=lambda *_: Window.close()))
        self.add_widget(root)

    def _difficulty_row(self):
        row = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        self._difficulty_buttons = []
        for text, level in (('Facil', ai.EASY), ('Medio', ai.MEDIUM), ('Dificil', ai.HARD)):
            toggle = ToggleButton(text=text, group='difficulty')
            toggle.background_normal = ''
            toggle.background_down = ''
            toggle.color = theme.TEXT
            toggle.font_size = sp(15)
            toggle.level = level
            toggle.bind(state=self._repaint_toggle)
            if level == ai.MEDIUM:
                toggle.state = 'down'
            row.add_widget(toggle)
            self._difficulty_buttons.append(toggle)
        self._repaint_toggle()
        return row

    def _repaint_toggle(self, *_):
        for toggle in self._difficulty_buttons:
            if toggle.state == 'down':
                toggle.background_color = theme.ACCENT
                toggle.color = (0.06, 0.07, 0.09, 1)
            else:
                toggle.background_color = theme.CARD
                toggle.color = theme.TEXT

    def _selected_level(self):
        for toggle in self._difficulty_buttons:
            if toggle.state == 'down':
                return toggle.level
        return ai.MEDIUM

    def _play_cpu(self, *_):
        if self.on_mode:
            self.on_mode('cpu', self._selected_level())

    def _play_pvp(self, *_):
        if self.on_mode:
            self.on_mode('pvp', None)


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = 'pvp'
        self.level = ai.MEDIUM
        self.game = UltimateTicTacToe()
        self.on_back = None

        layout = BoxLayout(orientation='vertical', padding=[dp(8), dp(6), dp(8), dp(6)], spacing=dp(6))
        top = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        self.btn_menu = styled_button('Menu', small=True, on_release=self._go_menu)
        self.btn_menu.size_hint_x = 0.28
        self.btn_restart = styled_button('Nuevo', small=True, on_release=self._restart)
        self.btn_restart.size_hint_x = 0.28
        self.status = Label(text='', font_size=sp(16), bold=True, halign='center')
        top.add_widget(self.btn_menu)
        top.add_widget(self.status)
        top.add_widget(self.btn_restart)

        self.board = BoardWidget()
        self.hint = Label(text='Tu movimiento envia al rival a ese tablero',
                          font_size=sp(12), color=theme.MUTED,
                          size_hint_y=None, height=dp(26))

        layout.add_widget(top)
        layout.add_widget(self.board)
        layout.add_widget(self.hint)
        self.add_widget(layout)

        self.board.on_move = self._human_move

    def start(self, mode, level):
        self.mode = mode
        self.level = level
        self.game = UltimateTicTacToe()
        self.board.game = self.game
        self.board.redraw()
        self._update_status()

    def _human_move(self, bi, r, c):
        if self.game.game_result() is not None:
            return
        if self.mode == 'cpu' and self.game.turn != HUMAN:
            return
        self._apply(bi, r, c)

    def _apply(self, bi, r, c):
        if not self.game.play(bi, r, c):
            return
        self.board.redraw()
        if self.game.game_result() is not None:
            self._update_status()
            return
        if self.mode == 'cpu' and self.game.turn == CPU:
            Clock.schedule_once(self._cpu_turn, 0.35)
        self._update_status()

    def _cpu_turn(self, dt):
        if self.manager is None or self.manager.current != 'game':
            return
        if self.game.game_result() is not None:
            return
        move = ai.choose_move(self.game, self.level)
        if move:
            self._apply(*move)

    def _update_status(self):
        result = self.game.game_result()
        if result == 'X' or result == 'O':
            self.status.text = f'GANA {result}!'
            self.status.color = theme.GOLD
        elif result == 'D':
            self.status.text = 'Empate!'
            self.status.color = theme.MUTED
        elif self.mode == 'cpu':
            if self.game.turn == HUMAN:
                self.status.text = 'Tu turno (X)'
                self.status.color = theme.X_COLOR
            else:
                self.status.text = 'Turno de la CPU (O)...'
                self.status.color = theme.O_COLOR
        else:
            self.status.text = f'Turno de {self.game.turn}'
            self.status.color = theme.X_COLOR if self.game.turn == 'X' else theme.O_COLOR

    def _restart(self, *_):
        self.start(self.mode, self.level)

    def _go_menu(self, *_):
        Clock.unschedule(self._cpu_turn)
        if self.on_back:
            self.on_back()