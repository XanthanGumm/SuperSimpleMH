import pyMeow as pm
from cachetools import cached
from cachetools.keys import hashkey


class Colors:
    Green = pm.get_color("green")
    SeaGreen = pm.get_color("seagreen"),
    GreenYellow = pm.get_color("greenyellow")
    D2RGreen = pm.new_color(0, 252, 0, 255)
    GreenBackground = pm.fade_color(pm.new_color(0, 252, 0, 255), 0.25)
    Blue = pm.get_color("blue")
    RoyalBlue = pm.get_color("royalblue")
    Cyan = pm.get_color("cyan")
    Navy = pm.get_color("navy")
    D2RBlue = pm.new_color(110, 110, 255, 255)
    SaddleBrown = pm.get_color("saddlebrown")
    D2RBrown = pm.new_color(199, 179, 119, 255)
    Red = pm.get_color("red")
    MediumVioletRed = pm.get_color("mediumvioletred")
    RedBackground = pm.new_color(139, 0, 0, 75)
    RedInvBackground = pm.fade_color(pm.new_color(128, 64, 0, 255), 0.20)
    Yellow = pm.get_color("yellow")
    D2RYellow = pm.new_color(255, 255, 100, 255)
    Salmon = pm.get_color("salmon")
    Orange = pm.get_color("orange")
    D2ROrange = pm.new_color(255, 168, 0, 255)
    White = pm.get_color("white")
    D2RBlackBackground = pm.new_color(0, 0, 0, 215)
    D2RGray = pm.new_color(240, 240, 240, 100)
    Gold = pm.get_color("gold")

    @classmethod
    @cached(cache={}, key=lambda cls, name, alpha: hashkey(name, alpha))
    def Fade(cls, name: str, alpha: float):
        color = cls.Get(name)
        faded = pm.fade_color(color, alpha)
        return faded

    @staticmethod
    def Get(name: str):
        return getattr(Colors, name)


# pm_colors = {
#     # greenish colors
#     "GreenYellow": pm.get_color("greenyellow"),
#     "Green": pm.get_color("green"),
#     "SeaGreen": pm.get_color("seagreen"),
#     "TooltipGreen": pm.new_color(0, 252, 0, 255),
#     "GreenBackground": pm.fade_color(pm.new_color(0, 252, 0, 255), 0.25),
#     # blueish colors
#     "Navy": pm.get_color("navy"),
#     "RoyalGreen": pm.get_color("royalblue"),
#     "Blue": pm.get_color("blue"),
#     "Cyan": pm.get_color("cyan"),
#     "TooltipBlue": pm.new_color(110, 110, 255, 255),
#     # brownish colors
#     "D2RBrown": pm.new_color(199, 179, 119, 255),
#     "SaddleBrown": pm.get_color("saddlebrown"),
#     # redish colors
#     "Red": pm.get_color("red"),
#     "MediumVioletRed": pm.get_color("mediumvioletred"),
#     "RedBackground": pm.new_color(139, 0, 0, 75),
#     "InvBackground": pm.fade_color(pm.new_color(128, 64, 0, 255), 0.20),
#     # yellowish colors
#     "Yellow": pm.get_color("yellow"),
#     "TooltipYellow": pm.new_color(255, 255, 100, 255),
#     # orange-ish colors
#     "Salmon": pm.get_color("salmon"),
#     "Orange": pm.get_color("orange"),
#     "TooltipOrange": pm.new_color(255, 168, 0, 255),
#     # whitish colors
#     "White": pm.get_color("white"),
#     # blackish colors
#     "Onyx": pm.new_color(53, 57, 53, 75),
#     "TooltipBackground": pm.new_color(0, 0, 0, 215),
#     "TooltipGray": pm.new_color(240, 240, 240, 100),
#     # others
#     "Gold": pm.get_color("gold"),
# }
