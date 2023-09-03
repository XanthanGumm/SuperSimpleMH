import math
import os
import time
import pyMeow as pm
from su_core.canvas.AdvancedStatsPanel import AdvancedStatsPanel
from su_core.canvas.InventoryPanel import InventoryPanel
from su_core.canvas.MapManager import MapManager
from su_core.canvas.drawings import pm_colors
from su_core.canvas.drawings import shapes
from su_core.data import Area
from su_core.logger import manager
from su_core.math import CSharpVector2
from su_core.pyTypes.unitTypes import (
    obtain_player,
    obtain_npcs,
    obtain_members,
    obtain_hovered_player,
    obtain_player_minions,
)
from su_core.utils import Window
from su_core.utils.exceptions import FailedReadInventory, InvalidPlayerUnit
from su_core.utils.helpers import get_root


class Canvas(Window):
    def __init__(self):
        super(Canvas, self).__init__()
        root = get_root(__file__)
        self._logger = manager.get_logger(__name__)
        
        # canvas scalars
        self._label_width_scalar = 0.07
        self._label_height_scalar = 0.05
        self._font_scalar = self._width / (2 * 1280)

        self._width_scalar = (self._width / (1280 * 2)) * 6.786
        self._height_scalar = self._width_scalar / 2
        self._map_scalar = (self._width / (2 * 1280)) * 4.8
        self._texture_scalar = 2.4

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
        pm.overlay_init(target="Diablo II: Resurrected")

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
                    player = obtain_player()

                except InvalidPlayerUnit:
                    continue

                if player is not None:
                    origin = player.path.room1.room2.level.origin
                    game_seed = player.act.act_misc.decrypt_seed()
                    player_area = player.path.room1.room2.level.area.value

                    # new game
                    if self._map_manager.is_new_game(game_seed):
                        self._map_manager.initialize(
                            seed=game_seed,
                            difficulty=player.act.act_misc.difficulty.value,
                        )

                    self._map_manager.update(area=player_area, player_pos=player.path.position)

                    pm.begin_drawing()
                    pm.draw_fps(self._su_label_posX, self._su_label_posY)

                    if self._map_manager.act_number in self._map_manager.acts_processed:
                        map_data = self._map_manager.get_level_data()

                        level_texture = self._map_manager.get_map(area=player_area)
                        adj_level_textures = {
                            level_name: self._map_manager.get_map(area=Area.FromName(level_name).value)
                            for level_name in map_data["adjacent_levels"].keys()
                        }

                        player_minions = obtain_player_minions(unit_id=player.unit_id)
                        npcs = obtain_npcs()

                        # check for player hover
                        if pm.key_pressed(0x22):
                            self._wait_to_be_released(key=0x22)

                            pagedn_key = True
                            hovered = obtain_hovered_player()
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
                            hovered = obtain_hovered_player()
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
                        ):
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
                                pm_colors["White"],
                                0,
                                self._map_scalar / self._texture_scalar,
                            )

                            # draw adjacent levels overlay
                            for name, data in map_data["adjacent_levels"].items():
                                texture_pos = self.world2map(
                                    player_pos=player.path.position,
                                    target_pos=data["origin"],
                                    area_origin=origin,
                                    width_scaler=self._width_scalar,
                                    height_scalar=self._height_scalar,
                                )
                                texture_pos.x = texture_pos.x - data["size"][0] * self._map_scalar

                                pm.draw_texture(
                                    adj_level_textures[name],
                                    texture_pos.x,
                                    texture_pos.y,
                                    pm_colors["White"],
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
                            self.draw_npc(player_icon_pos, color="Cyan")

                            # draw town npcs
                            for npc in npcs["town"]:
                                icon_pos = self.world2map(
                                    player_pos=player.path.position,
                                    target_pos=npc.path.position,
                                    area_origin=origin,
                                    width_scaler=self._width_scalar,
                                    height_scalar=self._height_scalar,
                                )
                                self.draw_npc(icon_pos, color="White")

                            # draw merc
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
                                        self.draw_npc(icon_pos, color="SeaGreen")
                                        break

                            (
                                hostiles_members,
                                in_party_members,
                                members,
                                hostiles_rosters,
                                in_party_rosters,
                            ) = obtain_members(player.unit_id)

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
                                self.draw_npc(icon_pos, color="TooltipGreen")

                                self.draw_npc_label(
                                    pos=icon_pos,
                                    name=member.name,
                                    cross_multiplayer=6,
                                    font_size=int(self._font_scalar * 26),
                                    text_color="White",
                                    background_color="GreenBackground",
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
                                self.draw_npc(icon_pos, color="Red")

                                self.draw_npc_label(
                                    pos=icon_pos,
                                    name=member.name,
                                    cross_multiplayer=6,
                                    font_size=int(self._font_scalar * 26),
                                    text_color="White",
                                    background_color="RedBackground",
                                )

                            # draw hostiled life percentage
                            for index, (roster_id, roster) in enumerate(hostiles_rosters.items(), 1):
                                self.draw_hostile_life_percent(
                                    self._hostile_labels_pos,
                                    name=roster.name,
                                    life_percent=roster.life_percent,
                                    index=index,
                                    font_size=int(self._font_scalar * 30),
                                    text_color="White",
                                    background_color="RedBackground",
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
                                    self.draw_npc(icon_pos, color="White")

                                    self.draw_npc_label(
                                        pos=icon_pos,
                                        name=member.name,
                                        cross_multiplayer=6,
                                        font_size=int(self._font_scalar * 26),
                                        text_color="D2RBrown",
                                        background_color="TooltipBackground",
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
                                    self.draw_destination_to(dst_pos, name="Waypoint", color="Navy")

                                # draw destination to mazes
                                if map_data["exits"] is not None:
                                    for name, exit_position in map_data["exits"].items():
                                        dst_pos = self.world2map(
                                            player_pos=player.path.position,
                                            target_pos=exit_position,
                                            area_origin=origin,
                                            width_scaler=self._width_scalar,
                                            height_scalar=self._height_scalar,
                                        )
                                        self.draw_destination_to(dst_pos, name, color="Green")

                                # draw destination to adjacent_levels
                                if map_data["adjacent_levels"] is not None:
                                    for name, data in map_data["adjacent_levels"].items():
                                        for intersection_position in data["outdoor"]:
                                            dst_pos = self.world2map(
                                                player_pos=player.path.position,
                                                target_pos=intersection_position,
                                                area_origin=origin,
                                                width_scaler=self._width_scalar,
                                                height_scalar=self._height_scalar,
                                            )
                                            self.draw_destination_to(dst_pos, name, color="GreenYellow")

                                # draw champions, uniques, super uniques
                                for npc in npcs["unique"]:
                                    icon_pos = self.world2map(
                                        player_pos=player.path.position,
                                        target_pos=npc.path.position,
                                        area_origin=origin,
                                        width_scaler=self._width_scalar,
                                        height_scalar=self._height_scalar,
                                    )

                                    self.draw_npc(
                                        pos=icon_pos,
                                        color=npc.resists_colors[0] if len(npc.resists_colors) else "White",
                                        color2=npc.resists_colors[1] if len(npc.resists_colors) > 1 else "",
                                        multiplayer=9,
                                        thickness=2,
                                    )

                                # draw normal monsters
                                for npc in npcs["other"]:
                                    icon_pos = self.world2map(
                                        player_pos=player.path.position,
                                        target_pos=npc.path.position,
                                        area_origin=origin,
                                        width_scaler=self._width_scalar,
                                        height_scalar=self._height_scalar,
                                    )

                                    self.draw_npc(
                                        pos=icon_pos,
                                        color=npc.resists_colors[0] if len(npc.resists_colors) else "White",
                                        color2=npc.resists_colors[1] if len(npc.resists_colors) > 1 else "",
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
                                            self.draw_npc(icon_pos, color="RoyalBlue")

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

    def draw_npc(self, pos, color, color2="", multiplayer=6, thickness=1):
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


if __name__ == "__main__":
    win = Window()
