import ctypes as ct
from MH_Core.pm import mem
from MH_Core.pyStructures import UnitAny as StructUnitAny
from MH_Core.pyStructures import Act as StructAct
from MH_Core.pyStructures import ActMisc as StructActMisc
from MH_Core.pyStructures import DynamicPath
from MH_Core.pyStructures import Room1 as StructRoom1
from MH_Core.pyStructures import Room2 as StructRoom2
from MH_Core.pyStructures import Level as StructLevel
from MH_Core.data import *


class UnitAny:

    def __init__(self, address):
        self._address = address
        self._struct = None
        self._unit_id = None
        self._txt_file_no = None
        self._next = None
        self._is_act_loaded = None
        self._path = None
        self.update()

    def read_unit_struct(self) -> StructUnitAny:
        return mem.read_struct(self._address, StructUnitAny)

    # attention - subclasses units will update twice because of the super() in the update method
    # take a look into it later on
    def update(self):
        self._struct = self.read_unit_struct()
        self._unit_id = self._struct.dwUnitId
        self._txt_file_no = self._struct.dwTxtFileNo
        self._next = self._struct.pListNext
        self._path = Path(self._struct.pPath)

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

        rustdecrypt = ct.CDLL(".\\rustdecrypt.dll")
        self._decrypt_seed = rustdecrypt["get_seed"]
        self._decrypt_seed.argtypes = [ct.c_uint32, ct.c_uint32, ct.c_uint32]
        self._decrypt_seed.restype = ct.c_uint32

        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, StructActMisc)
        self._real_tomb_area = Area(self._struct.dwRealTombArea)
        self._difficulty = Difficulty(self._struct.wDifficulty)

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def real_tomb_area(self):
        return self._real_tomb_area

    @property
    def decrypt_seed(self):
        init1 = self._struct.dwInitSeedHash1
        init2 = self._struct.dwInitSeedHash1
        end = self._struct.dwEndSeedHash

        if init1 != self.__last_init1 and init2 != self.__last_init2:
            self.__last_init1 = init1
            self.__last_init2 = init2
            self.__seed = self._decrypt_seed(init1, init2, end)

        return self.__seed


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
        return self._struct.xPos + self._struct.xOffset / 65536, self._struct.yPos + self._struct.yOffset / 65536

    @property
    def room1(self):
        return self._room1

    @property
    def is_act_loaded(self):
        return self._is_level_loaded and self.position[0] > 1 and self.position[1] > 1


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
