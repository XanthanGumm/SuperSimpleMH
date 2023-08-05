import os
import time
import psutil
import pathlib
import win32gui
import win32con
import win32process
from su_core.window.Inventory import Inventory
from su_core.utils import RPYClient
from logger import traceback, manager
from su_core.utils.exceptions import FailedReadInventory
from su_core.window.drawings import pm_colors
from su_core.math import CSharpVector2, CSharpMatrix3X2
from su_core.window.drawings.shapes import Arrow, Cross, PlayerLabel, HostileLabel, TextBox, pm, math
from su_core.pyTypes.unitTypes import (
    obtain_player,
    obtain_npcs,
    obtain_hostiled_players,
    obtain_hovered_player,
    obtain_player_minions,
    Menu
)

_logger = manager.get_logger(__file__)


class Window:

    def __init__(self):
        self._hwnd = None
        self._init_window_handle()
        assert self._hwnd is not None, "Cannot find Diablo 2 Resurrected window"

        # check if the window is minimized
        placement = win32gui.GetWindowPlacement(self._hwnd)
        if placement[1] == win32con.SW_SHOWMINIMIZED:
            win32gui.ShowWindow(self._hwnd, win32con.SW_SHOWNORMAL)

        x_start, y_start, x_end, y_end = win32gui.GetClientRect(self._hwnd)
        self._width = x_end - x_start
        self._height = y_end - y_start
        self._x_start, self._y_start = win32gui.ClientToScreen(self._hwnd, (x_start, y_start))
        self._x_end, self._y_end = win32gui.ClientToScreen(self._hwnd, (x_end, y_end))
        self._center = self._width / 2, self._height / 2

        self._scaleW = (self._width / (1280 * 2)) * 6.786
        self._scaleH = self._scaleW / 2
        self._center_pad = 100 * self._width / 2560
        self._start_line_pad = 120 * self._width / 2560

        # angles to set boundaries of the window
        self._win_pad = CSharpVector2(0.08 * self._width, 0.08 * self._height)
        start = CSharpVector2(*self._center)
        start.y -= self._center_pad

        self.topright = math.atan2(self.width - self._win_pad.x - start.x, self._win_pad.y - start.y)
        if self.topright < 0:
            self.topright += 2 * math.pi
        self.bottomright = math.atan2(self._width - self._win_pad.x - start.x, self._height - self._win_pad.y - start.y)
        if self.bottomright < 0:
            self.bottomright += 2 * math.pi
        self.topleft = math.atan2(self._win_pad.x - start.x, self._win_pad.y - start.y)
        if self.topleft < 0:
            self.topleft += 2 * math.pi
        self.bottomleft = math.atan2(self._win_pad.x - start.x, self._height - self._win_pad.y - start.y)
        if self.bottomleft < 0:
            self.bottomleft += 2 * math.pi

        win32gui.SetForegroundWindow(self._hwnd)

    def _init_window_handle(self):
        proc_name = "D2R.exe"
        proc_id = None
        for proc in psutil.process_iter():
            if proc_name in proc.name():
                proc_id = proc.pid

        def callback(hwnd, param):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid == proc_id:
                    self._hwnd = hwnd

        win32gui.EnumWindows(callback, None)

    def world2map(self, player_pos, target_pos, area_origin, scaleX=None, scaleY=None):

        map_mat = CSharpMatrix3X2.make_translation(area_origin[0], area_origin[1]) @ \
                  CSharpMatrix3X2.make_translation(-player_pos[0], -player_pos[1]) @ \
                  CSharpMatrix3X2.make_rotation(45) @ \
                  CSharpMatrix3X2.make_scale(self._scaleW if not scaleX else scaleX,
                                             self._scaleH if not scaleY else scaleY) @ \
                  CSharpMatrix3X2.make_translation(self.center[0], self.center[1])

        area_mat = CSharpMatrix3X2.make_translation(-area_origin[0], -area_origin[1]) @ map_mat

        if isinstance(target_pos, tuple):
            target_pos = CSharpVector2(*target_pos)

        return CSharpVector2.transform(target_pos, area_mat)

    def draw_arrow(self, end, text, color):
        start = CSharpVector2(*self.center)
        short_render = math.dist((start.x, start.y - self._center_pad), (end.x, end.y)) <= self._start_line_pad
        if not short_render:
            start.y -= self._center_pad

        if not (
                self._win_pad.x <= end.x <= self._width - self._win_pad.x and
                self._win_pad.y <= end.y <= self._height - self._win_pad.y
        ):
            M = (start.y - end.y) / (start.x - end.x)

            line_angle = math.atan2(end.x - start.x, end.y - start.y)
            if line_angle < 0:
                line_angle += 2 * math.pi

            if self.bottomright <= line_angle <= self.topright:
                end.x = self._width - self._win_pad.x
                end.y = start.y + M * (end.x - start.x)
            elif self.topright <= line_angle <= self.topleft:
                end.y = self._win_pad.y
                end.x = start.x + (end.y - start.y) / M
            elif self.topleft <= line_angle <= self.bottomleft:
                end.x = self._win_pad.x
                end.y = start.y + M * (end.x - start.x)
            elif (
                    self.bottomleft <= line_angle <= 2 * math.pi or
                    0 <= line_angle <= self.bottomright
            ):
                end.y = self._height - self._win_pad.y
                end.x = start.x + (end.y - start.y) / M

        Arrow(start, end, short_render, text, color, self._start_line_pad)

    def draw_cross(self, end, size, colors=[]):
        Cross(end, size, self._scaleW, self._scaleH, colors)

    def draw_player_label(self, end, text, size, font_size, text_color, back_color):
        PlayerLabel(end, text, size, self._scaleH, font_size, text_color, back_color)

    def draw_hostile_label(self, end, hostiled_life_percent, hostiled_index, text, font_size, text_color, back_color):
        end = CSharpVector2(end.x, end.y + hostiled_index * (font_size + font_size // 2))
        text += f" - {hostiled_life_percent}%".encode()
        background_length = pm.measure_text(text, font_size)
        background_length = (background_length - (1 / 6) * background_length) * hostiled_life_percent // 100
        HostileLabel(end, text, background_length, font_size, text_color, back_color)

    def draw_player_stats(self, text, font_size, text_color, back_color):
        overlay_pos = pm.get_window_position()
        mouse_pos = pm.mouse_position()
        relative_pos = mouse_pos["x"] - overlay_pos["x"], mouse_pos["y"] - overlay_pos["y"]
        pad_height = self._scaleH * 25
        pad_width = self._scaleH * 25
        text_length = pm.measure_text(text, font_size)
        text_length = text_length - 1 / 4 * text_length + self._scaleW
        text_height = font_size * text.count("\n") * 1.6 + self._scaleH

        if relative_pos[1] + pad_height + text_height >= self._height - self._win_pad.y - pad_height:
            start_posY = self._height - self._win_pad.y - pad_height - text_height
        elif relative_pos[1] <= self._win_pad.y:
            start_posY = self._win_pad.y + pad_height
        else:
            start_posY = relative_pos[1] + pad_height

        if relative_pos[0] + pad_width + text_length >= self._width - self._win_pad.x // 2 - pad_width:
            start_posX = self._width - self._win_pad.x // 2 - text_length - pad_width
        elif relative_pos[0] <= self._win_pad.x // 2:
            start_posX = self._win_pad.x // 2 + pad_width
        else:
            start_posX = relative_pos[0] + pad_width

        start_pos = CSharpVector2(start_posX - self._scaleW, start_posY - self._scaleH)
        TextBox(start_pos, text, text_length, text_height, font_size, text_color, back_color)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def start_pos_x(self):
        return self._x_start

    @property
    def start_pos_y(self):
        return self._y_start

    @property
    def center(self):
        return self._center


class Canvas:

    def __init__(self):
        root = pathlib.Path(__file__)
        while root.name != "SuperSimpleMH":
            root = root.parent

        self._logger = manager.get_logger(__name__)
        # init Canvas deps
        self._win = Window()
        self.map_cli = RPYClient()
        # canvas scalers
        self._map_scale = (self._win.width / (2 * 1280)) * 4.8
        self.su_label_posX = self._win.width * 0.07
        self.su_label_posY = self._win.height * 0.05
        self.su_label_font_scale = self._win.width / (2 * 1280)
        self.hostile_labels_pos = CSharpVector2(self.su_label_posX, self.su_label_posY + 2 * self.su_label_font_scale)
        self.textures = {"amulet": dict(), "arm": dict(), "armor": dict(), "helm": dict(), "belt": dict(), "boots": dict(), "gloves": dict(), "ring": dict()}

        self._hover_player = None
        self._player_inv_tooltip = dict()

        # init pymeow overlay
        pm.overlay_init()
        self._inv_win = Inventory(self._win.width, self._win.height, self._win.start_pos_x, self._win.start_pos_y, int(self.su_label_font_scale * 30))
        fps = pm.get_monitor_refresh_rate()
        pm.set_fps(fps)
        pm.set_window_size(self._win.width, self._win.height)
        pm.set_window_position(self._win.start_pos_x, self._win.start_pos_y)
        pm.load_font(os.path.join(root, "fonts", "formal436bt-regular.otf"), 1)

    # TODO: use r_ctype instead of my function.
    def event_loop(self):
        # flags
        pageup_key = False
        insert_key = False

        # player_tooltip
        player_tooltip = None

        while pm.overlay_loop():
            menu = Menu()

            if menu.is_game_active:
                player = obtain_player()

                if player is not None:
                    origin = player.path.room1.room2.level.origin
                    current_seed = player.act.act_misc.decrypt_seed()
                    current_area = player.path.room1.room2.level.area.value

                    # new game
                    if current_seed != self.map_cli.prev_seed:
                        difficulty = player.act.act_misc.difficulty.value
                        self._logger.info(f"Set map server with seed: {current_seed}, difficulty: {difficulty}")
                        self.map_cli.set_requirements(current_seed, difficulty)
                        self.map_cli.clear_cache()

                    # new area
                    if self.map_cli.prev_area != current_area:
                        self._logger.info(f"Request map data for area: {current_area}")
                        # clean the buffer when area is changed
                        pm.end_drawing()
                        self.map_cli.prev_area = current_area
                        map_data = self.map_cli.read_map(current_area, player.path.position)
                        level_image = self.map_cli.get_level_image(current_area)
                        level_texture = pm.load_texture_bytes(".png", level_image)

                    player_minions = obtain_player_minions(player.unit_id)
                    npcs = obtain_npcs()

                    pm.begin_drawing()
                    pm.draw_fps(self.su_label_posX, self.su_label_posY)

                    # check for player hover
                    # TODO: fix bug when display default values when player_tooltip is None
                    # if pm.key_pressed(33):
                    #     self._wait_to_be_released(key=33)
                    #     pageup_key = True
                    #     hovered_player = obtain_hovered_player()
                    #     if hovered_player is not None:
                    #         player_tooltip = textwrap.dedent(f"""\
                    #         {str(hovered_player.name, 'utf8')} Stats:
                    #         FasterCastRate: {hovered_player.fcr}
                    #         IncreaseAttackSpeed: {hovered_player.ias}
                    #         FasterHitRecovery: {hovered_player.fhr}
                    #         FasterRunWalk: {hovered_player.frw}
                    #         ColdResist: {hovered_player.resists['cold']}
                    #         FireResist: {hovered_player.resists["fire"]}
                    #         LightResist: {hovered_player.resists["light"]}
                    #         PoisonResist: {hovered_player.resists["poison"]}
                    #         MagicResist: {hovered_player.resists["magic"]}
                    #         PhysicalResist: {hovered_player.resists["physical"]}""")
                    #     else:
                    #         pageup_key = False
                    #         player_tooltip = None
                    #
                    # if pageup_key and player_tooltip is not None:
                    #     self._win.draw_player_stats(
                    #         text=player_tooltip, font_size=int(self.su_label_font_scale * 30),
                    #         text_color="white", back_color="onyx"
                    #     )

                    if pm.key_pressed(0x2d):
                        self._wait_to_be_released(0x2d)
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
                        self._inv_win.draw_inventory()
                        self._inv_win.draw_item_tooltip()

                    if not menu.is_open and not pageup_key:
                        texture_pos = self._win.world2map(player.path.position, origin, origin)
                        texture_pos.x = texture_pos.x - map_data["size"][1] * self._map_scale
                        pm.draw_texture(level_texture, texture_pos.x, texture_pos.y, pm_colors["white"], 0,
                                        self._map_scale)

                        player_icon_pos = self._win.world2map(player.path.position, player.path.position, origin)
                        self._win.draw_cross(player_icon_pos, size=6, colors=["cyan"])

                        # draw npcs
                        for npc in npcs["town"]:
                            icon_pos = self._win.world2map(player.path.position, npc.path.position, origin)
                            self._win.draw_cross(icon_pos, size=6, colors=npc.resists_colors)

                        for npc in npcs["merc"]:
                            for minion in player_minions:
                                if minion.dwUnitId == npc.unit_id and minion.dwOwnerId == player.unit_id:
                                    icon_pos = self._win.world2map(player.path.position, npc.path.position, origin)
                                    self._win.draw_cross(icon_pos, size=6, colors=["seagreen"])
                                    break

                        # draw hostiled players
                        hostiles, rosters = obtain_hostiled_players(player.unit_id)
                        for hostile in hostiles:
                            # minions = obtain_player_minions(hostile.unit_id)
                            icon_pos = self._win.world2map(player.path.position, hostile.path.position, origin)
                            self._win.draw_cross(icon_pos, size=6, colors=["red"])
                            self._win.draw_player_label(
                                icon_pos, text=hostile.name, size=6, font_size=22,
                                text_color="white", back_color="redbackground"
                            )

                        # draw hostiled life percentage
                        for index, (roster_id, roster) in enumerate(rosters.items(), 1):
                            self._win.draw_hostile_label(
                                self.hostile_labels_pos, roster.life_percent, index, text=roster.name,
                                font_size=int(self.su_label_font_scale * 30), text_color="white",
                                back_color="redbackground"
                            )

                        if not player.is_in_town:
                            if map_data["waypoint"] is not None:
                                end = self._win.world2map(player.path.position, map_data["waypoint"], origin)
                                self._win.draw_arrow(end, text="Waypoint", color="navy")

                            if map_data["exits"] is not None:
                                for k, v in map_data["exits"].items():
                                    end = self._win.world2map(player.path.position, v, origin)
                                    self._win.draw_arrow(end, k, color="green")

                            if map_data["adjacent_levels"] is not None:
                                for k, v in map_data["adjacent_levels"].items():
                                    for c in v["outdoor"]:
                                        end = self._win.world2map(player.path.position, c, origin)
                                        self._win.draw_arrow(end, k, color="greenyellow")

                            # draw monsters
                            for npc in npcs["unique"]:
                                icon_pos = self._win.world2map(player.path.position, npc.path.position, origin)
                                self._win.draw_cross(icon_pos, size=9, colors=npc.resists_colors)

                            for npc in npcs["other"]:
                                icon_pos = self._win.world2map(player.path.position, npc.path.position, origin)
                                self._win.draw_cross(icon_pos, size=6, colors=npc.resists_colors)

                            for npc in npcs["player_minions"]:
                                for minion in player_minions:
                                    if minion.dwUnitId == npc.unit_id and minion.dwOwnerId == player.unit_id:
                                        icon_pos = self._win.world2map(player.path.position, npc.path.position, origin)
                                        self._win.draw_cross(icon_pos, size=6, colors=["royalblue"])

            pm.end_drawing()

    @staticmethod
    def _wait_to_be_released(key: int, timeout=1):
        start = time.time()
        while time.time() - start <= timeout:
            if not pm.key_pressed(key):
                break
            time.sleep(0.01)


if __name__ == "__main__":
    win = Window()
