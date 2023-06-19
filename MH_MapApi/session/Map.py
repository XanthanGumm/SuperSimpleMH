import math
import pyastar2d
import numpy as np
from itertools import groupby
from pyWrappers.pyStructures import *
from utils.data.Area import Area
from utils.data.Npcs import Npc
from utils.data.GameObjects import GameObject
from utils.data.PresetType import PresetType


class Map:
    def __init__(self, d2api, area):
        self._d2api = d2api
        self._area = area

        self.tomb_area = None
        self.originX = None
        self.originY = None
        self.size = None
        self._map = None
        self.adjacent_levels = dict()
        self.npcs = dict()
        self.objects = dict()

        self._rle_map = dict()
        self.collision_map = None
        self.waypoint = None
        self.weights = None

    def read_room_adjacent_levels(self, p_level: POINTER(Level), p_room2: POINTER(Room2)):
        assert p_level, "Pointer to p_level is NULL"
        assert p_room2, "Pointer to p_room2 is NULL"

        n_rooms_near = p_room2.contents.dwRoomsNear
        for room_no in range(n_rooms_near):
            cur = p_room2.contents.pRoom2Near[room_no]
            # if the current level number != from the level number inside the room
            # This is not the same area
            if cur.contents.pLevel.contents.dwLevelNo != p_level.contents.dwLevelNo:
                near_originX = cur.contents.pLevel.contents.dwPosX * 5
                near_originY = cur.contents.pLevel.contents.dwPosY * 5
                near_level_height = cur.contents.pLevel.contents.dwSizeX * 5
                near_level_width = cur.contents.pLevel.contents.dwSizeY * 5
                level_no = cur.contents.pLevel.contents.dwLevelNo
                self.adjacent_levels[Area(level_no).name] = {"origin": (near_originX, near_originY),
                                                             "size": (near_level_width, near_level_height),
                                                             "exits": None,
                                                             "outdoor": []}

    def read_room_collisions(self, p_room2: POINTER(Room2), originX, originY):
        assert p_room2, "Pointer to p_room2 is NULL"

        x = p_room2.contents.pRoom1.contents.Coll.contents.dwPosGameX - originX
        y = p_room2.contents.pRoom1.contents.Coll.contents.dwPosGameY - originY
        cx = p_room2.contents.pRoom1.contents.Coll.contents.dwSizeGameX
        cy = p_room2.contents.pRoom1.contents.Coll.contents.dwSizeGameY
        limitX = x + cx
        limitY = y + cy

        p = p_room2.contents.pRoom1.contents.Coll.contents.pMapStart
        for j in range(y, limitY):
            for i in range(x, limitX):
                index = (j - y) * cy + (i - x)
                self._map[j][i] = p[index]

    def read_room_presets(self, p_room2: POINTER(Room2)):
        assert p_room2, "Pointer to p_room2 is NULL"

        p_preset = p_room2.contents.pPreset
        while p_preset:
            preset_type = PresetType(p_preset.contents.dwType)
            pos_x = p_room2.contents.dwPosX * 5 + p_preset.contents.dwPosX
            pos_y = p_room2.contents.dwPosY * 5 + p_preset.contents.dwPosY
            # if preset_type == PresetType.npc:
            #     npc = Npc(p_preset.contents.dwTxtFileNo)
            #     if self.npcs.get(npc.name):
            #         self.npcs[npc.name].append((pos_x, pos_y))
            #     else:
            #         self.npcs[npc.name] = [(pos_x, pos_y)]
            if preset_type == PresetType.object:
                if p_preset.contents.dwTxtFileNo < 580:
                    object_txt = self._d2api.get_object_txt(p_preset.contents.dwTxtFileNo)
                    if object_txt.contents.nSelectable0:
                        if object_txt.contents.nOperateFn == 23:
                            self.waypoint = (pos_x, pos_y)

            if preset_type == PresetType.tile:
                self.read_room_exits(p_room2, pos_x, pos_y)

            p_preset = p_preset.contents.pPresetNext

    def read_room_exits(self, p_room2, pos_x, pos_y):
        p_room_tile = p_room2.contents.pRoomTiles
        while p_room_tile:
            if p_room_tile.contents.nNum[0] == p_room2.contents.pPreset.contents.dwTxtFileNo:
                level_no = p_room_tile.contents.pRoom2.contents.pLevel.contents.dwLevelNo

                if self.adjacent_levels[Area(level_no).name]["exits"] is not None:
                    raise ValueError("There is more than one exit in this level.")

                self.adjacent_levels[Area(level_no).name]["exits"] = pos_x, pos_y
            p_room_tile = p_room_tile.contents.pNext

    def build_coll_map(self, act: POINTER(Act), area):

        if act.contents.pMisc.contents.dwStaffTombLevel != 0:
            pass  # add the tomb area

        # get the level pointer
        p_level = self._d2api.get_level(act.contents.pMisc, area)
        assert p_level, "Returned NULL p_level from d2api.get_level"

        # init the level rooms
        if not p_level.contents.pRoom2First:
            self._d2api.init_level(p_level)
        assert p_level.contents.pRoom2First, "Pointer to pRoom2First is NULL after init level's rooms"

        self.originX, self.originY = p_level.contents.dwPosX * 5, p_level.contents.dwPosY * 5
        self.size = p_level.contents.dwSizeX * 5, p_level.contents.dwSizeY * 5
        self._map = [[-1] * self.size[0] for _ in range(self.size[1])]

        p_room2 = p_level.contents.pRoom2First
        while p_room2:
            b_added = True if not p_room2.contents.pRoom1 else False
            if b_added:
                self._d2api.add_room_data(act,
                                          p_level.contents.dwLevelNo,
                                          p_room2.contents.dwPosX,
                                          p_room2.contents.dwPosY,
                                          None)

            self.read_room_adjacent_levels(p_level, p_room2)
            # if p_room2.contents.pRoom1 and p_room2.contents.pRoom1.contents.Coll:
            self.read_room_collisions(p_room2, self.originX, self.originY)
            self.read_room_presets(p_room2)

            if b_added:
                self._d2api.remove_room_data(act,
                                             p_level.contents.dwLevelNo,
                                             p_room2.contents.dwPosX,
                                             p_room2.contents.dwPosY,
                                             None)

            p_room2 = p_room2.contents.pRoom2Next

        # print(self.originX, self.originY)
        # print(self.adjacent_levels)

    def _generate_rle_map(self):
        rle_map = []
        rle_map_keys = []
        for row in self._map:
            groups = []
            uniquekeys = []
            for k, g in groupby(row):
                uniquekeys.append(k)
                groups.append(len(list(g)))
            rle_map_keys.append(uniquekeys)
            rle_map.append(groups)

        self._rle_map["keys"] = rle_map_keys
        self._rle_map["rle"] = rle_map

    def generate_coll_map(self):
        collisions = []
        cost_matrix = []
        self._generate_rle_map()
        rle_map_keys, rle_map = self._rle_map["keys"], self._rle_map["rle"]
        for rkeys, rmap in zip(rle_map_keys, rle_map):
            cost_matrix.append([np.inf if k & 1 or k == 1024 else 1 for k, n in zip(rkeys, rmap) for _ in range(n)])
            collisions.append([''.join('X' * n if k & 1 or k == 1024 else ' ' * n for k, n in zip(rkeys, rmap))])

        self.collision_map = collisions
        self.weights = np.array(cost_matrix).astype(np.float32)

    def add_outdoor_exits(self, position):
        sides = {
            "left": {"w": self.weights[:, 0], "outdoor": []},
            "top": {"w": self.weights[0, :], "outdoor": []},
            "right": {"w": self.weights[:, -1], "outdoor": []},
            "down": {"w": self.weights[-1, :], "outdoor": []}
        }

        def outdoor_connectors(w):
            index = 0
            for k, g in groupby(w):
                g = list(g)
                if k == 1. and 3 < len(g) <= 30:
                    yield index + len(g) / 2
                index += len(g)

        for c in outdoor_connectors(sides["left"]["w"]):
            sides["left"]["outdoor"].append(
                {"adjacent": (self.originX - 1, self.originY + c),
                 "edge": (self.originX, self.originY + c)}
            )

        for c in outdoor_connectors(sides["top"]["w"]):
            sides["top"]["outdoor"].append(
                {"adjacent": (self.originX + c, self.originY - 1),
                 "edge": (self.originX + c, self.originY)}
            )

        for c in outdoor_connectors(sides["right"]["w"]):
            sides["right"]["outdoor"].append(
                {"adjacent": (self.originX + self.size[0] + 1, self.originY + c),
                 "edge": (self.originX + self.size[0] - 1, self.originY + c)}
            )

        for c in outdoor_connectors(sides["down"]["w"]):
            sides["down"]["outdoor"].append(
                {"adjacent": (self.originX + c, self.originY + self.size[1] + 1),
                 "edge": (self.originX + c, self.originY + self.size[1] - 1)}
            )

        weights = self.weights.transpose()
        src = int(position[0]) - self.originX, int(position[1]) - self.originY

        for _, c in sides.items():
            c["outdoor"] = sorted(c["outdoor"], key=lambda outdoor: math.dist(outdoor["adjacent"], position),
                                  reverse=True)

            for connector in c["outdoor"]:
                dst = (int(connector["edge"][0] - self.originX), int(connector["edge"][1] - self.originY))
                if pyastar2d.astar_path(weights, src, dst) is None:
                    continue

                for name, info in self.adjacent_levels.items():
                    x, y = connector["adjacent"]
                    w, h = info["size"][1], info["size"][0]
                    if (
                            info["origin"][0] <= x <= info["origin"][0] + w and
                            info["origin"][1] <= y <= info["origin"][1] + h
                    ):
                        self.adjacent_levels[name]["outdoor"].append((x, y))

                # break only if a path has been found
                break
