class PlayerNotFound(ValueError):
    def __init__(self, value=""):
        self.value = value


class InvalidPlayerUnit(ValueError):
    def __init__(self, value=""):
        self.value = value


class ItemTypeNotFound(TypeError):
    def __init__(self, value=""):
        self.value = value


class FailedReadInventory(ValueError):
    def __init__(self, value=""):
        self.value = value
