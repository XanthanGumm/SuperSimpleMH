from su_core.pyTypes import UnitAny
from su_core.pm import mem
from su_core.pyTypes import Act
from su_core.data import Area
from su_core.data import Stat
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
        self._resists = dict()
        self.update()

    def update(self):
        super(Player, self).update()

        if not self.path.is_act_loaded:
            raise InvalidPlayerUnit("Act is not loaded")

        self._act = Act(self._struct.pAct)
        self._name = mem.read_bytes(self._struct.pUnitData, 16).rstrip(b'\x00')

        return True

    def read_stats(self):
        basestats, stats = super(Player, self).read_stats()
        difficulty = self.act.act_misc.difficulty.value
        penalty = 100 if difficulty == 2 else 40 if difficulty == 1 else 0

        if self.unit_id == self.my_player_id:
            self._life = next(iter(basestats[Stat.Life.name][-1].values())) >> 8

            if Stat.MaxLife.name in stats:
                self._maxlife = next(iter(stats[Stat.MaxLife.name][-1].values()))
            else:
                self._maxlife = next(iter(basestats[Stat.MaxLife.name][-1].values()))

            self._life_percent = self._life // self._maxlife

        else:
            # Here I assume all pvpers did Anya quest
            penalty = penalty - 30

        # self._resists["cold"] =
        #
        # self._resists["cold"] = next(iter(stats[Stat.ColdResist.name][-1].values())) - penalty
        # self._resists["fire"] = next(iter(stats[Stat.FireResist.name][-1].values())) - penalty
        # self._resists["light"] = next(iter(stats[Stat.LightningResist.name][-1].values())) - penalty
        # self._resists["poison"] = next(iter(stats[Stat.PoisonResist.name][-1].values())) - penalty
        # # self._resists["physical"] = next(iter(stats[Stat.DamageReduced.name][-1].values()))


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
    def life(self):
        return self._life

    @property
    def maxlife(self):
        return self._maxlife

    @property
    def resists(self):
        return self._resists

    @property
    def life_percent(self):
        return self._life_percent

    @life_percent.setter
    def life_percent(self, p):
        self._life_percent = p

