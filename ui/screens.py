from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from game import ai
from game.logic import UltimateTicTacToe
from ui import theme
from ui.board import BoardWidget
from ui.neon import NeonButton, NeonPill, NeonToggle, attach_background

HUMAN = 'X'
CPU = 'O'


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_mode = None
        self.on_help = None
        attach_background(self)
        root = BoxLayout(orientation='vertical',
                         padding=[dp(26), dp(40), dp(26), dp(14)],
                         spacing=dp(12))
        root.add_widget(Widget())
        title = Label(text='TIC TAC TOWER',
                      font_name=theme.FONT_UI, font_size=theme.TITLE_SIZE,
                      color=theme.CYAN, halign='center')
        title.outline_width = 3
        title.outline_color = (0.02, 0.03, 0.06, 1)
        root.add_widget(title)
        root.add_widget(Label(text='ULTIMATE TIC-TAC-TOE 9x9',
                              font_name=theme.FONT_UI, font_size=theme.SUB_SIZE,
                              color=theme.VIOLET))
        root.add_widget(Label(text='Gana 3 mini-tableros en linea',
                              font_name=theme.FONT_BODY, font_size=theme.SMALL_SIZE,
                              color=theme.MUTED))
        root.add_widget(Widget())
        root.add_widget(NeonButton(text='JUGAR VS CPU', primary=True,
                                   on_release=self._play_cpu))
        root.add_widget(self._difficulty_row())
        root.add_widget(NeonButton(text='DOS JUGADORES',
                                   on_release=self._play_pvp))
        root.add_widget(NeonButton(text='COMO SE JUEGA?', small=True,
                                   on_release=self._open_help))
        root.add_widget(Widget())
        root.add_widget(Label(text='por Marcos Bordas Gonzalez',
                              font_name=theme.FONT_UI, font_size=sp(11),
                              color=theme.MUTED))
        root.add_widget(NeonButton(text='SALIR', small=True,
                                   on_release=lambda *_: Window.close()))
        self.add_widget(root)

    def _difficulty_row(self):
        row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        self._difficulty_buttons = []
        self._selected_level = ai.MEDIUM
        for text, level in (('Facil', ai.EASY), ('Medio', ai.MEDIUM), ('Dificil', ai.HARD)):
            toggle = NeonToggle(text=text, small=True, selected=(level == ai.MEDIUM))
            toggle.level = level
            toggle.bind(on_release=lambda *_, t=toggle: self._select_difficulty(t))
            self._difficulty_buttons.append(toggle)
            row.add_widget(toggle)
        return row

    def _select_difficulty(self, chosen):
        for toggle in self._difficulty_buttons:
            toggle.selected = (toggle is chosen)
        self._selected_level = chosen.level

    def _play_cpu(self, *_):
        if self.on_mode:
            self.on_mode('cpu', self._selected_level)

    def _play_pvp(self, *_):
        if self.on_mode:
            self.on_mode('pvp', None)

    def _open_help(self, *_):
        if self.on_help:
            self.on_help()


class HelpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_back = None
        attach_background(self)
        root = BoxLayout(orientation='vertical',
                         padding=[dp(22), dp(26), dp(22), dp(14)],
                         spacing=dp(10))

        head = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        back = NeonButton(text='ATRAS', small=True, on_release=self._back)
        back.size_hint_x = 0.32
        head.add_widget(back)
        head.add_widget(Widget())
        root.add_widget(head)

        title = Label(text='COMO SE JUEGA',
                      font_name=theme.FONT_UI, font_size=theme.SUB_SIZE,
                      color=theme.CYAN, size_hint_y=None, height=dp(34))
        root.add_widget(title)

        text = (
            '1. Es un tablero 9x9 dividido en 9 mini-tableros.\n\n'
            '2. Ganas un mini-tablero cuando pones 3 de tus '
            'simbolos en linea (horizontal, vertical o diagonal).\n\n'
            '3. Con cada jugada envias a tu rival al mini-tablero '
            'que senala la casilla que acabas de jugar.\n\n'
            '4. Siempre debes jugar en el mini-tablero marcado '
            'con el borde brillante. Si ese tablero esta lleno o '
            'ganado, eliges cualquier mini-tablero libre.\n\n'
            '5. Gana la partida quien consiga 3 mini-tableros '
            'en linea.'
        )
        body = Label(text=text,
                     font_name=theme.FONT_BODY, font_size=theme.BODY_SIZE,
                     color=theme.TEXT, halign='center', valign='top')
        body.bind(size=lambda *_: setattr(body, 'text_size', body.size))
        scroll = ScrollView()
        scroll.add_widget(body)
        root.add_widget(scroll)
        root.add_widget(NeonButton(text='ENTENDIDO', primary=True,
                                   on_release=self._back))
        self.add_widget(root)

    def _back(self, *_):
        if self.on_back:
            self.on_back()


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = 'pvp'
        self.level = ai.MEDIUM
        self.game = UltimateTicTacToe()
        self.on_back = None
        attach_background(self)
        layout = BoxLayout(orientation='vertical',
                           padding=[dp(8), dp(6), dp(8), dp(6)], spacing=dp(6))
        top = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        self.btn_menu = NeonButton(text='MENU', small=True, on_release=self._go_menu)
        self.btn_menu.size_hint_x = 0.3
        self.status = NeonPill(text='', tint=theme.CYAN)
        self.btn_restart = NeonButton(text='NUEVO', small=True, on_release=self._restart)
        self.btn_restart.size_hint_x = 0.3
        top.add_widget(self.btn_menu)
        top.add_widget(self.status)
        top.add_widget(self.btn_restart)

        self.board = BoardWidget()
        self.hint = Label(text='',
                          font_name=theme.FONT_BODY, font_size=theme.SMALL_SIZE,
                          color=theme.MUTED, halign='center',
                          size_hint_y=None, height=dp(30))

        layout.add_widget(top)
        layout.add_widget(self.board)
        layout.add_widget(self.hint)
        self.add_widget(layout)

        self.board.on_move = self._human_move

    def on_enter(self):
        self.board.set_running(True)

    def on_leave(self):
        self.board.set_running(False)
        Clock.unschedule(self._cpu_turn)

    def start(self, mode, level):
        self.mode = mode
        self.level = level
        self.game = UltimateTicTacToe()
        self.board.game = self.game
        self.board.last_move = None
        self.board.redraw()
        self._update_status()
        self._update_hint()

    def _human_move(self, bi, r, c):
        if self.game.game_result() is not None:
            return
        if self.mode == 'cpu' and self.game.turn != HUMAN:
            return
        self._apply(bi, r, c)

    def _apply(self, bi, r, c):
        if not self.game.play(bi, r, c):
            return
        self.board.mark((bi, r, c))
        self.board.redraw()
        if self.game.game_result() is not None:
            self.board.set_running(False)
            self._update_status()
            self._update_hint()
            return
        if self.mode == 'cpu' and self.game.turn == CPU:
            Clock.schedule_once(self._cpu_turn, 0.55)
        self._update_status()
        self._update_hint()

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
        if result in ('X', 'O'):
            self.status.text = f'GANA {result}!'
            self.status.tint = theme.GOLD
        elif result == 'D':
            self.status.text = 'EMPATE'
            self.status.tint = theme.MUTED
        elif self.mode == 'cpu':
            if self.game.turn == HUMAN:
                self.status.text = 'TU TURNO'
                self.status.tint = theme.X_COLOR
            else:
                self.status.text = 'CPU PIENSA...'
                self.status.tint = theme.O_COLOR
        else:
            self.status.text = f'TURNO DE {self.game.turn}'
            self.status.tint = theme.X_COLOR if self.game.turn == 'X' else theme.O_COLOR

    def _update_hint(self):
        if self.game.game_result() is not None:
            self.hint.text = 'Pulsa NUEVO para jugar otra partida'
            self.hint.color = theme.MUTED
            return
        locked = self.game.active_board is not None
        if self.mode == 'cpu':
            if self.game.turn == CPU:
                self.hint.text = 'La CPU esta eligiendo su jugada...'
            elif locked:
                self.hint.text = 'Tu turno: juega en el tablero iluminado'
            else:
                self.hint.text = 'Tu turno: elige un mini-tablero libre'
        else:
            if locked:
                self.hint.text = f'Turno de {self.game.turn}: juega en el tablero iluminado'
            else:
                self.hint.text = f'Turno de {self.game.turn}: elige un mini-tablero libre'
        self.hint.color = theme.fade(theme.X_COLOR if self.game.turn == 'X' else theme.O_COLOR, 0.9)

    def _restart(self, *_):
        Clock.unschedule(self._cpu_turn)
        self.start(self.mode, self.level)

    def _go_menu(self, *_):
        Clock.unschedule(self._cpu_turn)
        if self.on_back:
            self.on_back()