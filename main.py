import arcade
import pyglet

from views.main_menu import MainMenuView

pyglet.options.dpi_scaling = "stretch"

pyglet.resource.path = ["assets"]
pyglet.resource.reindex()


def main():
    window = arcade.Window(1024, 768, "PyGarden")
    window.set_icon(pyglet.resource.image("icon.png").get_image_data())

    window.show_view(MainMenuView())

    arcade.run()


if __name__ == "__main__":
    main()
