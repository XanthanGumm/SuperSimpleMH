try:
    import pyMeow as pm

except ModuleNotFoundError:
    from su_core.utils.helpers import get_root
    import sys
    import os

    root = get_root(__file__)
    sys.path.insert(0, os.path.join(root, "dep"))
