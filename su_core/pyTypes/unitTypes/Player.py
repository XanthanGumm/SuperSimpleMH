from su_core.pyTypes import UnitAny
from su_core.pyTypes import Act
from su_core.data import Area


class Player(UnitAny):

    def __init__(self, address):
        super(Player, self).__init__(address)
        self._act = None
        self._area = None

    def update(self):
        super(Player, self).update()

        if not self.path.is_act_loaded:
            return False

        self._act = Act(self._struct.pAct)

        return True

    @property
    def act(self):
        return self._act

    @property
    def is_in_town(self):
        return self.path.room1.room2.level.area in [Area.RogueEncampment,
                                                    Area.LutGholein,
                                                    Area.KurastDocks,
                                                    Area.ThePandemoniumFortress,
                                                    Area.Harrogath]
