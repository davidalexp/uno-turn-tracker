from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Rotate, PushMatrix, PopMatrix, Color, Rectangle
import os


class RotatingImage(Image):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self.rotation = Rotate(angle=self.angle, origin=self.center)
        with self.canvas.after:
            PopMatrix()

        self.bind(pos=self.update_origin, size=self.update_origin, angle=self.update_rotation)

    def update_origin(self, *args):
        self.rotation.origin = self.center

    def update_rotation(self, *args):
        self.rotation.angle = self.angle


class UnoTurnTracker(App):
    def build(self):
        self.players = []
        self.current_index = 0
        self.direction = 1
        self.arrow_animation = None
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.name_input = TextInput(hint_text='Digite o nome do jogador', multiline=False, size_hint=(0.8, 1), font_size=20)
        self.add_button = Button(text="Adicionar Jogador", size_hint=(0.2, 1))
        self.add_button.bind(on_press=self.add_player)

        self.input_layout.add_widget(self.name_input)
        self.input_layout.add_widget(self.add_button)

        self.main_layout.add_widget(self.input_layout)

        self.start_button = Button(text='Iniciar Jogo', size_hint=(1, 0.1))
        self.start_button.bind(on_press=self.start_game)
        self.main_layout.add_widget(self.start_button)

        return self.main_layout

    def add_player(self, instance):
        player_name = self.name_input.text.strip()
        if player_name:
            self.players.append(player_name)
            self.name_input.text = ''

    def start_game(self, instance):
        if len(self.players) < 2:
            return

        self.main_layout.clear_widgets()
        self.setup_game_ui()

    def setup_game_ui(self):
        self.turn_label = Label(text=f"Turno de: {self.players[self.current_index]}", font_size=30)
        self.direction_label = Label(text="Sentido: Horário", font_size=20)

        self.arrow_image = RotatingImage(source='arrow.png', size_hint=(1, 0.6))

        self.main_layout.add_widget(self.arrow_image)
        self.main_layout.add_widget(self.turn_label)
        self.main_layout.add_widget(self.direction_label)

        self.buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))

        self.next_button = Button(text="Próximo", size_hint=(0.4, 1))
        self.next_button.bind(on_press=self.next_turn)
        self.buttons_layout.add_widget(self.next_button)

        self.reverse_button = Button(text="Inverter Sentido", size_hint=(0.4, 1))
        self.reverse_button.bind(on_press=self.reverse_direction)
        self.buttons_layout.add_widget(self.reverse_button)

        self.reset_button = Button(text="Novo Jogo", size_hint=(0.2, 1))
        self.reset_button.bind(on_press=self.reset_game)
        self.buttons_layout.add_widget(self.reset_button)

        self.main_layout.add_widget(self.buttons_layout)

        self.animate_arrow()

    def next_turn(self, instance):
        self.current_index = (self.current_index + self.direction) % len(self.players)
        self.turn_label.text = f"Turno de: {self.players[self.current_index]}"
        self.animate_arrow()

    def reverse_direction(self, instance):
        self.direction *= -1
        direction_text = "Horário" if self.direction == 1 else "Anti-Horário"
        self.direction_label.text = f"Sentido: {direction_text}"
        self.animate_arrow()

    def reset_game(self, instance):
        self.players = []
        self.current_index = 0
        self.direction = 1
        self.main_layout.clear_widgets()
        self.build()

    def animate_arrow(self):
        if self.arrow_animation:
            self.arrow_animation.stop(self.arrow_image)
        self.arrow_image.angle = 0
        self.arrow_animation = Animation(angle=360 if self.direction == 1 else -360, duration=5)
        self.arrow_animation.repeat = True
        self.arrow_animation.start(self.arrow_image)


if __name__ == "__main__":
    UnoTurnTracker().run()