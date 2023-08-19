import rpyc
import pyMeow as pm
from cachetools import cached
from cachetools.keys import hashkey


class RPYClient:
    def __init__(self, port=18861):
        self._conn = rpyc.connect(
            "localhost",
            port=port,
            config={"sync_request": True, "sync_request_timeout": 60},
        )

        self._prev_seed = None
        self._prev_area = None

    @cached(cache={}, key=lambda self, area, player_position: hashkey(area))
    def read_map(self, area: int, player_position: tuple) -> dict:
        data = self._conn.root.read_map_data(area, player_position)
        return {
            "area": data["area"],
            "size": data["size"],
            "origin": data["origin"],
            "exits": data["exits"],
            "waypoint": data["waypoint"],
            "adjacent_levels": data["adjacent_levels"],
        }

    @cached(cache={}, key=lambda self, area: hashkey(area))
    def get_level_image(self, area: int) -> bytes:
        return self._conn.root.generate_map_image(area)

    @cached(cache={}, key=lambda self, area: hashkey(area))
    def get_level_texture(self, area: int):
        return pm.load_texture_bytes(".png", self.get_level_image(area))

    def set_requirements(self, seed: int, difficulty: int) -> None:
        self._prev_seed = seed
        self._conn.root.set_map_seed(seed)
        self._conn.root.set_difficulty(difficulty)

    def clear_cache(self) -> None:
        self.get_level_image.cache.clear()
        self.get_level_texture.cache.clear()
        self.read_map.cache.clear()
        self._prev_area = None

    @property
    def prev_seed(self):
        return self._prev_seed

    @property
    def prev_area(self):
        return self._prev_area

    @prev_area.setter
    def prev_area(self, area: int):
        self._prev_area = area
