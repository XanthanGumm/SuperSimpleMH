class PlayerNotFound(ValueError):
    def __init__(self, value):
        self.value = value
