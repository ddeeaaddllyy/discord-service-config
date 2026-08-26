import time
import psutil
import pygetwindow as gw
from pypresence import Presence
from core.utils.OSutill import OSutill
from core.entity.client_tokens import client_discord_tokens as tokens
import json

# Data from json file that describes all applications and their processes
os_bits = OSutill.get_os_bits()
if os_bits == 64:
    with open(r"..\data\projects64.json", "r", encoding="utf-8") as file:
        data = json.load(file)
elif os_bits == 32:
    with open(r"..\data\projects32.json", "r", encoding="utf-8") as file:
        data = json.load(file)
else:
    raise OSError("Your OS is not available now")

app_map = {exe.lower(): name for name, exe in data["apps"].items() if exe}

rpc = Presence(tokens.CLIENT_ID)
rpc.connect()

last_app_name = None
last_state = None

def is_pycharm_running():
    for proc in psutil.process_iter(["name"]):
        try:
            name = proc.info["name"]
            if name and name.lower() == "pycharm64.exe":
                return True

        except Exception:
            pass

    return False


def get_project_name():
    try:
        for title in gw.getAllTitles():
            if "PyCharm" in title:
                project = title.replace(" - PyCharm", "").strip()

                if project == "":
                    project = "Без проекта"

                return project
    except Exception:
        pass

    return "Unknown project"


while True:

    if is_pycharm_running():

        project = get_project_name()
        if project != last_project:
            rpc.update(
                details="Work in PyCharm",
                state=project,
                large_image="pycharm",
                large_text="PyCharm",
                start=int(time.time())
            )

            last_project = project

    else:
        rpc.clear()
        last_project = None

    time.sleep(5)
