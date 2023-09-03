from multiprocessing import Lock
from su_core.canvas.drawings import pm
# from su_core.utils.helpers import get_root
# import os


class ProgressBar:

    def __init__(self):
        # root = get_root(__file__)

        self._lock = Lock()

        pm.gui_fade(0.5)
        # pm.gui_load_style(os.path.join(root, "resources", "gui_style", "jungle", "jungle.rgs"))
        self._win_width = pm.get_screen_width()
        self._win_height = pm.get_screen_height()

        self._pos_x = self._win_width // 4
        self._pox_y = self._win_height * 0.08

        self._width = self._win_width // 2
        self._height = (self._win_width / (2 * 1280)) * 34

        self._max_value = 0
        self._value = 0

    def initialize_bar(self, start_value: int, max_value: int) -> None:
        self._value = start_value
        self._max_value = max_value

    def update(self, *args) -> None:
        with self._lock:
            self._value += 1

    def draw(self) -> None:
        pm.gui_progress_bar(
            self._pos_x,
            self._pox_y,
            self._width,
            self._height,
            "",
            "",
            self._value,
            0,
            self._max_value,
        )

    @property
    def value(self) -> int:
        return self._value

    # @property
    # def max_value(self):
    #     return self._max_value
    #
    # @max_value.setter
    # def max_value(self, ):

        # pm.gui_label(
        #     self._pos_x + self._width - self._width // 4,
        #     self._pox_y,
        #     self._width // 4,
        #     self._height,
        #     "Loading Maps"
        # )