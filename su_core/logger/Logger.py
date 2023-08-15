import os
import logging
from su_core.utils.helpers import get_root


class Logger:

    def __init__(self):
        root = get_root(__file__)
        self._log_fle = os.path.join(root, "su_core", "logger", "logs.log")
        self._log_level = logging.DEBUG

        if os.path.exists(self._log_fle):
            os.remove(self._log_fle)

    def get_logger(self, module_name):
        logger = logging.getLogger(module_name)
        logger.setLevel(self._log_level)
        handler = logging.FileHandler(self._log_fle)
        logger.addHandler(handler)
        return logger
