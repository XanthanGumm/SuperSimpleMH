import os
import pathlib
import pyMeow as pm


root = pathlib.Path(__file__)
while root.name != "SuperSimpleMH":
    root = root.parent

# load fonts
# pm.load_font(os.path.join(root, "fonts", "formal436bt-regular.otf"), 1)

# fonts = {
#     "formal": 1
# }

pm_colors = {
    # greenish colors
    "greenyellow": pm.get_color("greenyellow"),
    "green": pm.get_color("green"),
    "seagreen": pm.get_color("seagreen"),

    # blueish colors
    "navy": pm.get_color("navy"),
    "royalblue": pm.get_color("royalblue"),
    "blue": pm.get_color("blue"),
    "cyan": pm.get_color("cyan"),

    # brownish colors
    "d2rbrown": pm.new_color(199, 179, 119, 255),

    # redish colors
    "red": pm.get_color("red"),
    "mediumvioletred": pm.get_color("mediumvioletred"),
    "redbackground":  pm.new_color(139, 0, 0, 75),

    # yellowish colors
    "yellow": pm.get_color("yellow"),

    # orangeish colors
    "salmon": pm.get_color("salmon"),
    "orange": pm.get_color("orange"),

    # whiteish colors
    "white": pm.get_color("white"),

    # others
    "gold": pm.get_color("gold")
}
