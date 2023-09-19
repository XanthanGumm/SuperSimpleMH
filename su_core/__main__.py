import os
import pathlib
import subprocess
import win32gui
import dearpygui.dearpygui as dpg
import multiprocessing as mp
import ctypes
from su_core.canvas import Canvas
from su_core.utils import Config
from su_core.utils import SharedMemory
from su_core.data import Area
from su_core.gui import create_gui, create_directions_checkboxes, on_visibility_change, MARGINS


def run(shared_memory: SharedMemory):
    shared_memory.on_path_validator.wait()

    root = pathlib.Path(__file__)
    while root.name != "SuperSimpleMH":
        root = root.parent

    server_path = os.path.join(root, "rpyc-d2-map-api")
    python_exe = os.path.join(server_path, "venv", "Scripts", "python.exe")
    server_proc = subprocess.Popen([python_exe, "-m", "map_server"])
    if server_proc.poll() is not None:
        raise ValueError("Failed to start RPC server")

    try:
        canvas = Canvas(shared_memory)
        canvas.event_loop()
    except Exception as e:
        raise e
    finally:
        server_proc.terminate()


def main():
    dwm = ctypes.windll.dwmapi
    hwnd = win32gui.FindWindow(None, "Diablo II: Resurrected")
    x, y, *_ = win32gui.GetClientRect(hwnd)
    x_start, y_start = win32gui.ClientToScreen(hwnd, (x, y))

    manager = mp.Manager()
    cfg = Config()
    shared_memory = SharedMemory(manager, cfg)

    dpg.create_context()
    dpg.setup_dearpygui()
    dpg.create_viewport(
        title="Settings",
        width=325,
        height=465,
        x_pos=x_start,
        y_pos=y_start,
        always_on_top=True,
        decorated=False,
        resizable=False,
        clear_color=[0.0, 0.0, 0.0, 0.0],
    )
    create_gui(shared_memory, cfg)

    mh_process = mp.Process(target=run, args=(shared_memory,))

    try:
        mh_process.start()
        dpg.show_viewport()

        is_gui_visible = dpg.get_item_state("main")["visible"]
        hwnd = win32gui.FindWindow(None, "Settings")
        margins = MARGINS(-1, -1, -1, -1)
        dwm.DwmExtendFrameIntoClientArea(hwnd, margins)

        while dpg.is_dearpygui_running():
            visibility_state = dpg.get_item_state("main")["visible"]

            if is_gui_visible != visibility_state:
                on_visibility_change(visibility_state)
                is_gui_visible = visibility_state

            if shared_memory.on_area_change.is_set():
                shared_memory.on_area_change.clear()
                shared_memory.directions.update(cfg.directions[Area(shared_memory.area.value).name])
                shared_memory.on_directions_change.set()
                create_directions_checkboxes(shared_memory, cfg.directions)
            dpg.render_dearpygui_frame()

    except Exception as e:
        raise e

    finally:
        mh_process.close()
        dpg.destroy_context()


if __name__ == "__main__":
    main()
