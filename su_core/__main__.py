import pathlib
import os
import subprocess
from su_core.window import Canvas


def main():
    root = pathlib.Path(__file__)
    while root.name != "SuperSimpleMH":
        root = root.parent

    server_path = os.path.join(root, "rpyc-d2-map-api")
    python_exe = os.path.join(server_path, "venv", "Scripts", "python.exe")
    server_proc = subprocess.Popen([python_exe, "-m", "map_server"])
    if server_proc.poll() is not None:
        raise ValueError("Failed to start RPC server")

    try:
        canvas = Canvas()
        canvas.run_event_loop()
    except Exception as e:
        raise e
    finally:
        server_proc.terminate()


if __name__ == '__main__':
    main()
