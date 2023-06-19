import rpyc
from session.Session import Session


class MapService(rpyc.Service):

    game = None

    def on_connect(self, conn):
        self.game = Session()

    @rpyc.exposed
    def map_seed(self):
        return self.game.seed

    @rpyc.exposed
    def set_map_seed(self, seed):
        self.game.seed = seed

    @rpyc.exposed
    def get_difficulty(self):
        return self.game.difficulty

    @rpyc.exposed
    def set_difficulty(self, d):
        self.game.difficulty = d

    @rpyc.exposed
    def obtain_map_data(self, area: int, position: tuple):
        return self.game.obtain_map_data(area, position)

    def on_disconnect(self, conn):
        pass
