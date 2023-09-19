from abc import ABC, abstractmethod
from concurrent.futures import Future
from rpyc import AsyncResult


class Batch(ABC):

    def __init__(self):
        self._data: dict = dict()
        self._is_processed: bool = False

    def insert_data(self, key, value) -> None:
        self._data[key] = value

    def clear(self):
        self._data.clear()
        self._is_processed = False

    @abstractmethod
    def ready(self):
        return NotImplemented

    @property
    def empty(self) -> bool:
        return bool(self._data)

    @property
    def is_processed(self) -> bool:
        return self._is_processed

    @is_processed.setter
    def is_processed(self, value: bool) -> None:
        self._is_processed = value


class RequestsBatch(Batch):

    def get_data(self, key: AsyncResult):
        return self._data[key]

    def ready(self) -> bool:
        # if not self._data:
        #     raise ValueError("Packet is empty")
        return all(v.ready for v in self._data.keys())

    # def extract_all(self) -> dict:
    #     if not self._data:
    #         raise ValueError("Packet is not ready")
    #     return {k: v.value for k, v in self._data.items()}


class TexturesBatch(Batch):

    def ready(self) -> bool:
        if not self._data:
            return False
        return all(v.done() for v in self._data.values())

    def extract_all(self):
        if not self.ready():
            raise ValueError("BatchTextures is not ready")
        return {k: v.result() for k, v in self._data.items()}

    def cancel(self):
        for job in self._data.values():
            job.cancel()

        self.clear()








