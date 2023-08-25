try:
    import pyMeow as pm

except ModuleNotFoundError:
    # from su_core.utils.helpers import get_root
    import sys
    import os
    import pathlib

    root = pathlib.Path(__file__)
    while root.name != "SuperSimpleMH":
        root = root.parent

    # root = get_root(__file__)
    sys.path.insert(0, os.path.join(root, "dep"))
