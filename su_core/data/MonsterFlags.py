from enum import Enum


class MonsterTypeFlag(Enum):
    none = 0
    Other = 1
    SuperUnique = 1 << 1
    Champion = 1 << 2
    Unique = 1 << 3
    Minion = 1 << 4
    Possessed = 1 << 5
    Ghostly = 1 << 6
    Multishot = 1 << 7
