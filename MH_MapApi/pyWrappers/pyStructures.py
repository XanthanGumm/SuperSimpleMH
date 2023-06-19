from ctypes import Structure
from ctypes.wintypes import DWORD
from ctypes.wintypes import WORD
from ctypes.wintypes import BYTE
from ctypes.wintypes import CHAR
from ctypes.wintypes import WCHAR
from ctypes import POINTER


class CollMap(Structure):
    pass


class Room2(Structure):
    pass


class Room1(Structure):
    pass


class PresetUnit(Structure):
    pass


class RoomTile(Structure):
    pass


class Level(Structure):
    pass


class LevelTxt(Structure):
    pass


class ObjectTxt(Structure):
    pass


class ActMisc(Structure):
    pass


class Act(Structure):
    pass


LevelTxt._fields_ = [
        ("dwLevelNo", DWORD),
        ("_1", DWORD * 60),
        ("_2", BYTE),
        ("szName", CHAR * 40),
        ("szEntranceText", CHAR * 40),
        ("szLevelDesc", CHAR * 40),
        ("wName", WCHAR * 40),
        ("wEntranceText", WCHAR * 40),
        ("nObjGroup", BYTE * 8),
        ("nObjPrb", BYTE * 8)
]


ObjectTxt._fields_ = [
        ("szName", CHAR * 0x40),
        ("wszName", WCHAR * 0x40),
        ("_1", BYTE * 4),
        ("nSelectable0", BYTE),
        ("_2", BYTE * 0x87),
        ("nOrientation", BYTE),
        ("_2b", BYTE * 0x19),
        ("nSubClass", BYTE),
        ("_3", BYTE * 0x11),
        ("nParm0", BYTE),
        ("_4", BYTE * 0x39),
        ("nPopulateFn", BYTE),
        ("nOperateFn", BYTE),
        ("_5", BYTE * 5),
        ("nAutoMap", DWORD)
]


CollMap._fields_ = [
        ("dwPosGameX", DWORD),
        ("dwPosGameY", DWORD),
        ("dwSizeGameX", DWORD),
        ("dwSizeGameY", DWORD),
        ("dwPosRoomX", DWORD),
        ("dwPosRoomY", DWORD),
        ("dwSizeRoomX", DWORD),
        ("dwSizeRoomY", DWORD),
        ("pMapStart", POINTER(WORD)),
        # ("pMapEnd", POINTER(WORD))
    ]


Room2._fields_ = [
        ("_1", DWORD * 2),
        ("pRoom2Near", POINTER(POINTER(Room2))),
        ("_2", DWORD * 6),
        ("pRoom2Next", POINTER(Room2)),
        ("dwRoomFlags", DWORD),
        ("dwRoomsNear", DWORD),
        ("pRoom1", POINTER(Room1)),
        ("dwPosX", DWORD),
        ("dwPosY", DWORD),
        ("dwSizeX", DWORD),
        ("dwSizeY", DWORD),
        ("_3", DWORD),
        ("dwPresetType", DWORD),
        ("pRoomTiles", POINTER(RoomTile)),
        ("_4", DWORD * 2),
        ("pLevel", POINTER(Level)),
        ("pPreset", POINTER(PresetUnit))
    ]


Room1._fields_ = [
        ("pRoomsNear", POINTER(POINTER(Room1))),
        ("_1", DWORD * 3),
        ("pRoom2", POINTER(Room2)),
        ("_2", DWORD * 3),
        ("Coll", POINTER(CollMap)),
        ("dwRoomsNear", DWORD),
        ("_3", DWORD * 9),
        ("dwPosX", DWORD),
        ("dwPosY", DWORD),
        ("dwSizeX", DWORD),
        ("dwSizeY", DWORD),
        ("_4", DWORD * 6),
        ("pUnitFirst", POINTER(DWORD)),
        ("_5", DWORD),
        ("pRoomNext", POINTER(Room1))
    ]


PresetUnit._fields_ = [
        ("_1", DWORD),
        ("dwTxtFileNo", DWORD),
        ("dwPosX", DWORD),
        ("pPresetNext", POINTER(PresetUnit)),
        ("_3", DWORD),
        ("dwType", DWORD),
        ("dwPosY", DWORD)
    ]


RoomTile._fields_ = [
        ("pRoom2", POINTER(Room2)),
        ("pNext", POINTER(RoomTile)),
        ("_2", DWORD * 2),
        ("nNum", POINTER(DWORD))
    ]


Level._fields_ = [
        ("_1", DWORD * 4),
        ("pRoom2First", POINTER(Room2)),
        ("_2", DWORD * 2),
        ("dwPosX", DWORD),
        ("dwPosY", DWORD),
        ("dwSizeX", DWORD),
        ("dwSizeY", DWORD),
        ("_3", DWORD * 96),
        ("pNextLevel", POINTER(Level)),
        ("_4", DWORD),
        ("pMisc", POINTER(ActMisc)),
        ("_5", DWORD * 6),
        ("dwLevelNo", DWORD)
    ]


ActMisc._fields_ = [
        ("_1", DWORD * 37),
        ("dwStaffTombLevel", DWORD),
        ("_2", DWORD * 245),
        ("pAct", POINTER(Act)),
        ("_3", DWORD * 3),
        ("pLevelFirst", POINTER(Level))
    ]

Act._fields_ = [
        ("_1", DWORD * 3),
        ("dwMapSeed", DWORD),
        ("pRoom1", POINTER(Room1)),
        ("dwAct", DWORD),
        ("_2", DWORD * 12),
        ("pMisc", POINTER(ActMisc))
    ]



