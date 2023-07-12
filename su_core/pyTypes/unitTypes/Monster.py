from su_core.pyTypes import UnitAny
from su_core.pyStructures import MonsterData, MonsterTxt
from su_core.pm import mem
from su_core.data import PlrMode, MonsterTypeFlag, Npc, UselessNpc, Stat


class Monster(UnitAny):

    def __init__(self, address):
        super(Monster, self).__init__(address)
        self._monster_data = None
        self._monster_txt = None
        self._mode = None
        self._npc = None
        self._resists = dict()
        self._immunities_colors = []
        self.update()

    def update(self):
        super(Monster, self).update()
        self._monster_data = mem.read_struct(self._struct.pUnitData, MonsterData)
        self._monster_txt = mem.read_struct(self._monster_data.pMonsterTxt, MonsterTxt)
        self._mode = PlrMode(self._struct.dwMode)
        self._npc = Npc(self._txt_file_no)

    def read_stats(self):
        basestats, stats = super(Monster, self).read_stats()
        if Stat.ColdResist.name in stats:
            cold_res = next(iter(stats[Stat.ColdResist.name][-1].values()))
            self._resists["cold"] = cold_res
            if cold_res >= 100:
                self._immunities_colors.append("blue")
        if Stat.FireResist.name in stats:
            fire_res = next(iter(stats[Stat.FireResist.name][-1].values()))
            self._resists["fire"] = fire_res
            if fire_res >= 100:
                self._immunities_colors.append("red")
        if Stat.LightningResist.name in stats:
            light_res = next(iter(stats[Stat.LightningResist.name][-1].values()))
            self._resists["light"] = light_res
            if light_res >= 100:
                self._immunities_colors.append("yellow")
        if Stat.PoisonResist.name in stats:
            poison_res = next(iter(stats[Stat.PoisonResist.name][-1].values()))
            self._resists["poison"] = poison_res
            if poison_res >= 100:
                self._immunities_colors.append("green")
        if Stat.MagicResist.name in stats:
            magic_res = next(iter(stats[Stat.MagicResist.name][-1].values()))
            if magic_res >= 100:
                self._immunities_colors.append("gold")
        if Stat.DamageReduced.name in stats:
            physical_res = next(iter(stats[Stat.DamageReduced.name][-1].values()))
            if physical_res >= 100:
                self._immunities_colors.append("saddlebrown")

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
    def resists(self):
        return self._resists

    @property
    def resists_colors(self):
        return self._immunities_colors
