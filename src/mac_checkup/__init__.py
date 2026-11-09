import os
import sys
from importlib.resources import files


def main() -> None:
    script_path = str(files("mac_checkup") / "mac-checkup")
    os.execv("/bin/zsh", ["/bin/zsh", script_path, *sys.argv[1:]])
