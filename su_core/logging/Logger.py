import os
import inspect
import logging, traceback
from su_core.utils.helpers import get_root


class Logger:

    __instance = None
    _file_path = None
    _f_formatter = logging.Formatter('%(asctime)s::%(name)s::%(funcName)s::%(levelname)s:: %(message)s')
    _s_formatter = logging.Formatter('%(name)s::%(funcName)s::%(levelname)s:: %(message)s')

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def _initialize(cls):
        root = get_root(__file__)
        cls._file_path = os.path.join(root, "su_core", "logging", "logs.log")
        if os.path.exists(cls._file_path):
            os.remove(cls._file_path)

        cls.__instance = cls()

    @classmethod
    def get_logger(cls, module_name):

        if not cls.__instance:
            cls._initialize()

        logger = logging.getLogger(module_name.split(".")[-1])
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            logger.propagate = False

            # stream handler
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(cls._s_formatter)

            # file handler
            file_handler = logging.FileHandler(cls._file_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(cls._f_formatter)

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        return logger
