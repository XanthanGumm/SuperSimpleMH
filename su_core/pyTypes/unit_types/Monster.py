from su_core.pyTypes import UnitAny
from su_core.pyStructures import MonsterData, MonsterTxt
from su_core.data import PlrMode, MonsterTypeFlag, Npc, UselessNpc, StatOriginal


class Monster(UnitAny):
    def __init__(self, address):
        super(Monster, self).__init__(address)
        if self._struct.pStatList:
            self._is_revived = self._mem.read_uint(self._struct.pStatList + 0xAC8 + 0xC) & 31 == 1
        else:
            self._is_revived = False

        self._monster_data = None
        self._monster_txt = None
        self._mode = PlrMode(self._struct.dwMode)
        self._npc = Npc(self._txt_file_no)
        self._resists = dict()
        self._immunities_colors = []

    def update(self):
        super(Monster, self).update()
        self._monster_data = self._mem.read_struct(self._struct.pUnitData, MonsterData)
        self._monster_txt = self._mem.read_struct(self._monster_data.pMonsterTxt, MonsterTxt)

    def read_npc_stats(self) -> bool:
        if not self._stats_list_struct.Stats.pStats:
            return False

        stats = self.read_stats(self._stats_list_struct.Stats)
        if StatOriginal.coldresist.name in stats:
            cold_res = next(iter(stats[StatOriginal.coldresist.name][-1].values()))
            self._resists["cold"] = cold_res
            if cold_res >= 100:
                self._immunities_colors.append("Blue")
        if StatOriginal.fireresist.name in stats:
            fire_res = next(iter(stats[StatOriginal.fireresist.name][-1].values()))
            self._resists["fire"] = fire_res
            if fire_res >= 100:
                self._immunities_colors.append("Red")
        if StatOriginal.lightresist.name in stats:
            light_res = next(iter(stats[StatOriginal.lightresist.name][-1].values()))
            self._resists["light"] = light_res
            if light_res >= 100:
                self._immunities_colors.append("Yellow")
        if StatOriginal.poisonresist.name in stats:
            poison_res = next(iter(stats[StatOriginal.poisonresist.name][-1].values()))
            self._resists["poison"] = poison_res
            if poison_res >= 100:
                self._immunities_colors.append("Green")
        if StatOriginal.magicresist.name in stats:
            magic_res = next(iter(stats[StatOriginal.magicresist.name][-1].values()))
            if magic_res >= 100:
                self._immunities_colors.append("Gold")
        if StatOriginal.damageresist.name in stats:
            physical_res = next(iter(stats[StatOriginal.damageresist.name][-1].values()))
            if physical_res >= 100:
                self._immunities_colors.append("SaddleBrown")

        return True

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
    def is_revived(self):
        return self._is_revived

    @property
    def is_strong_monster(self):
        return (
            (self._monster_data.bMonsterTypeFlags & MonsterTypeFlag.Champion.value) != 0
            or (self._monster_data.bMonsterTypeFlags & MonsterTypeFlag.Unique.value) != 0
            or (self._monster_data.bMonsterTypeFlags & MonsterTypeFlag.SuperUnique.value) != 0
        )

    @property
    def resists(self):
        return self._resists

    @property
    def resists_colors(self):
        return self._immunities_colors

    @property
    def name(self):
        return self._monster_txt.name.capitalize()
