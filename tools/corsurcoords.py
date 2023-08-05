import pyMeow as pm
import psutil
import win32gui
import win32con
import win32process


class Window:

    def __init__(self):
        self._hwnd = None
        self._init_window_handle()

        x_start, y_start, x_end, y_end = win32gui.GetClientRect(self._hwnd)
        self._width = x_end - x_start
        self._height = y_end - y_start
        self._x_start, self._y_start = win32gui.ClientToScreen(self._hwnd, (x_start, y_start))
        self._x_end, self._y_end = win32gui.ClientToScreen(self._hwnd, (x_end, y_end))
        self._center = self._width / 2, self._height / 2

    def _init_window_handle(self, proc_name="D2R.exe"):
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
        self._win = Window()
        self.cursor_posX = self._win.width * 0.07
        self.cursor_posY = self._win.height * 0.05
        self.cursor_color = pm.get_color("white")

        pm.overlay_init()
        fps = pm.get_monitor_refresh_rate()
        pm.set_fps(fps)
        pm.set_window_size(self._win.width, self._win.height)
        pm.set_window_position(self._win.start_pos_x, self._win.start_pos_y)

    def event_loop(self):
        overlay_pos = pm.get_window_position()
        while pm.overlay_loop():
            mouse_pos = pm.mouse_position()
            relative_pos = mouse_pos["x"] - overlay_pos["x"], mouse_pos["y"] - overlay_pos["y"]

            pm.begin_drawing()
            cursor_position = f"X: {relative_pos[0]}, Y: {relative_pos[1]}"
            pm.draw_text(cursor_position, self.cursor_posX, self.cursor_posY, fontSize=20, color=self.cursor_color)
            pm.end_drawing()


if __name__ == "__main__":
    canvas = Canvas()
    canvas.event_loop()