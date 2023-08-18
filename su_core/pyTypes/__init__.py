import os
import pathlib
import ctypes as ct
from su_core.pm import mem
from su_core.pyStructures import UnitAny as StructUnitAny
from su_core.pyStructures import Act as StructAct
from su_core.pyStructures import ActMisc as StructActMisc
from su_core.pyStructures import DynamicPath
from su_core.pyStructures import Room1 as StructRoom1
from su_core.pyStructures import Room2 as StructRoom2
from su_core.pyStructures import Level as StructLevel
from su_core.pyStructures import StatsList as StructStatList
from su_core.pyStructures import Stat as StructStat
from su_core.pyStructures import ItemPath as StructItemPath
from su_core.data import *


class UnitAny:
    def __init__(self, address, path_type="dynamic"):
        self._address = address
        self._path_type = path_type
        self._struct = self.read_unit_struct()
        self._unit_id = self._struct.dwUnitId
        self._txt_file_no = self._struct.dwTxtFileNo
        self._next = self._struct.pListNext
        self._is_act_loaded = None
        self._path = None
        self._stats_list_struct = None

    def update(self):
        self._stats_list_struct = mem.read_struct(
            self._struct.pStatList, StructStatList
        )

        if self._path_type == "dynamic":
            self._path = Path(self._struct.pPath)
        elif self._path_type == "item":
            self._path = ItemPath(self._struct.pPath)
        elif self._path_type == "object":
            pass

    def read_unit_struct(self) -> StructUnitAny:
        return mem.read_struct(self._address, StructUnitAny)

    @staticmethod
    def read_stats(stat_vector):
        num_of_stats = stat_vector.dwlSize
        raw_stats = mem.read_bytes(
            stat_vector.pStats, num_of_stats * ct.sizeof(StructStat)
        )
        stats_array = StructStat * num_of_stats
        stats_array = stats_array.from_buffer_copy(raw_stats)

        stats = dict()

        for stat_struct in stats_array:
            stat = StatOriginal(stat_struct.wStatId)
            stat_layer = {stat_struct.wLayer: stat_struct.dwValue}
            if stat.name not in stats:
                stats[stat.name] = []
            if stat_layer not in stats[stat.name]:
                stats[stat.name].append(stat_layer)

        return stats

    @property
    def unit_id(self):
        return self._unit_id

    @property
    def path(self):
        return self._path

    @property
    def next(self):
        return self._next


class ActMisc:
    __last_init1 = None
    __last_init2 = None
    __seed = None

    def __init__(self, address):
        self._address = address
        self._struct = None
        self._real_tomb_area = None
        self._difficulty = None

        root = pathlib.Path(__file__)
        while root.name != "SuperSimpleMH":
            root = root.parent

        rustdecrypt = ct.CDLL(os.path.join(root, "dep", "rustdecrypt.dll"))
        self._decrypt_seed = rustdecrypt["get_seed"]
        self._decrypt_seed.argtypes = [ct.c_uint32, ct.c_uint32, ct.c_uint32]
        self._decrypt_seed.restype = ct.c_uint32

        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, StructActMisc)
        self._real_tomb_area = Area(self._struct.dwRealTombArea)
        self._difficulty = Difficulty(self._struct.wDifficulty)

    def decrypt_seed(self):
        init1 = self._struct.dwInitSeedHash1
        init2 = self._struct.dwInitSeedHash1
        end = self._struct.dwEndSeedHash

        if init1 != self.__last_init1 and init2 != self.__last_init2:
            self.__last_init1 = init1
            self.__last_init2 = init2
            self.__seed = self._decrypt_seed(init1, init2, end)

        return self.__seed

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def real_tomb_area(self):
        return self._real_tomb_area


class Act:
    def __init__(self, address):
        self._address = address
        self._struct = None
        self._act_no = None
        self._act_misc = None
        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, StructAct)
        self._act_no = ActNo(self._struct.dwAct)
        self._act_misc = ActMisc(self._struct.pActMisc)

    @property
    def act_no(self):
        return self._act_no

    @property
    def act_misc(self):
        return self._act_misc


class Path:
    def __init__(self, address):
        self._struct = None
        self._room1 = None
        self._is_level_loaded = None
        self._address = address
        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, DynamicPath)
        self._is_level_loaded = self._struct.pRoom1 is not None
        if self._is_level_loaded:
            self._room1 = Room1(self._struct.pRoom1)

    @property
    def position(self):
        return (
            self._struct.xPos + self._struct.xOffset / 65536,
            self._struct.yPos + self._struct.yOffset / 65536,
        )

    @property
    def room1(self):
        return self._room1

    @property
    def is_act_loaded(self):
        return self._is_level_loaded and self.position[0] > 1 and self.position[1] > 1


class ItemPath:
    def __init__(self, address):
        self._address = address
        self._struct = None
        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, StructItemPath)

    @property
    def position(self):
        return self._struct.xPos, self._struct.yPos


class Room1:
    def __init__(self, address):
        self._address = address
        self._struct = None
        self._room2 = None
        self._coll = None
        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, StructRoom1)
        self._room2 = Room2(self._struct.pRoom2)

    @property
    def room2(self):
        return self._room2


class Room2:
    def __init__(self, address):
        self._address = address
        self._struct = None
        self._level = None
        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, StructRoom2)
        self._level = Level(self._struct.pLevel)

    @property
    def level(self):
        return self._level


class Level:
    def __init__(self, address):
        self._address = address
        self._struct = None
        self._area = None
        self._origin = None
        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, StructLevel)
        self._area = Area(self._struct.dwLevelNo)
        self._origin = self._struct.dwPosX * 5, self._struct.dwPosY * 5

    @property
    def area(self):
        return self._area

    @property
    def origin(self):
        return self._origin
