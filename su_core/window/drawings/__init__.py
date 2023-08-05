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
    "tooltipgreen": pm.new_color(0, 252, 0, 255),

    # blueish colors
    "navy": pm.get_color("navy"),
    "royalblue": pm.get_color("royalblue"),
    "blue": pm.get_color("blue"),
    "cyan": pm.get_color("cyan"),
    "tooltipblue": pm.new_color(110, 110, 255, 255),

    # brownish colors
    "d2rbrown": pm.new_color(199, 179, 119, 255),
    "saddlebrown": pm.get_color("saddlebrown"),

    # redish colors
    "red": pm.get_color("red"),
    "mediumvioletred": pm.get_color("mediumvioletred"),
    "redbackground":  pm.new_color(139, 0, 0, 75),
    "invbackground": pm.fade_color(pm.new_color(128, 64, 0, 255), 0.15),

    # yellowish colors
    "yellow": pm.get_color("yellow"),
    "tooltipyellow": pm.new_color(255, 255, 100, 255),

    # orangeish colors
    "salmon": pm.get_color("salmon"),
    "orange": pm.get_color("orange"),
    "tooltiporange": pm.new_color(255, 168, 0, 255),

    # whiteish colors
    "white": pm.get_color("white"),

    # blackish colors
    "onyx": pm.new_color(53, 57, 53, 75),
    "tooltipbackground": pm.new_color(0, 0, 0, 215),
    "tooltipgray": pm.new_color(240, 240, 240, 100),

    # others
    "gold": pm.get_color("gold")
}
