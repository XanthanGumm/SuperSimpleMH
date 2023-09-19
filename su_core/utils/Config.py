import os
import toml
import pathlib
from su_core.utils.helpers import get_root


class Config:
    def __init__(self):
        root = get_root(__file__)
        self._cfg_path = os.path.join(root, "config")
        self._cfg_map_api_path = os.path.join(root, "rpyc-d2-map-api", "settings.toml")

        with open(os.path.join(self._cfg_path, "areas.toml"), "r") as f:
            self._areas = toml.load(f)

        with open(os.path.join(self._cfg_path, "directions.toml"), "r") as f:
            self._directions = toml.load(f)

        with open(os.path.join(self._cfg_path, "general.toml"), "r") as f:
            self._general = toml.load(f)

        with open(self._cfg_map_api_path, "r") as f:
            self._map_api = toml.load(f)

    def update_d2lod_path(self, path):
        self._map_api["diablo2"]["path"] = path
        with open(self._cfg_map_api_path, "w") as f:
            toml.dump(self._map_api, f)

    def save(self):
        with open(os.path.join(self._cfg_path, "areas.toml"), "w") as f:
            toml.dump(self._areas, f)

        with open(os.path.join(self._cfg_path, "directions.toml"), "w") as f:
            toml.dump(self._directions, f)

        with open(os.path.join(self._cfg_path, "general.toml"), "w") as f:
            toml.dump(self._general, f)

    @staticmethod
    def is_d2lod_path_is_valid(path) -> bool:
        if not os.path.exists(path):
            return False

        else:
            d2lod_dlls = [d for d in pathlib.Path(path).iterdir() if d.name.endswith(".dll")]
            if len(d2lod_dlls) != 22 or not os.path.isfile(os.path.join(path, "Game.exe")):
                return False

        return True

    @property
    def areas(self):
        return self._areas

    @property
    def directions(self):
        return self._directions

    @property
    def general(self):
        return self._general

    @property
    def map_api(self):
        return self._map_api