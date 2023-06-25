import sys
import os
import shutil
import pathlib
import subprocess
from venv import create


def main():
    """
    Script which creates venv and install map_server module for the server side.
    """
    is_64bits = sys.maxsize > 2 ** 32
    if not is_64bits:
        raise Exception("SuperSimpleMH can only run on 64 bit version of python")

    root = pathlib.Path(__file__)
    while root.name != "SuperSimpleMH":
        root = root.parent

    subprocess.run(["py", "-3.11-32", os.path.join("tools", "build.py")], cwd=os.path.join(root, "rpyc-d2-map-api"))

    if os.path.isdir(os.path.join(root, "venv")):
        shutil.rmtree(os.path.join(root, "venv"))

    venv_dir = os.path.join(root, "venv")
    create(venv_dir, with_pip=True)
    subprocess.run([os.path.join(root, "venv", "Scripts", "pip.exe"), "install", "."],
                   stdout=sys.stdout, stderr=sys.stderr)

    pymeow = next(f for f in os.listdir(root) if os.path.split(f)[-1].startswith("pyMeow"))
    subprocess.run([os.path.join(root, 'venv', 'Scripts', 'pip.exe'), "install", pymeow],
                   stdout=sys.stdout, stderr=sys.stderr)


if __name__ == "__main__":
    main()
