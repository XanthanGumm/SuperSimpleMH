import concurrent.futures
import io
import os
import pickle
import time
import tomllib
import cv2
import numpy as np
from su_core.logger import manager
from su_core.canvas.drawings.ProgressBar import ProgressBar, pm
from su_core.pyTypes.unitTypes import Menu
from su_core.utils import RPYClient
from su_core.utils.data_structures import RequestsBatch, TexturesBatch, AsyncResult
from su_core.utils.helpers import get_root

# from typing - learn how to add type hints


class MapManager:
    def __init__(self, texture_scalar: float):
        # root = get_root(__file__)
        #
        # # load levels textures config priority
        # with open(os.path.join(root, "config", "levels_priority.toml"), "rb") as f:
        #     self._levels_priority = tomllib.load(f)

        self._logger = manager.get_logger(__name__)
        
        self._texture_scalar: float= texture_scalar
        self._rpyc_client: RPYClient = RPYClient()
        self._pool = None
        self._game_difficulty: int = -1
        self._game_seed: int = -1
        self._player_area: int = -1
        self._acts_levels: list[range] = [range(1, 40), range(40, 75), range(75, 103), range(103, 109), range(109, 132)]

        # vars for download each act
        self._timer_begin: int = 0
        self._timer_end: int = 0
        self._acts_to_process: dict = dict()
        self._acts_processed: set = set()
        self._requests_batch: RequestsBatch = RequestsBatch()
        self._textures_batch: TexturesBatch = TexturesBatch()
        self._level_data = dict()
        self._textures = dict()
        self._game_ui: Menu = Menu()
        self._progress_bar: ProgressBar = ProgressBar()

    def initialize(self, seed: int, difficulty: int) -> None:
        self._logger.info(
            f"[!] Initialize MapManager with seed: {hex(seed)}, at {'normal' if difficulty == 0 else 'nightmare' if difficulty == 1 else 'hell'} difficulty"
        )

        self._player_area: int = -1
        self._game_difficulty: int = difficulty
        self._game_seed: int = seed
        self._rpyc_client.set_requirements(seed, difficulty)
        self._acts_processed: set = set()
        for index, levels in enumerate(self._acts_levels):
            self._acts_to_process[index] = self._acts_levels[index]
        self.clear()

    # TODO: add in town npc labels
    # TODO: add act levels config loader
    # TODO: add waypoints, maze and outdoor, stash
    # TODO: fix act 1 town/bloodmoor
    # process each act
    def update(self, area: int, player_pos: tuple[float, float]):
        progress_value: int = 0
        progress_max_value: int = 0

        self._read_level_data(area, player_pos)

        if self._game_ui.last_act is not None:
            # player changed act in the middle of loading maps
            if (
                self._game_ui.last_act not in self._acts_to_process
                and self._game_ui.last_act not in self._acts_processed
            ):
                self._logger.info(
                    f"[!] Player switched from Act{self.act_number} at the middle of processing Act{self._game_ui.last_act + 1} maps."
                )
                self._logger.info(f"[!] Waiting for Act{self._game_ui.last_act + 1} maps requests to finish..")
                self._logger.warning(f"[!] Canceling the process of up scaling Act{self._game_ui.last_act + 1} maps...")

                # fix progress bar when player changing act while loading
                progress_value = self._progress_bar.value
                progress_max_value = 2 * len(self._acts_levels[self._game_ui.last_act]) + progress_value

                # close the pool and add the previous act to the process list
                self._pool.shutdown(wait=False, cancel_futures=True)
                self._acts_to_process[self._game_ui.last_act] = self._acts_levels[self._game_ui.last_act]

        if self.act_number in self._acts_to_process:
            progress_value += progress_value
            progress_max_value += 2 * len(self._acts_levels[self.act_number]) - 1
            self._progress_bar.initialize_bar(start_value=progress_value, max_value=progress_max_value)
            self._timer_begin = time.perf_counter()

            self._pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 2)
            self._textures_batch.clear()
            self._request_current_act_maps()

        if not self._textures_batch.is_processed:
            if self._requests_batch.ready() and self._textures_batch.ready():
                self._pool.shutdown()
                self._load_textures()
                self._acts_processed.add(self.act_number)
                self._textures_batch.is_processed = True
                self._requests_batch.clear()
                self._timer_end = time.perf_counter()
                self._logger.info(
                    f"[!] Finished to load Act{self.act_number + 1} map levels after: {self._timer_end - self._timer_begin} seconds"
                )

        if self.act_number not in self._acts_processed:
            self._progress_bar.draw()

    def _read_level_data(self, area: int, player_pos: tuple[float, float]) -> None:
        self._player_area = area

        if area not in self._level_data:
            self._logger.info(f"[!] Requesting area data for area: {area}...")

            self._level_data[area] = self._rpyc_client.get_level_data(area, player_pos)

    def get_level_data(self):
        if isinstance(self._level_data[self._player_area], AsyncResult):
            self._logger.info(f"[!] Caching area data for area: {self._player_area}...")

            self._level_data[self._player_area] = dict(self._level_data[self._player_area].value)
        return self._level_data[self._player_area]

    def _request_current_act_maps(self):
        self._logger.info(f"[!] Requesting Act{self.act_number + 1} map levels grids...")

        areas = self._acts_to_process.pop(self.act_number)
        for area in areas:
            req = self._rpyc_client.get_level_map(area)
            req.add_callback(self._on_map_grid_arrival)
            self._requests_batch.insert_data(req, area)

    def read_game_ui(self) -> None:
        self._game_ui.update()

    def _on_map_grid_arrival(self, req):
        area = self._requests_batch.get_data(req)
        texture_bytes = req.value
        job = self._pool.submit(self._process_map_texture, texture_bytes, self._texture_scalar, 7)
        job.add_done_callback(self._progress_bar.update)
        self._textures_batch.insert_data(area, job)
        self._progress_bar.update()

    @staticmethod
    def _process_map_texture(pickled_map, scalar: float, ksize: int) -> bytes:
        level_map_bytes, h, w = pickle.loads(pickled_map)
        level_map = np.frombuffer(level_map_bytes, np.int32).reshape(h, w)

        level_map_invert = np.copy(level_map)
        level_map_invert[level_map_invert == -1] = 255

        level_map = np.where((level_map == -1) | (level_map % 2 != 0), 0, 255).astype(np.uint8)

        height, width = level_map.shape[:2]
        offset = int(height)

        def cart_to_iso(indices):
            xs = indices[:, 1] - indices[:, 0] + offset
            ys = (indices[:, 1] + indices[:, 0]) // 2
            return np.array([ys, xs])

        level_map_invert_indices = np.argwhere(level_map_invert != 255)
        orthoX_invert_indices = level_map_invert_indices[:, 1]
        orthoY_invert_indices = level_map_invert_indices[:, 0]
        level_map_invert_iso_y, level_map_invert_iso_x = cart_to_iso(level_map_invert_indices)
        level_map_invert_iso = np.ones(((height + width) // 2, width + height)).astype(np.uint8) * 255
        level_map_invert_iso[level_map_invert_iso_y, level_map_invert_iso_x] = level_map_invert[
            orthoY_invert_indices, orthoX_invert_indices
        ]

        level_map_binary = cv2.bitwise_not(np.where(level_map_invert_iso % 2 != 0, 255, level_map_invert_iso))

        level_map_indices = np.argwhere(level_map != 255)
        orthoX_indices = level_map_indices[:, 1]
        orthoY_indices = level_map_indices[:, 0]
        level_map_iso_y, level_map_iso_x = cart_to_iso(level_map_indices)
        level_map_iso = np.ones(((height + width) // 2, width + height)).astype(np.uint8) * 255
        level_map_iso[level_map_iso_y, level_map_iso_x] = level_map[orthoY_indices, orthoX_indices]

        h_invert, w_invert = level_map_binary.shape[:2]
        cnts_invert, hierarchy_invert = cv2.findContours(level_map_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        level_map_cnts_invert = np.ones((h_invert, w_invert)).astype(np.uint8) * 255
        cv2.drawContours(level_map_cnts_invert, cnts_invert, -1, (0, 255, 0), cv2.FILLED)

        h, w = level_map_iso.shape[:2]
        cnts, hierarchy = cv2.findContours(level_map_iso, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        level_map_cnts = np.ones((h, w)).astype(np.uint8) * 255
        cv2.drawContours(level_map_cnts, cnts, -1, (0, 255, 0), 1)

        cnts_mask = level_map_cnts_invert == 0
        level_map_cnts[~cnts_mask] = 255

        level_map_iso_brga = cv2.cvtColor(level_map_cnts, cv2.COLOR_BGR2BGRA)
        level_map_iso_brga[0, :] = [255, 255, 255, 0]
        Bmask = np.all(level_map_iso_brga == [0, 0, 0, 255], axis=-1)
        Wmask = np.all(level_map_iso_brga == [255, 255, 255, 255], axis=-1)

        level_map_iso_brga[Bmask] = [127, 127, 127, 127]
        level_map_iso_brga[Wmask] = [255, 255, 255, 0]

        h, w = level_map_iso_brga.shape[:2]

        level_map_iso_brga = cv2.resize(
            level_map_iso_brga,
            (int(w * scalar), int(h * scalar)),
            interpolation=cv2.INTER_CUBIC,
        )

        level_map_iso_brga = cv2.GaussianBlur(level_map_iso_brga, (3, 3), 0)
        level_map_iso_brga = cv2.medianBlur(level_map_iso_brga, ksize=ksize)

        _, buffer = cv2.imencode(".png", level_map_iso_brga)
        texture_byte_arr = io.BytesIO(buffer)

        return bytes(texture_byte_arr.getbuffer())

    def _load_textures(self) -> None:
        self._logger.info(f"[!] Loading Act{self.act_number + 1} textures...")

        data = self._textures_batch.extract_all()
        for area, texture in data.items():
            self._textures[area] = pm.load_texture_bytes(".png", texture)

    def get_map(self, area):
        return self._textures[area]

    def is_new_game(self, seed):
        return seed != self._game_seed

    def is_new_area(self, area):
        return area != self._player_area and area in self._level_data

    def clear(self):
        self._logger.info("[!] Clearing MapManager' levels textures and data cache...")
        self._logger.info("[!] Unloading textures from memory...")

        areas = list(self._textures.keys())
        for area in areas:
            texture = self._textures.pop(area)
            pm.unload_texture(texture)

        self._level_data.clear()

    @property
    def loading_area(self) -> bool:
        if self._game_ui is None:
            raise TypeError("Game UI is not initialized")
        return self._game_ui.is_loading_area

    @property
    def in_game(self) -> bool:
        if self._game_ui is None:
            raise TypeError("Game UI is not initialized")
        return self._game_ui.is_game_active

    @property
    def textures(self):
        return self._textures

    @property
    def is_panel_open(self):
        return self._game_ui.is_open

    @property
    def level_data(self):
        return self._level_data

    @level_data.setter
    def level_data(self, data):
        self._level_data = data

    @property
    def act_number(self) -> int:
        if self._game_ui is None:
            raise TypeError("Game UI is not initialized")
        return self._game_ui.act_number

    @property
    def acts_processed(self):
        return self._acts_processed
