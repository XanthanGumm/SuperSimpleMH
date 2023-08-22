from su_core.pm import mem
from su_core.pyStructures import RosterMember, HostileInfo


class Roster:
    def __init__(self, address):
        self._address = address
        self._struct = mem.read_struct(self._address, RosterMember)
        self._name = bytes(self._struct.name).rstrip(b"\x00")
        self._unit_id = self._struct.dwUnitId
        self._life_percent = self._struct.dwLifePercentage
        self._player_level = self._struct.wPlayerLevel
        self._position = self._struct.dwPosX, self._struct.dwPosY
        self._next = self._struct.pNext
        self._party_id = self._struct.wPartyId

    def is_hostiled(self, unit_id):
        if unit_id == self._unit_id:
            return 0

        p_hostile_info = mem.read_pointer(self._struct.pHostileInfo)

        while True:
            if not p_hostile_info:
                break

            hostile_info = mem.read_struct(p_hostile_info, HostileInfo)

            if hostile_info.dwUnitId == unit_id:
                if hostile_info.dwHostileFlag > 0:
                    return self._unit_id
                return 0

            p_hostile_info = hostile_info.pNext

        return 0

    @property
    def unit_id(self):
        return self._unit_id

    @property
    def position(self):
        return self._struct.dwPosX, self._struct.dwPosY

    @property
    def life_percent(self):
        return self._life_percent

    @property
    def player_level(self):
        return self._player_level

    @property
    def party_id(self):
        return self._party_id

    @property
    def name(self):
        return self._name

    @property
    def next(self):
        return self._next
