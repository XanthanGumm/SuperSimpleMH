import win32process
import win32gui
import win32api
import win32con
import psutil
from su_core.math import CSharpVector2, CSharpMatrix3X2


class Window:
    def __init__(self):
        self._hwnd = None
        self._init_window_handle()
        assert self._hwnd is not None, "Cannot find Diablo 2 Resurrected canvas"

        # check if the canvas is minimized
        placement = win32gui.GetWindowPlacement(self._hwnd)
        if placement[1] == win32con.SW_SHOWMINIMIZED:
            win32gui.ShowWindow(self._hwnd, win32con.SW_SHOWNORMAL)

        x_start, y_start, x_end, y_end = win32gui.GetClientRect(self._hwnd)
        self._width = x_end - x_start
        self._height = y_end - y_start
        self._x, self._y = win32gui.ClientToScreen(self._hwnd, (x_start, y_start))
        self._x2, self._y2 = win32gui.ClientToScreen(self._hwnd, (x_end, y_end))
        self._center = self._width / 2, self._height / 2

        # TODO: force window to be on top
        try:
            win32gui.ShowWindow(self._hwnd, 5)
            win32gui.SetForegroundWindow(self._hwnd)
        except Exception:
            pass

        # hForeground = win32gui.GetForegroundWindow()
        # cur_thread = win32api.GetCurrentThread()
        # remote_thread = win32process.GetWindowThreadProcessId(hForeground, None)
        #
        # win32process.AttachThreadInput(cur_thread, remote_thread, True)
        # win32gui.SetForegroundWindow(self._hwnd)
        # win32process.AttachThreadInput(cur_thread, remote_thread, False)

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

    def world2map(self, player_pos, target_pos, area_origin, width_scaler, height_scalar):
        map_mat = (
            CSharpMatrix3X2.make_translation(area_origin[0], area_origin[1])
            @ CSharpMatrix3X2.make_translation(-player_pos[0], -player_pos[1])
            @ CSharpMatrix3X2.make_rotation(45)
            @ CSharpMatrix3X2.make_scale(width_scaler, height_scalar)
            @ CSharpMatrix3X2.make_translation(self._center[0], self._center[1])
        )

        area_mat = CSharpMatrix3X2.make_translation(-area_origin[0], -area_origin[1]) @ map_mat

        if isinstance(target_pos, tuple):
            target_pos = CSharpVector2(*target_pos)

        return CSharpVector2.transform(target_pos, area_mat)