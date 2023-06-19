import rpyc
import time
import psutil
import win32gui
import win32con
import win32process
from MH_Core.pyTypes.unitTypes import obtain_player, Menu, Menus, PlayerNotFound
from MH_Core.window.shapes import *
from MH_Core.math import *


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

    def world2map(self, player_pos, target_pos, area_origin):

        map_mat = CSharpMatrix3X2.make_translation(area_origin[0], area_origin[1]) @ \
                  CSharpMatrix3X2.make_translation(-player_pos[0], -player_pos[1]) @ \
                  CSharpMatrix3X2.make_rotation(45) @ \
                  CSharpMatrix3X2.make_scale(self._scaleW, self._scaleH) @ \
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

    def draw_player_circle(self):
        pm.draw_circle_lines(self._center[0], self._center[1] - self._center_pad, self._start_line_pad, pm.get_color("red"))

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
    colors = {"greenyellow": pm.get_color("greenyellow"),
              "green": pm.get_color("green"),
              "navy": pm.get_color("navy")}

    def __init__(self):
        self._win = Window()
        pm.overlay_init()
        fps = pm.get_monitor_refresh_rate()
        pm.set_fps(fps)
        pm.set_window_size(self._win.width, self._win.height)
        pm.set_window_position(self._win.start_pos_x, self._win.start_pos_y)

        self._rpconn = rpyc.connect("localhost", port=18861)

    def try_get_player(self):
        menu = Menu()
        if not menu.is_open:
            try:
                player = obtain_player()
            except PlayerNotFound as e:
                if menu.last_open in [Menus.charMenu, Menus.quitMenu, Menus.loading]:
                    time.sleep(0.1)
                    return None
                raise e

            if player.update():
                return player

        return None

    def run_event_loop(self):
        current_area = None
        origin = None
        waypoint = None
        exits = None
        adjacent_levels = None

        while pm.overlay_loop():

            player = self.try_get_player()
            if player is not None:

                current_seed = player.act.act_misc.decrypt_seed

                if current_seed != self._rpconn.root.map_seed():
                    self._rpconn.root.set_map_seed(current_seed)
                    self._rpconn.root.set_difficulty(player.act.act_misc.difficulty.value)
                    current_area = None

                if player.path.room1.room2.level.area.value != current_area:
                    current_area = player.path.room1.room2.level.area.value
                    origin = player.path.room1.room2.level.origin
                    map_data = self._rpconn.root.obtain_map_data(
                        player.path.room1.room2.level.area.value, player.path.position
                    )
                    waypoint = map_data.waypoint
                    exits = map_data.exits
                    adjacent_levels = map_data.adjacent_levels

                if not player.is_in_town:

                    pm.begin_drawing()
                    if waypoint is not None:
                        end = self._win.world2map(player.path.position, waypoint, origin)
                        self._win.draw_arrow(end, text="Waypoint", color=self.colors["navy"])

                    if exits is not None:
                        for k, v in exits.items():
                            end = self._win.world2map(player.path.position, v, origin)
                            self._win.draw_arrow(end, k, color=self.colors["green"])

                    if adjacent_levels is not None:
                        for k, v in adjacent_levels.items():
                            for c in v["outdoor"]:
                                end = self._win.world2map(player.path.position, c, origin)
                                self._win.draw_arrow(end, k, color=self.colors["greenyellow"])

            pm.end_drawing()


if __name__ == "__main__":
    win = Window()
