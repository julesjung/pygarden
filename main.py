import arcade
import pyglet

from utils import BASE_ASSETS_DIR
from views.main_menu import MainMenuView

pyglet.options.dpi_scaling = "stretch"
pyglet.resource.path = ["assets"]
pyglet.resource.reindex()

arcade.resources.add_resource_handle("assets", BASE_ASSETS_DIR / "assets")
arcade.load_font(":assets:fonts/dohyeon-regular.ttf")


def main():
    window = arcade.Window(1024, 768, "PyGarden")
    window.set_icon(pyglet.resource.image("icon.png").get_image_data())

    window.show_view(MainMenuView())

    arcade.run()


if __name__ == "__main__":
    main()
