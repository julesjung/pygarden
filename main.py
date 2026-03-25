import arcade
import pyglet

from views.main_menu import MainMenuView

pyglet.options.dpi_scaling = "stretch"

arcade.load_font("assets/fonts/dohyeon-regular.ttf")


def main():
    window = arcade.Window(1024, 768, "PyGarden")
    window.set_icon(pyglet.image.load("assets/icon.png").get_image_data())

    window.show_view(MainMenuView())

    arcade.run()


if __name__ == "__main__":
    main()
