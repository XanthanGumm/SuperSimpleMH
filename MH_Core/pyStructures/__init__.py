from ctypes import Structure
from ctypes.wintypes import DWORD
from ctypes.wintypes import WORD
from ctypes.wintypes import BYTE
from ctypes.wintypes import CHAR
from ctypes import c_void_p
from ctypes import c_bool


class UnitHashTable(Structure):
    pass


class UnitAny(Structure):
    pass


class Room1(Structure):
    pass


class Room2(Structure):
    pass


class Level(Structure):
    pass


class ActMisc(Structure):
    pass


class Act(Structure):
    pass


class DynamicPath(Structure):
    pass


class ItemPath(Structure):
    pass


class ObjectPath(Structure):
    pass


class PlayerInfo(Structure):
    pass


class PlayerInfoStrc(Structure):
    pass


class UI(Structure):
    pass


UnitHashTable._fields_ = [
    ("table", c_void_p * 128)
]

UnitAny._fields_ = [
    ("dwType", DWORD),  # 0x00
    ("dwTxtFileNo", DWORD),  # 0x04
    ("dwUnitId", DWORD),  # 0x08
    ("dwMode", DWORD),  # 0x0C
    ("pUnitData", c_void_p),  # 0x10
    ("dwAct", DWORD),  # 0x18
    ("_1", DWORD),  # 0x1C
    ("pAct", c_void_p),  # 0x20
    ("_2", DWORD * 4),  # 0x28
    ("pPath", c_void_p),  # 0x38
    ("_3", DWORD * 0x12),  # 0x40
    ("pStatListEx", c_void_p),  # 0x88 not sure about this later I'll figure it
    ("pInventory", c_void_p),  # 0x90
    ("_4", DWORD * 0x0B),  # 0x98
    ("wX", WORD),  # 0xC4
    ("wY", WORD),  # 0xC6
    ("_5", DWORD * 4),  # 0xC8
    ("unkSortStashBy", DWORD),  # 0xD8
    ("_6", DWORD * 0x09),  # 0xDC
    ("pSkills", c_void_p),  # 0x100
    ("_7", DWORD * 0x12),  # 0x108
    ("pListNext", c_void_p),  # 0x150
    ("pRoomNext", c_void_p),  # 0x158
    ("_8", DWORD * 5),  # 0x160
    ("playerClass", DWORD),  # 0x174
    ("_9", DWORD * 0x0F)  # 0x178
]

Room2._fields_ = [
    ("_1", DWORD * 4),  # 0x00
    ("pRoom2Near", c_void_p),  # 0x10
    ("_2", DWORD * 7),  # 0x18
    ("_3", c_void_p),  # 0x38
    ("_4", c_void_p),  # 0x40 some pointer
    ("pRoom2Next", c_void_p),  # 0x48
    ("_5", DWORD * 2),  # 0x50
    ("pRoom1", c_void_p),  # 0x58
    ("dwPosX", DWORD),  # 0x60
    ("dwPosY", DWORD),  # 0x64
    ("dwSizeX", DWORD),  # 0x68
    ("dwSizeY", DWORD),  # 0x6C
    ("_6", DWORD * 6),  # 0x70
    ("_7", c_void_p),  # 0x88
    ("pLevel", c_void_p),  # 0x90
    ("pPreset", c_void_p)  # 0x98
]

Level._fields_ = [
    ("_1", DWORD * 4),  # 0x00
    ("pRoom2First", c_void_p),  # 0x10
    ("_2", DWORD * 4),  # 0x18
    ("dwPosX", DWORD),  # 0x28
    ("dwPosY", DWORD),  # 0x2C
    ("dwSizeX", DWORD),  # 0x30
    ("dwSizeY", DWORD),  # 0x34
    ("_3", DWORD * 0x60),  # 0x38
    ("pNextLevel", c_void_p),  # 0x1B8
    ("_4", c_void_p),  # 0x1C0
    ("pActMisc", c_void_p),  # 0x1C8
    ("_5", DWORD * 0xA),  # 0x1D0
    ("dwLevelNo", DWORD),  # 0x1F8
    ("_6", DWORD * 3),  # 0x1FC
    ("RoomCenterWrapX", DWORD * 9),  # 0x208
    ("RoomCenterWrapY", DWORD * 9),  # 0x22C
    ("dwRoomEntries", DWORD)  # 250
]

