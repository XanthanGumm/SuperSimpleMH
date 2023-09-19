import math
import os
import time
import pyMeow as pm
from su_core.canvas.AdvancedStatsPanel import AdvancedStatsPanel
from su_core.canvas.InventoryPanel import InventoryPanel
from su_core.canvas.MapManager import MapManager
from su_core.canvas.drawings import Colors
from su_core.canvas.drawings import shapes
from su_core.data import Area
from su_core.logging.Logger import Logger
from su_core.math import CSharpVector2
from su_core.pyTypes.unit_types import UnitsFunctions
from su_core.utils import Window
from su_core.utils.exceptions import FailedReadInventory, InvalidPlayerUnit
from su_core.utils.helpers import get_root


class Canvas(Window):
    def __init__(self, shared_memory):  # TODO: type hint this later
        super(Canvas, self).__init__()
        root = get_root(__file__)
        self._logger = Logger.get_logger(__name__)
        self._units = UnitsFunctions.Obtain()

        self._shared_memory = shared_memory
        self._directions_cfg = dict()

        # canvas scalars
        self._label_width_scalar = 0.07
        self._label_height_scalar = 0.05
        self._font_scalar = self._width / (2 * 1280)

        self._width_scalar = (self._width / (1280 * 2)) * 6.786
        self._height_scalar = self._width_scalar / 2
        self._map_scalar = (self._width / (2 * 1280)) * 4.8
        self._texture_scalar = self.get_map_quality_scalar()

        # arrow paddings and boundaries paddings
        self._padding_scalar = self._width / (1280 * 2)
        self._padding_from_center = 100 * self._padding_scalar
        self._padding_from_beginning = 120 * self._padding_scalar

        # labels positions
        self._su_label_posX = self._width * self._label_width_scalar
        self._su_label_posY = self._height * self._label_height_scalar
        self._hostile_labels_pos = CSharpVector2(self._su_label_posX, self._su_label_posY + 2 * self._font_scalar)

        # define angles in order to set boundaries for drawing arrows
        self._margin = CSharpVector2(0.08 * self._width, 0.08 * self._height)
        start = CSharpVector2(*self._center)
        start.y -= self._padding_from_center

        self._q1 = math.atan2(
            self._width - self._margin.x - start.x,
            self._margin.y - start.y,
        )
        if self._q1 < 0:
            self._q1 += 2 * math.pi

        self._q4 = math.atan2(
            self._width - self._margin.x - start.x,
            self._height - self._margin.y - start.y,
        )
        if self._q4 < 0:
            self._q4 += 2 * math.pi

        self._q2 = math.atan2(
            self._margin.x - start.x,
            self._margin.y - start.y,
        )
        if self._q2 < 0:
            self._q2 += 2 * math.pi

        self._q3 = math.atan2(
            self._margin.x - start.x,
            self._height - self._margin.y - start.y,
        )
        if self._q3 < 0:
            self._q3 += 2 * math.pi

        self._hover_player = None
        self._player_inv_tooltip = dict()

        # init PyMeow overlay
        pm.overlay_init(target="Diablo II: Resurrected", trackTarget=True)

        self._inv_win = InventoryPanel(
            self._width,
            self._height,
            self._x,
            self._y,
            int(self._font_scalar * 30),
        )

        self._stats_win = AdvancedStatsPanel(
            self._width,
            self._height,
            self._x,
            self._y,
            int(self._font_scalar * 20),
        )

        self._map_manager = MapManager(self._texture_scalar)

        fps = pm.get_monitor_refresh_rate()
        pm.set_fps(fps)
        pm.set_window_size(self._width, self._height)
        pm.set_window_position(self._x, self._y)
        pm.load_font(os.path.join(root, "fonts", "formal436bt-regular.otf"), 1)

    # TODO: use r_ctype instead of my function.
    def event_loop(self):
        # flags
        pagedn_key = False
        insert_key = False

        while pm.overlay_loop():
            self._map_manager.read_game_ui()

            if self._map_manager.in_game:
                try:
                    player = self._units.obtain_player()

                except InvalidPlayerUnit:
                    continue

                # player in game
                if player is not None:
                    origin = player.path.room1.room2.level.origin
                    game_seed = player.act.act_misc.decrypt_seed()
                    player_area = player.path.room1.room2.level.area.value

                    if self._map_manager.is_new_area(player_area):
                        # set flags and pass data to the gui
                        self._shared_memory.act.value = self._map_manager.act_number
                        self._shared_memory.area.value = player_area
                        self._shared_memory.on_area_change.set()

                    if self._shared_memory.on_directions_change.is_set():
                        self._shared_memory.on_directions_change.clear()
                        self._directions_cfg.clear()
                        self._directions_cfg.update(self._shared_memory.directions)

                    if self._shared_memory.on_quality_change.is_set():
                        self._shared_memory.on_quality_change.clear()
                        self._texture_scalar = self.get_map_quality_scalar()
                        self._map_manager.set_texture_quality(self._texture_scalar)

                    # set rpyc-d2-map-api requirements
                    if self._map_manager.is_new_game(game_seed):
                        acts_levels = []
                        for act, levels in self._shared_memory.acts_levels.items():
                            acts_levels.append(
                                [Area.FromName(lvl).value for lvl, to_load in levels.items() if to_load]
                            )

                        self._map_manager.initialize(
                            seed=game_seed,
                            difficulty=player.act.act_misc.difficulty.value,
                            act_levels=acts_levels,
                        )

                    self._map_manager.update(area=player_area, player_pos=player.path.position)

                    pm.begin_drawing()
                    pm.draw_fps(self._su_label_posX, self._su_label_posY)

                    if self._map_manager.act_number in self._map_manager.acts_processed:
                        map_data = self._map_manager.get_level_data()

                        level_texture = self._map_manager.get_map(area=player_area)
                        adj_level_textures = {
                            level: self._map_manager.get_map(area=level)
                            for level in map_data["adjacent_levels"].keys()
                        }

                        player_minions = self._units.obtain_player_minions(unit_id=player.unit_id)
                        npcs = self._units.obtain_npcs()

                        # check for player hover
                        if pm.key_pressed(0x22):
                            self._wait_to_be_released(key=0x22)

                            pagedn_key = True
                            hovered = self._units.obtain_hovered_player()
                            if hovered is not None:
                                self._stats_win.hover_player = hovered
                                self._stats_win.create_tooltip()
                            else:
                                pagedn_key = False

                        if pagedn_key:
                            self._stats_win.draw_advanced_stats()

                        if pm.key_pressed(0x2D):
                            self._wait_to_be_released(0x2D)

                            insert_key = True
                            hovered = self._units.obtain_hovered_player()
                            if hovered is not None:
                                self._inv_win.hover_player = hovered
                                try:
                                    self._inv_win.create_tooltips()

                                except FailedReadInventory:
                                    insert_key = False
                            else:
                                insert_key = False

                        if insert_key:
                            if pm.key_pressed(0x21):
                                self._wait_to_be_released(0x21)
                                self._inv_win.is_on_switch = not self._inv_win.is_on_switch
                            self._inv_win.draw_inventory()
                            self._inv_win.draw_item_tooltip()

                        if (
                            not self._map_manager.loading_area
                            and not self._map_manager.is_panel_open
                            and not pagedn_key
                            and not insert_key
                            and self._shared_memory.overlay.value
                        ):
                            if level_texture:
                                # draw current level overlay
                                texture_pos = self.world2map(
                                    player_pos=player.path.position,
                                    target_pos=origin,
                                    area_origin=origin,
                                    width_scaler=self._width_scalar,
                                    height_scalar=self._height_scalar,
                                )
                                texture_pos.x = texture_pos.x - map_data["size"][1] * self._map_scalar

                                pm.draw_texture(
                                    level_texture,
                                    texture_pos.x,
                                    texture_pos.y,
                                    Colors.Fade("White", self._shared_memory.overlay_opacity.value),
                                    0,
                                    self._map_scalar / self._texture_scalar,
                                )

                            # draw adjacent levels overlay
                            for level, data in map_data["adjacent_levels"].items():
                                if adj_level_textures[level]:
                                    texture_pos = self.world2map(
                                        player_pos=player.path.position,
                                        target_pos=data["origin"],
                                        area_origin=origin,
                                        width_scaler=self._width_scalar,
                                        height_scalar=self._height_scalar,
                                    )
                                    texture_pos.x = texture_pos.x - data["size"][0] * self._map_scalar

                                    pm.draw_texture(
                                        adj_level_textures[level],
                                        texture_pos.x,
                                        texture_pos.y,
                                        Colors.Fade("White", self._shared_memory.overlay_opacity.value),
                                        0,
                                        self._map_scalar / self._texture_scalar,
                                    )

                            # draw player
                            player_icon_pos = self.world2map(
                                player_pos=player.path.position,
                                target_pos=player.path.position,
                                area_origin=origin,
                                width_scaler=self._width_scalar,
                                height_scalar=self._height_scalar,
                            )
                            self.draw_npc(
                                pos=player_icon_pos,
                                color=Colors.Fade("Cyan", self._shared_memory.npcs_opacity.value),
                            )

                            # draw town npcs
                            for npc in npcs["town"]:
                                icon_pos = self.world2map(
                                    player_pos=player.path.position,
                                    target_pos=npc.path.position,
                                    area_origin=origin,
                                    width_scaler=self._width_scalar,
                                    height_scalar=self._height_scalar,
                                )

                                self.draw_npc(
                                    pos=icon_pos,
                                    color=Colors.Fade("White", self._shared_memory.npcs_opacity.value),
                                )

                                self.draw_npc_label(
                                    pos=icon_pos,
                                    name=npc.name,
                                    cross_multiplayer=6,
                                    font_size=int(self._font_scalar * 26),
                                    text_color=Colors.Fade("White", self._shared_memory.npcs_opacity.value),
                                    background_color=Colors.Get("D2RBlackBackground"),
                                )

                            # draw merc
                            if self._shared_memory.merc.value:
                                for npc in npcs["merc"]:
                                    for minion in player_minions:
                                        if minion.dwUnitId == npc.unit_id and minion.dwOwnerId == player.unit_id:
                                            icon_pos = self.world2map(
                                                player_pos=player.path.position,
                                                target_pos=npc.path.position,
                                                area_origin=origin,
                                                width_scaler=self._width_scalar,
                                                height_scalar=self._height_scalar,
                                            )
                                            self.draw_npc(
                                                pos=icon_pos,
                                                color=Colors.Fade("SeaGreen", self._shared_memory.npcs_opacity.value),
                                            )
                                            break

                            (
                                hostiles_members,
                                in_party_members,
                                members,
                                hostiles_rosters,
                                in_party_rosters,
                            ) = self._units.obtain_members(player.unit_id)

                            # draw in party players
                            for unit_id, member in in_party_rosters.items():
                                m = next((m for m in in_party_members if m.unit_id == unit_id), None)

                                icon_pos = self.world2map(
                                    player_pos=player.path.position,
                                    target_pos=m.path.position if m else member.position,
                                    area_origin=origin,
                                    width_scaler=self._width_scalar,
                                    height_scalar=self._height_scalar,
                                )
                                self.draw_npc(
                                    pos=icon_pos,
                                    color=Colors.Fade("D2RGreen", self._shared_memory.npcs_opacity.value),
                                )

                                self.draw_npc_label(
                                    pos=icon_pos,
                                    name=member.name,
                                    cross_multiplayer=6,
                                    font_size=int(self._font_scalar * 26),
                                    text_color=Colors.Fade("White", self._shared_memory.npcs_opacity.value),
                                    background_color=Colors.Get("GreenBackground"),
                                )

                            # draw hostiled players
                            for index, member in enumerate(hostiles_members):
                                # minions = obtain_player_minions(hostile.unit_id)
                                icon_pos = self.world2map(
                                    player_pos=player.path.position,
                                    target_pos=member.path.position,
                                    area_origin=origin,
                                    width_scaler=self._width_scalar,
                                    height_scalar=self._height_scalar,
                                )
                                self.draw_npc(icon_pos, color=Colors.Fade("Red", self._shared_memory.npcs_opacity.value))

                                self.draw_npc_label(
                                    pos=icon_pos,
                                    name=member.name,
                                    cross_multiplayer=6,
                                    font_size=int(self._font_scalar * 26),
                                    text_color=Colors.Fade("White", self._shared_memory.npcs_opacity.value),
                                    background_color=Colors.Get("RedBackground"),
                                )

                            # draw hostiled life percentage
                            for index, (roster_id, roster) in enumerate(hostiles_rosters.items(), 1):
                                self.draw_hostile_life_percent(
                                    self._hostile_labels_pos,
                                    name=roster.name,
                                    life_percent=roster.life_percent,
                                    index=index,
                                    font_size=int(self._font_scalar * 30),
                                    text_color=Colors.Fade("White", self._shared_memory.npcs_opacity.value),
                                    background_color=Colors.Get("RedBackground"),
                                )

                            # draw players that either not hostile and not in our party
                            for member in members:
                                if member.unit_id not in in_party_rosters and member.unit_id not in hostiles_rosters:
                                    icon_pos = self.world2map(
                                        player_pos=player.path.position,
                                        target_pos=member.path.position,
                                        area_origin=origin,
                                        width_scaler=self._width_scalar,
                                        height_scalar=self._height_scalar,
                                    )
                                    self.draw_npc(icon_pos, color=Colors.Fade("White", self._shared_memory.npcs_opacity.value))

                                    self.draw_npc_label(
                                        pos=icon_pos,
                                        name=member.name,
                                        cross_multiplayer=6,
                                        font_size=int(self._font_scalar * 26),
                                        text_color=Colors.Fade("D2RBrown", self._shared_memory.npcs_opacity.value),
                                        background_color=Colors.Get("D2RBlackBackground"),
                                    )

                            if not player.is_in_town:
                                # draw waypoint
                                if map_data["waypoint"] is not None:
                                    waypoint_position = map_data["waypoint"]
                                    dst_pos = self.world2map(
                                        player_pos=player.path.position,
                                        target_pos=waypoint_position,
                                        area_origin=origin,
                                        width_scaler=self._width_scalar,
                                        height_scalar=self._height_scalar,
                                    )
                                    self.draw_destination_to(
                                        dst_pos=dst_pos,
                                        name="Waypoint",
                                        color=Colors.Fade("Navy", self._shared_memory.directions_opacity.value),
                                    )

                                # draw destination to mazes
                                if map_data["exits"] is not None:
                                    for level, exit_position in map_data["exits"].items():
                                        level_name = Area(level).name
                                        try:
                                            if self._directions_cfg[level_name]:
                                                dst_pos = self.world2map(
                                                    player_pos=player.path.position,
                                                    target_pos=exit_position,
                                                    area_origin=origin,
                                                    width_scaler=self._width_scalar,
                                                    height_scalar=self._height_scalar,
                                                )
                                                self.draw_destination_to(
                                                    dst_pos=dst_pos,
                                                    name=level_name,
                                                    color=Colors.Fade("Green", self._shared_memory.directions_opacity.value),
                                                )
                                        except KeyError:
                                            pass

                                # draw destination to adjacent_levels
                                if map_data["adjacent_levels"] is not None:
                                    for level, data in map_data["adjacent_levels"].items():
                                        level_name = Area(level).name
                                        try:
                                            if self._directions_cfg[level_name]:
                                                for intersection_position in data["outdoor"]:
                                                    dst_pos = self.world2map(
                                                        player_pos=player.path.position,
                                                        target_pos=intersection_position,
                                                        area_origin=origin,
                                                        width_scaler=self._width_scalar,
                                                        height_scalar=self._height_scalar,
                                                    )

                                                    self.draw_destination_to(
                                                        dst_pos=dst_pos,
                                                        name=level_name,
                                                        color=Colors.Fade("GreenYellow", self._shared_memory.directions_opacity.value),
                                                    )
                                        except KeyError:
                                            pass

                                # draw champions, uniques, super uniques
                                if self._shared_memory.uniques.value:
                                    for npc in npcs["unique"]:
                                        icon_pos = self.world2map(
                                            player_pos=player.path.position,
                                            target_pos=npc.path.position,
                                            area_origin=origin,
                                            width_scaler=self._width_scalar,
                                            height_scalar=self._height_scalar,
                                        )

                                        color1 = npc.resists_colors[0] if len(npc.resists_colors) else "White"
                                        color2 = npc.resists_colors[1] if len(npc.resists_colors) > 1 else None
                                        self.draw_npc(
                                            pos=icon_pos,
                                            color=Colors.Fade(color1, self._shared_memory.npcs_opacity.value),
                                            color2=Colors.Fade(color2, self._shared_memory.npcs_opacity.value) if color2 else None,
                                            multiplayer=9,
                                            thickness=2,
                                        )

                                # draw normal monsters
                                if self._shared_memory.monsters.value:
                                    for npc in npcs["other"]:
                                        icon_pos = self.world2map(
                                            player_pos=player.path.position,
                                            target_pos=npc.path.position,
                                            area_origin=origin,
                                            width_scaler=self._width_scalar,
                                            height_scalar=self._height_scalar,
                                        )

                                        color1 = npc.resists_colors[0] if len(npc.resists_colors) else "White"
                                        color2 = npc.resists_colors[1] if len(npc.resists_colors) > 1 else None
                                        self.draw_npc(
                                            pos=icon_pos,
                                            color=Colors.Fade(color1, self._shared_memory.npcs_opacity.value),
                                            color2=Colors.Fade(color2, self._shared_memory.npcs_opacity.value) if color2 else None,
                                        )

                                # draw player minions
                                for npc in npcs["player_minions"]:
                                    for minion in player_minions:
                                        if minion.dwUnitId == npc.unit_id and minion.dwOwnerId == player.unit_id:
                                            icon_pos = self.world2map(
                                                player_pos=player.path.position,
                                                target_pos=npc.path.position,
                                                area_origin=origin,
                                                width_scaler=self._width_scalar,
                                                height_scalar=self._height_scalar,
                                            )

                                            self.draw_npc(
                                                pos=icon_pos,
                                                color=Colors.Fade("RoyalBlue", self._shared_memory.npcs_opacity.value),
                                            )

            pm.end_drawing()

    def draw_hostile_life_percent(self, pos, name, life_percent, index, font_size, text_color, background_color):
        pos = CSharpVector2(pos.x, pos.y + index * (font_size + font_size // 2))
        name += f" - {life_percent}%".encode()
        text_measurement = pm.measure_font(1, name, font_size, 0)
        shapes.draw_label_shape(
            text=name,
            position=pos,
            text_width=text_measurement["x"],
            font_size=font_size,
            text_color=text_color,
            background_color=background_color,
        )

    def draw_npc(self, pos, color, color2=None, multiplayer=6, thickness=1):
        shapes.draw_cross_shape(
            position=pos,
            beta=self._width_scalar,
            gamma=self._height_scalar,
            color=color,
            color2=color2,
            multiplayer=multiplayer,
            thickness=thickness,
        )

    def draw_npc_label(self, pos, name, cross_multiplayer, font_size, text_color, background_color):
        text_measurement = pm.measure_font(1, name, font_size, 0)
        pos.x -= text_measurement["x"] // 2
        pos.y -= text_measurement["y"] + cross_multiplayer * self._height_scalar
        shapes.draw_label_shape(
            text=name,
            position=pos,
            text_width=text_measurement["x"],
            font_size=font_size,
            text_color=text_color,
            background_color=background_color,
        )

    def draw_destination_to(self, dst_pos, name, color):
        start = CSharpVector2(self._center[0], self._center[1] - self._padding_from_center)

        # drawing boundaries
        width_boundary = self._width - self._margin.x
        height_boundary = self._height - self._margin.y

        # player is too close to destination do not the draw arrow
        if math.dist((start.x, start.y), (dst_pos.x, dst_pos.y)) <= self._padding_from_beginning:
            return

        # arrow is too long, therefore, shortens the line to be at the canvas boundaries
        if not (self._margin.x <= dst_pos.x <= width_boundary and self._margin.y <= dst_pos.y <= height_boundary):
            M = (start.y - dst_pos.y) / (start.x - dst_pos.x)

            line_angle = math.atan2(dst_pos.x - start.x, dst_pos.y - start.y)
            if line_angle < 0:
                line_angle += 2 * math.pi

            # checkin the angles which define the drawing boundaries
            if self._q4 <= line_angle <= self._q1:
                dst_pos.x = self._width - self._margin.x
                dst_pos.y = start.y + M * (dst_pos.x - start.x)
            elif self._q1 <= line_angle <= self._q2:
                dst_pos.y = self._margin.y
                dst_pos.x = start.x + (dst_pos.y - start.y) / M
            elif self._q2 <= line_angle <= self._q3:
                dst_pos.x = self._margin.x
                dst_pos.y = start.y + M * (dst_pos.x - start.x)
            elif self._q3 <= line_angle <= 2 * math.pi or 0 <= line_angle <= self._q4:
                dst_pos.y = self._height - self._margin.y
                dst_pos.x = start.x + (dst_pos.y - start.y) / M

        # TODO: adjust font size
        shapes.draw_arrow_shape(
            start=start,
            end=dst_pos,
            padding=self._padding_from_beginning,
            gamma=15,
            color=color,
            text=name,
            font_size=9,
        )

    @staticmethod
    def _wait_to_be_released(key: int, timeout=1):
        start = time.time()
        while time.time() - start <= timeout:
            if not pm.key_pressed(key):
                break
            time.sleep(0.01)

    def get_map_quality_scalar(self) -> float:
        if self._shared_memory.quality.value == b"Low":
            return 1.0
        elif self._shared_memory.quality.value == b"Medium":
            return 2.4
        else:
            return self._map_scalar


if __name__ == "__main__":
    win = Window()
