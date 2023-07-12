class PlayerNotFound(ValueError):
    def __init__(self, value):
        self.value = value


class InvalidPlayerUnit(ValueError):
    def __init__(self, value):
        self.value = value
