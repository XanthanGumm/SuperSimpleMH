import os
import logging
import pathlib


class Logger:

    def __init__(self):
        root = pathlib.Path(__file__)
        while root.name != "SuperSimpleMH":
            root = root.parent

        self._log_fle = os.path.join(root, "logger", "logs.log")
        self._log_level = logging.DEBUG

        if os.path.exists(self._log_fle):
            os.remove(self._log_fle)

    def get_logger(self, module_name):
        logger = logging.getLogger(module_name)
        logger.setLevel(self._log_level)
        handler = logging.FileHandler(self._log_fle)
        logger.addHandler(handler)
        return logger
