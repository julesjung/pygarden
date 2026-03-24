from pyglet.graphics import Batch, Group
from pyglet.shapes import Rectangle
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import Window

from resources import load_image, load_spritesheet
from utils.scissor import ScissorGroup

AVAILABLE_TREES = [
    "Tree 0",
    "Tree 1",
    "Tree 2",
    "Tree 3",
    "Tree 4",
    "Tree 5",
    "Tree 6",
    "Tree 7",
    "Tree 8",
    "Tree 9",
    "Tree 10",
    "Tree 11",
    "Tree 12",
    "Tree 13",
    "Tree 14",
    "Tree 15",
]


class ShopView:
    def __init__(self, window: Window):
        super().__init__()

        self.window = window

        self.background_batch = Batch()
        self.overlay = Rectangle(
            0,
            0,
            1024,
            768,
            color=(0, 0, 0),
            batch=self.background_batch,
            group=Group(-1),
        )
        self.overlay.opacity = 192
        self.background = Sprite(
            load_image("shop/background.png"),
            batch=self.background_batch,
            group=Group(order=0),
        )

        self.batch = Batch()
        self.tree_preview = Sprite(
            load_spritesheet("plants/tree.png", 1, 3)[2], x=640, y=92, batch=self.batch
        )

        self.leaf_count = 0
        self.leaf_count_text = Label(
            f"{self.leaf_count:.2e}",
            464,
            552,
            anchor_x="right",
            anchor_y="center",
            font_name="Do Hyeon",
            font_size=26,
            batch=self.batch,
        )

        self.list_scissor = ScissorGroup(114, 89, 382, 387)

        self.list_items: list[Sprite | Label] = []

        for index, tree_name in enumerate(AVAILABLE_TREES):
            frame = Sprite(
                load_image("shop/frame.png"),
                x=128,
                y=412 - index * 64,
                batch=self.batch,
                group=self.list_scissor,
            )
            label = Label(
                tree_name,
                x=144,
                y=436 - index * 64,
                anchor_x="left",
                anchor_y="center",
                font_name="Do Hyeon",
                font_size=16,
                batch=self.batch,
                group=self.list_scissor,
            )
            self.list_items.append(frame)
            self.list_items.append(label)

    def draw(self):
        self.background_batch.draw()
        self.batch.draw()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        for list_item in self.list_items:
            list_item.y -= scroll_y * 16
