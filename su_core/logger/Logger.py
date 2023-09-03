import os
import inspect
import logging
from su_core.utils.helpers import get_root



class Logger:
    def __init__(self):
        root = get_root(__file__)
        self._log_fle = os.path.join(root, "su_core", "logger", "logs.log")
        self._log_level = logging.DEBUG
        self._f_formatter = logging.Formatter('%(asctime)s::%(name)s::%(funcName)s::%(levelname)s:: %(message)s')
        self._s_formatter = logging.Formatter('%(name)s::%(funcName)s::%(levelname)s:: %(message)s')
        if os.path.exists(self._log_fle):
            os.remove(self._log_fle)

    def get_logger(self, module_name):
        logger = logging.getLogger(module_name.split(".")[-1])
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            logger.propagate = False

            # stream handler
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(self._s_formatter)

            # file handler
            file_handler = logging.FileHandler(self._log_fle)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(self._f_formatter)

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        return logger
