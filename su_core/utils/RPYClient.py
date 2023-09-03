import rpyc


class RPYClient:
    def __init__(self, port=18861):
        self._conn = rpyc.connect(
            "localhost",
            port=port,
        )

        self._async_read_map_data = rpyc.async_(self._conn.root.read_map_data)
        self._async_read_map_grid = rpyc.async_(self._conn.root.read_map_grid)

    def read_map_data(self, area, player_position=None):
        return self._async_read_map_data(area, player_position)

    def read_map_grid(self, area):
        return self._async_read_map_grid(area)

    def set_requirements(self, seed: int, difficulty: int) -> None:
        self._conn.root.set_map_seed(seed)
        self._conn.root.set_difficulty(difficulty)


