import pathlib
import os
import subprocess
from MH_Core.window import Canvas


if __name__ == '__main__':
    server_path = os.path.join(pathlib.Path(__file__).parent.parent, "MH_MapApi", "main.py")
    server_proc = subprocess.Popen(["py", "-3.11-32", server_path])
    if server_proc.poll() is not None:
        raise ValueError("Failed to start RPC server")

    try:
        canvas = Canvas()
        canvas.run_event_loop()
    finally:
        server_proc.terminate()

