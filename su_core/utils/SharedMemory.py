import multiprocessing as mp


class SharedMemory:
    def __init__(self, manager: mp.Manager, cfg):
        # data to receive
        self.act: mp.Value = mp.Value("i", -1)
        self.area: mp.Value = mp.Value("i", 0)
        # data to pass
        self.overlay_opacity: mp.Value = mp.Value("f", (10 - cfg.general["properties"]["overlay_opacity"]) * 0.1)
        self.directions_opacity: mp.Value = mp.Value("f", (10 - cfg.general["properties"]["directions_opacity"]) * 0.1)
        self.npcs_opacity: mp.Value = mp.Value("f", (10 - cfg.general["properties"]["npcs_opacity"]) * 0.1)
        self.quality: mp.Array = mp.Array("c", b"Medium")
        self.quality.value = bytes(cfg.general["properties"]["quality"], "utf8")
        self.acts_levels: mp.Manager.dict = manager.dict(cfg.areas)
        self.directions: mp.Manager.dict = manager.dict()
        self.overlay = mp.Value("i", cfg.general["properties"]["draw_overlay"])
        self.monsters = mp.Value("i", cfg.general["properties"]["draw_monsters"])
        self.uniques = mp.Value("i", cfg.general["properties"]["draw_uniques"])
        self.merc = mp.Value("i", cfg.general["properties"]["draw_merc"])
        # events
        self.on_path_validator = mp.Event()
        self.on_area_change = mp.Event()
        self.on_quality_change = mp.Event()
        self.on_directions_change = mp.Event()
        self.shut_down = mp.Event()
