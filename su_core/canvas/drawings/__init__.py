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
    "GreenYellow": pm.get_color("greenyellow"),
    "Green": pm.get_color("green"),
    "SeaGreen": pm.get_color("seagreen"),
    "TooltipGreen": pm.new_color(0, 252, 0, 255),
    # blueish colors
    "Navy": pm.get_color("navy"),
    "RoyalGreen": pm.get_color("royalblue"),
    "Blue": pm.get_color("blue"),
    "Cyan": pm.get_color("cyan"),
    "TooltipBlue": pm.new_color(110, 110, 255, 255),
    # brownish colors
    "D2RBrown": pm.new_color(199, 179, 119, 255),
    "SaddleBrown": pm.get_color("saddlebrown"),
    # redish colors
    "Red": pm.get_color("red"),
    "MediumVioletRed": pm.get_color("mediumvioletred"),
    "RedBackground": pm.new_color(139, 0, 0, 75),
    "InvBackground": pm.fade_color(pm.new_color(128, 64, 0, 255), 0.20),
    # yellowish colors
    "Yellow": pm.get_color("yellow"),
    "TooltipYellow": pm.new_color(255, 255, 100, 255),
    # orange-ish colors
    "Salmon": pm.get_color("salmon"),
    "Orange": pm.get_color("orange"),
    "TooltipOrange": pm.new_color(255, 168, 0, 255),
    # whitish colors
    "White": pm.get_color("white"),
    # blackish colors
    "Onyx": pm.new_color(53, 57, 53, 75),
    "TooltipBackground": pm.new_color(0, 0, 0, 215),
    "TooltipGray": pm.new_color(240, 240, 240, 100),
    # others
    "Gold": pm.get_color("gold"),
}
