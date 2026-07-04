import time
import psutil
import pygetwindow as gw
from pypresence import Presence


# The client name and avatar are set when creating the Discord application.
# If you use my CLIENT_ID, it will default to "Difference" and my av.
CLIENT_ID = "1522675721246478536"
CLIENT_PUBLIC_KEY = "983e95a6eb09f546b0f5c9264310861af65d5ef9d6488c64e1e49d06384dc160"

rpc = Presence(CLIENT_ID)
rpc.connect()

last_project = None


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
