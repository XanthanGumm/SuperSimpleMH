from enum import Enum


class Act(Enum):
    Act1 = 0
    Act2 = 1
    Act3 = 2
    Act4 = 3
    Act5 = 4

    @property
    def code(self):
        act_codes = [1, 40, 75, 103, 109, 137]
        return act_codes[self.value]

    @classmethod
    def FromArea(cls, area):
        if 0 <= area < 40:
            return cls(0)
        elif 40 <= area < 75:
            return cls(1)
        elif 75 <= area < 103:
            return cls(2)
        elif 103 <= area < 109:
            return cls(3)
        elif 109 <= area < 200:
            return cls(4)
        raise ValueError("Area code value error")

