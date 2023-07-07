from su_core.pyTypes import UnitAny
from su_core.pyStructures import MonsterData, MonsterTxt
from su_core.pm import mem
from su_core.data import PlrMode, MonsterTypeFlag, Npc, UselessNpc


class Monster(UnitAny):

    def __init__(self, address):
        super(Monster, self).__init__(address)
        self._monster_data = None
        self._monster_txt = None
        self._mode = None
        self._npc = None
        self._resistances = dict()
        self._immunities_colors = []

    def update(self):
        super(Monster, self).update()
        self._monster_data = mem.read_struct(self._struct.pUnitData, MonsterData)
        self._monster_txt = mem.read_struct(self._monster_data.pMonsterTxt, MonsterTxt)
        self._mode = PlrMode(self._struct.dwMode)
        self._npc = Npc(self._txt_file_no)

    def read_resistances(self):
        self.read_stats_structs()
        for stat in self._stats:
            if stat.wStatId == 36:
                self._resistances["physical"] = stat.dwValue
                if stat.dwValue >= 100:
                    self._immunities_colors.append("saddlebrown")
            elif stat.wStatId == 37:
                self._resistances["magic"] = stat.dwValue
                if stat.dwValue >= 100:
                    self._immunities_colors.append("gold")
            elif stat.wStatId == 39:
                self._resistances["fire"] = stat.dwValue
                if stat.dwValue >= 100:
                    self._immunities_colors.append("red")
            elif stat.wStatId == 41:
                self._resistances["light"] = stat.dwValue
                if stat.dwValue >= 100:
                    self._immunities_colors.append("yellow")
            elif stat.wStatId == 43:
                self._resistances["cold"] = stat.dwValue
                if stat.dwValue >= 100:
                    self._immunities_colors.append("blue")
            elif stat.wStatId == 45:
                self._resistances["poison"] = stat.dwValue
                if stat.dwValue >= 100:
                    self._immunities_colors.append("green")

    @property
    def npc(self):
        return self._npc

    @property
    def is_useless(self):
        return self._npc in UselessNpc

    @property
    def is_dead(self):  # why the hell the mode is kick when the monster is dead
        return self._mode == PlrMode.Dead or self._mode == PlrMode.Death or self._mode == PlrMode.Kick

    @property
    def is_strong_monster(self):
        return (self._monster_data.bMonsterTypeFlags & MonsterTypeFlag.Champion.value) != 0 or \
               (self._monster_data.bMonsterTypeFlags & MonsterTypeFlag.Unique.value) != 0 or \
               (self._monster_data.bMonsterTypeFlags & MonsterTypeFlag.SuperUnique.value) != 0

    @property
    def resistances(self):
        return self._resistances

    @property
    def resistances_colors(self):
        return self._immunities_colors