ActMisc._fields_ = [
    ("_1", DWORD * 0x48),  # 0x00
    ("dwRealTombArea", DWORD),  # 0x120
    ("_2", DWORD * 0x1C3),  # 0x124
    ("wDifficulty", WORD),  # 0x830
    ("_3", WORD),  # 0x832
    ("_4", DWORD * 3),  # 0x834
    ("dwInitSeedHash1", DWORD),  # 0x840
    ("dwInitSeedHash2", DWORD),  # 0x844
    ("_5", DWORD * 5),  # 0x848
    ("pAct", c_void_p),  # 0x860
    ("dwEndSeedHash", DWORD),  # 0x868
    ("_6", DWORD),  # 0x86C
    ("pLevelFirst", c_void_p)  # 0x870
]

Room1._fields_ = [
    ("pRoomsNear", c_void_p),  # 0x00
    ("_1", c_void_p),  # 0x08 some pointer
    ("_2", DWORD * 2),  # 0x10
    ("pRoom2", c_void_p),  # 0x18
    ("_3", DWORD * 5),  # 0x20
    ("Coll", c_void_p),  # 0x38
    ("dwRoomsNear", DWORD),  # 0x40
    ("_4", DWORD),  # 0x44
    ("pAct", c_void_p),  # 0x48
    ("_5", DWORD * 0x0C),  # 0x50
    ("dwXStart", DWORD),  # 0x80
    ("dwYStart", DWORD),  # 0x84
    ("dwXSize", DWORD),  # 0x88
    ("dwYSize", DWORD),  # 0x8C
    ("_6", DWORD * 6),  # 0x90
    ("pUnitFirst", c_void_p),  # 0xA8
    ("pRoomNext", c_void_p),  # 0xB0
]

Act._fields_ = [
    ("_1", DWORD * 7),  # 0x00
    ("dwMapSeed", DWORD),  # 0x1C
    ("pRoom1", c_void_p),  # 0x20
    ("dwAct", DWORD),  # 0x28
    ("_2", DWORD * 0x12),  # 0x2C
    ("pActMisc", c_void_p)  # 0x78
]

DynamicPath._fields_ = [
    ("xOffset", WORD),  # 0x00
    ("xPos", WORD),  # 0x02
    ("yOffset", WORD),  # 0x04
    ("yPos", WORD),  # 0x06
    ("_1", DWORD * 6),  # 0x08
    ("pRoom1", c_void_p),  # 0x20
    ("pRoom1Unk", c_void_p),  # 0x28
    ("_2", DWORD * 4),  # 0x30
    ("pUnit", c_void_p),  # 0x40
    ("_3", 10 * DWORD),  # 0x48
    ("pUnitTarget", c_void_p),  # 0x70
    ("dwTargetType", DWORD),  # 0x78
    ("dwTargetId", DWORD),  # 0x7C
    ("_3", BYTE * 2),  # 0x80
    ("bDirection", BYTE),  # 0x82 not sure about this
    ("_4", BYTE),  # 0x83
    ("_5", DWORD * 17),  # 0x84
    ("xTarget", WORD),  # 0xC8
    ("yTarget", WORD),  # 0xCA
]

ItemPath._fields_ = [
    ("_1", DWORD * 4),  # 0x00
    ("xPos", WORD),  # 0x10
    ("_2", WORD),  # 0x12
    ("yPos", WORD)  # 0x14
]

ObjectPath._fields_ = [
    ("pRoom1", c_void_p),  # 0x00
    ("_1", DWORD * 2),  # 0x08
    ("xPos", WORD),  # 0x10
    ("_2", WORD),  # 0x12
    ("yPos", WORD)  # 0x14
]

PlayerInfo._fields_ = [
    ("pPlayerInfoStrc", c_void_p)
]

PlayerInfoStrc._fields_ = [
    ("expansion", c_bool)
]

UI._fields_ = [
    ("inGame", BYTE),
    ("invMenu", c_bool),
    ("charMenu", c_bool),
    ("skillSelect", c_bool),
    ("skillMenu", c_bool),
    ("_2", BYTE * 3),
    ("npcInteract", c_bool),
    ("quitMenu", c_bool),
    ("_3", BYTE),
    ("npcShop", c_bool),
    ("_4", BYTE * 2),
    ("questsMenu", c_bool),
    ("_5", BYTE * 4),
    ("waypointMenu", c_bool),
    ("_6", BYTE),
    ("partyMenu", c_bool),
    ("_7", BYTE * 2),
    ("stash", c_bool),
    ("_8", BYTE * 5),
    ("mercMenu", c_bool),
    ("_9", BYTE * 0x14D),
    ("loading", c_bool)
]

if __name__ == "__main__":
    for field in UI._fields_:
        print(field[0], hex(getattr(UI, field[0]).offset))
