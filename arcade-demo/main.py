"""
This program shows how to:
  * Have one or more instruction screens
  * Show a 'Game over' text and halt the game
  * Allow the user to restart the game

Make a separate class for each view (screen) in your game.
The class will inherit from arcade.View. The structure will
look like an arcade.Window as each view will need to have its own draw,
update and window event methods. To switch a view, simply create a view
with `view = MyView()` and then use the view.show() method.

This example shows how you can set data from one View on another View to pass data
around (see: time_taken), or you can store data on the Window object to share data between
all Views (see: total_score).

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.view_instructions_and_game_over.py

Modified by David F. Barrero
This file includes code from the following sources:
https://api.arcade.academy/en/latest/examples/view_instructions_and_game_over.html#view-instructions-and-game-over


"""

import arcade
import random
import os


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


WIDTH = 1250
HEIGHT = 730
SPRITE_SCALING = 0.5
collect_coin_sound = arcade.load_sound("/home/tomas/Downloads/Samsung notification sound effect ( no copyright).wav")

class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Albion Online es un mmorpg no lineal,  Explora un amplio mundo abierto con 5 biomas únicos, todo cuánto hagas tendrá su repercusión en el mundo, con la economía orientada al jugador de Albion, los jugadores crean prácticamente todo el equipo a partir de los recursos que consiguen, el equipo que llevas define quién eres, cambia de arma y armadura para pasar de caballero a mago, o juega como una mezcla de ambas clases. Aventúrate en el mundo abierto frente a los habitantes y las criaturas de Albion, inicia expediciones o adéntrate en mazmorras en las que encontrarás enemigos aún más difíciles, enfréntate a otros jugadores en encuentros en el mundo abierto, lucha por los territorios o por ciudades enteras en batallas tácticas, relájate en tu isla privada, donde podrás construir un hogar, cultivar cosechas y criar animales, únete a un gremio, todo es mejor cuando se trabaja en grupo. Adéntrate ya en el mundo de Albion y escribe tu propia historia. ", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("en el que escribes tu propia historia sin limitarte a seguir un camino prefijado.", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.time_taken = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(5):

            # Create the coin instance
            coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING / 3)

            # Position the coin
            coin.center_x = random.randrange(WIDTH)
            coin.center_y = random.randrange(HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

    def on_draw(self):
        arcade.start_render()
        # Draw all the sprites.
        self.player_list.draw()
        self.coin_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 30, arcade.color.WHITE, 14)
        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        self.time_taken += delta_time

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        self.player_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the
        # score.
        for coin in hit_list:
            arcade.play_sound(collect_coin_sound)
            coin.kill()
            self.score += 1
            self.window.total_score += 1


        # If we've collected all the games, then move to a "GAME_OVER"
        # state.
        if len(self.coin_list) == 0:
            arcade.play_sound(arcade.load_sound("/home/tomas/Downloads/Clash Royale 'He He He Haw' Sound Effect [Original Audio] MEME SOUND EFFECT.wav"))
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

    def on_mouse_motion(self, x, y, _dx, _dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         WIDTH / 2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Different Views Example")
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()