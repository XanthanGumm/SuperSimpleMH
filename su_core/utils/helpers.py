import pathlib


def get_root(file_name: str):
    root = pathlib.Path(file_name)
    while root.name != "SuperSimpleMH":
        root = root.parent
    return root


def get_last_key(d: dict):
    return next(iter(d[-1].keys()))


def get_last_val(d: dict):
    return next(iter(d[-1].values()))
