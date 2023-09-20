import concurrent.futures
import io
import os
import pickle
import time
import cv2
import numpy as np
from su_core.logging.Logger import Logger
from su_core.canvas.drawings.ProgressBar import ProgressBar, pm
from su_core.pyTypes.unit_types import Menu
from su_core.utils import RPYClient
from su_core.utils.data_structures import RequestsBatch, TexturesBatch, AsyncResult

# from typing - learn how to add type hints


class MapManager:
    def __init__(self, texture_scalar: float):

        self._logger = Logger.get_logger(__name__)
        self._texture_scalar: float = texture_scalar
        self._quality: bytes | None = None
        self._ksize: int | None = None

        self._rpyc_client: RPYClient = RPYClient()
        self._pool = None
        self._game_difficulty: int = -1
        self._game_seed: int = -1
        self._player_area: int = -1
        self._workers = os.cpu_count() - 2

        self._timer_begin: int = 0
        self._timer_end: int = 0
        self._acts_levels: list[range] = [range(1, 40), range(40, 75), range(75, 103), range(103, 109), range(109, 132)]
        self._requests: dict = {0: dict(), 1: dict(), 2: dict(), 3: dict(), 4: dict()}
        self._acts_to_process: dict = {b"Low": dict(), b"Medium": dict(), b"High": dict()}
        self._acts_processed: dict = {b"Low": set(), b"Medium": set(), b"High": set()}
        self._textures: dict = {b"Low": dict(), b"Medium": dict(), b"High": dict()}
        self._level_data = dict()
        self._requests_batch: RequestsBatch = RequestsBatch()
        self._textures_batch: TexturesBatch = TexturesBatch()

        self._game_ui: Menu = Menu()
        self._progress_bar: ProgressBar = ProgressBar()

    def initialize(self, seed: int, difficulty: int, act_levels: list) -> None:
        self._logger.info(
            f"[!] Initialize MapManager with seed: {hex(seed)},"
            f" at {'normal' if difficulty == 0 else 'nightmare' if difficulty == 1 else 'hell'} difficulty"
        )

        self._player_area: int = -1
        self._game_difficulty: int = difficulty
        self._game_seed: int = seed
        self._acts_levels = act_levels
        self._rpyc_client.set_requirements(seed, difficulty)
        self.set_texture_quality(self._texture_scalar)

        for quality in [b"Low", b"Medium", b"High"]:
            self._acts_to_process[quality].clear()
            self._acts_processed[quality].clear()

            for index, levels in enumerate(self._acts_levels):
                self._acts_to_process[quality][index] = self._acts_levels[index]

        self.clear()

    # TODO: add waypoints, maze and outdoor, stash
    # TODO: fix act 1 town/bloodmoor
    # process each act
    def update(self, area: int, player_pos: tuple[float, float]):
        progress_value: int = 0
        progress_max_value: int = 0

        # read level data
        self._player_area: int = area
        if area not in self._level_data:
            self._logger.info(f"[!] Requesting area data for area: {area}")
            self._level_data[area] = self._rpyc_client.get_level_data(area, player_pos)

        if self._game_ui.last_act is not None:
            # player changed act in the middle of loading maps
            if (
                self._game_ui.last_act not in self._acts_to_process[self._quality]
                and self._game_ui.last_act not in self._acts_processed[self._quality]
            ):
                self._logger.info(
                    f"[!] Player switched from Act{self.act_number} at"
                    f" the middle of processing Act{self._game_ui.last_act + 1} maps"
                )
                self._logger.info(f"[!] Waiting for Act{self._game_ui.last_act + 1} maps requests to finish")
                self._logger.warning(f"[!] Canceling the process of up scaling Act{self._game_ui.last_act + 1} maps")

                # fix progress bar when player changing act while loading
                progress_value = self._progress_bar.value
                progress_max_value = 2 * len(self._acts_levels[self._game_ui.last_act]) + progress_value

                # close the pool and add the previous act to the process list
                self._pool.shutdown(wait=False, cancel_futures=True)
                self._acts_to_process[self._quality][self._game_ui.last_act] = self._acts_levels[self._game_ui.last_act]

        # initialize process textures dependencies
        if self.act_number in self._acts_to_process[self._quality]:
            progress_value += progress_value
            progress_max_value += 2 * len(self._acts_levels[self.act_number]) - 1
            self._progress_bar.initialize_bar(start_value=progress_value, max_value=progress_max_value)
            self._timer_begin = time.perf_counter()
            self._pool = concurrent.futures.ThreadPoolExecutor(max_workers=self._workers)
            self._textures_batch.clear()

            areas = self._acts_to_process[self._quality].pop(self.act_number)

            # request act maps
            if not self._requests[self.act_number]:
                self._logger.info(f"[!] Requesting Act{self.act_number + 1} map levels grids")
                for area in areas:
                    req = self._rpyc_client.get_level_map(area)
                    req.add_callback(self._on_map_grid_arrival)
                    self._requests_batch.insert_data(req, area)
            else:
                for area in areas:
                    self._submit_process_job(area, self._requests[self.act_number][area])

        # upscale textures quality
        if not self._textures_batch.is_processed:
            if self._requests_batch.ready() and self._textures_batch.ready():
                self._logger.info(f"[!] Loading Act{self.act_number + 1} textures")

                self._pool.shutdown()
                # load textures to memory
                data = self._textures_batch.extract_all()
                for area, texture in data.items():
                    self._textures[self._quality][area] = pm.load_texture_bytes(".png", texture)

                self._acts_processed[self._quality].add(self.act_number)
                self._textures_batch.is_processed = True
                self._requests_batch.clear()
                self._timer_end = time.perf_counter()
                self._logger.info(
                    f"[!] Finished to load Act{self.act_number + 1} map levels after: "
                    f"{self._timer_end - self._timer_begin} seconds"
                )

        if self.act_number not in self._acts_processed[self._quality]:
            self._progress_bar.draw()

    def get_level_data(self):
        if isinstance(self._level_data[self._player_area], AsyncResult):
            self._logger.info(f"[!] Caching area data for area: {self._player_area}")

            self._level_data[self._player_area] = dict(self._level_data[self._player_area].value)
        return self._level_data[self._player_area]

    def read_game_ui(self) -> None:
        self._game_ui.update()

    def get_map(self, area):
        if area not in self._textures[self._quality]:
            return None

        return self._textures[self._quality][area]

    def is_new_game(self, seed) -> bool:
        return seed != self._game_seed

    def is_new_area(self, area) -> bool:
        return area != self._player_area

    def set_texture_quality(self, texture_scalar) -> None:
        self._texture_scalar = texture_scalar
        self._quality = b"Low" if texture_scalar == 1.0 else b"Medium" if texture_scalar == 2.4 else b"High"

        if texture_scalar == 1:
            self._ksize = 0
        elif 1 < texture_scalar <= 2.4:
            self._ksize = 5
        elif 2.4 < texture_scalar <= 3.6:
            self._ksize = 7
        elif 3.6 < texture_scalar <= 4.8:
            self._ksize = 9
        else:
            self._ksize = 11

    def _on_map_grid_arrival(self, req):
        area = self._requests_batch.get_data(req)
        texture_bytes = req.value
        self._requests[self.act_number][area] = texture_bytes
        self._submit_process_job(area, texture_bytes)

    def _submit_process_job(self, area: int, texture_bytes: bytes):
        job = self._pool.submit(self._process_map_texture, texture_bytes, self._texture_scalar, self._ksize)
        job.add_done_callback(self._progress_bar.update)
        self._textures_batch.insert_data(area, job)
        self._progress_bar.update()

    def clear(self):
        for _, textures in self._textures.items():
            for _, texture in textures.items():
                pm.unload_texture(texture)
            textures.clear()

        for act in [0, 1, 2, 3, 4]:
            self._requests[act].clear()

        self._level_data.clear()

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

        Wmask = np.all(level_map_iso_brga == [255, 255, 255, 255], axis=-1)
        level_map_iso_brga[Wmask] = [255, 255, 255, 0]

        if not ksize:
            Bmask = np.all(level_map_iso_brga == [0, 0, 0, 255], axis=-1)
            level_map_iso_brga[Bmask] = [127, 127, 127, 127]

        h, w = level_map_iso_brga.shape[:2]

        level_map_iso_brga = cv2.resize(
            level_map_iso_brga,
            (int(w * scalar), int(h * scalar)),
            interpolation=cv2.INTER_CUBIC,
        )

        if ksize:
            level_map_iso_brga = cv2.GaussianBlur(level_map_iso_brga, (3, 3), 0)
            level_map_iso_brga = cv2.medianBlur(level_map_iso_brga, ksize=ksize)

        _, buffer = cv2.imencode(".png", level_map_iso_brga)
        texture_byte_arr = io.BytesIO(buffer)

        return bytes(texture_byte_arr.getbuffer())

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
        return self._acts_processed[self._quality]
