from su_core.pyTypes import UnitAny
from su_core.pm import mem
from su_core.pyTypes import Act
from su_core.data import Area
from su_core.data import StatOriginal
from su_core.pyTypes.unitTypes.Inventories import Inventories
from su_core.utils.exceptions import InvalidPlayerUnit


class Player(UnitAny):

    my_player_id = None

    def __init__(self, address):
        super(Player, self).__init__(address)
        self._act = None
        self._area = None
        self._name = None
        self._life = None
        self._maxlife = None
        self._life_percent = None
        self._ias = None
        self._fcr = None
        self._fhr = None
        self._frw = None
        self._resists = dict()
        self._inventory = None

    def update(self):
        super(Player, self).update()

        if not self.path.is_act_loaded:
            raise InvalidPlayerUnit("Act is not loaded")

        self._act = Act(self._struct.pAct)
        self._name = mem.read_bytes(self._struct.pUnitData, 16).rstrip(b'\x00')

        return True

    def read_player_stats(self):
        difficulty = self.act.act_misc.difficulty.value
        penalty = 100 if difficulty == 2 else 40 if difficulty == 1 else 0
        stats = self.read_stats(self._stats_list_struct.Stats)

        if self.unit_id == self.my_player_id:
            basestats = self.read_stats(self._stats_list_struct.BaseStats)
            self._life = next(iter(basestats[StatOriginal.Life.name][-1].values())) >> 8
            if StatOriginal.MaxLife.name in stats:
                self._maxlife = next(iter(stats[StatOriginal.MaxLife.name][-1].values()))
            else:
                self._maxlife = next(iter(basestats[StatOriginal.MaxLife.name][-1].values()))

            self._life_percent = self._life // self._maxlife

        else:
            penalty = penalty - 30

        cold, fire, light, poison, magic, physical = 0, 0, 0, 0, 0, 0
        fcr, frw, fhr, ias = 0, 0, 0, 0

        if StatOriginal.coldresist.name in stats:
            cold = next(iter(stats[StatOriginal.coldresist.name][-1].values()))
        if StatOriginal.fireresist.name in stats:
            fire = next(iter(stats[StatOriginal.fireresist.name][-1].values()))
        if StatOriginal.lightresist.name in stats:
            light = next(iter(stats[StatOriginal.lightresist.name][-1].values()))
        if StatOriginal.poisonresist.name in stats:
            poison = next(iter(stats[StatOriginal.poisonresist.name][-1].values()))
        if StatOriginal.magicresist.name in stats:
            magic = next(iter(stats[StatOriginal.magicresist.name][-1].values()))
        if StatOriginal.damageresist.name in stats:
            physical = next(iter(stats[StatOriginal.damageresist.name][-1].values()))

        if StatOriginal.item_fastercastrate.name in stats:
            fcr = next(iter(stats[StatOriginal.item_fastercastrate.name][-1].values()))
        if StatOriginal.item_fasterattackrate.name in stats:
            ias = next(iter(stats[StatOriginal.item_fasterattackrate.name][-1].values()))
        if StatOriginal.item_fastermovevelocity.name in stats:
            frw = next(iter(stats[StatOriginal.item_fastermovevelocity.name][-1].values()))
        if StatOriginal.item_fastergethitrate.name in stats:
            fhr = next(iter(stats[StatOriginal.item_fastergethitrate.name][-1].values()))

        self._resists["cold"] = cold - penalty
        self._resists["fire"] = fire - penalty
        self._resists["light"] = light - penalty
        self._resists["poison"] = poison - penalty
        self._resists["magic"] = magic
        self._resists["physical"] = physical

        self._fcr = fcr
        self._fhr = fhr
        self._frw = frw
        self._ias = ias

    def read_player_inventory(self):
        self._inventory = Inventories(self._struct.pInventory)
        self._inventory.read_equip_items()

    @property
    def act(self):
        return self._act

    @property
    def name(self):
        return self._name

    @property
    def is_in_town(self):
        return self.path.room1.room2.level.area in [Area.RogueEncampment,
                                                    Area.LutGholein,
                                                    Area.KurastDocks,
                                                    Area.ThePandemoniumFortress,
                                                    Area.Harrogath]

    @property
    def inventory(self) -> Inventories:
        return self._inventory

    @property
    def life(self):
        return self._life

    @property
    def maxlife(self):
        return self._maxlife

    @property
    def life_percent(self):
        return self._life_percent

    @life_percent.setter
    def life_percent(self, p):
        self._life_percent = p

    @property
    def resists(self):
        return self._resists

    @property
    def fcr(self):
        return self._fcr

    @property
    def fhr(self):
        return self._fhr

    @property
    def frw(self):
        return self._frw

    @property
    def ias(self):
        return self._ias


