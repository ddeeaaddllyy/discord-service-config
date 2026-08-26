import time
import psutil
import pygetwindow as gw
from pypresence import Presence
from core.utils.OSutill import OSutill
from core.entity.client_tokens import client_discord_tokens as tokens

# Data from json file that describes all applications and their processes
data = OSutill.get_apps_json()
app_map = {exe.lower(): name for name, exe in data["apps"].items() if exe}

rpc = Presence(tokens.CLIENT_ID)
rpc.connect()

last_app_name = None
last_state = None


def get_running_app():
    for proc in psutil.process_iter(["name"]):
        try:
            exe = proc.info["name"]
            if not exe:
                continue
            exe_lower = exe.lower()
            if exe_lower in app_map:
                app_name = app_map[exe_lower]
                project = extract_project_name(app_name, exe)
                return app_name, project, exe
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None, None, None


def extract_project_name(app_name, exe_name):
    try:
        search_keywords = [app_name, exe_name.replace(".exe", "").replace("64", "")]
        for title in gw.getAllTitles():
            if not title:
                continue
            title_lower = title.lower()
            for kw in search_keywords:
                if kw.lower() in title_lower:
                    for sep in [" - ", " – ", "  "]:
                        if sep in title:
                            parts = title.split(sep, 1)
                            if len(parts) == 2:
                                project = parts[0].strip()
                                if project:
                                    return project
                    return title.strip()
        return "Без проекта"
    except Exception:
        return "Без проекта"


def update_rpc(app_name, project_name):
    """Обновляет Presence в Discord."""
    if app_name is None:
        rpc.clear()
        return None

    large_image = app_name.replace(" ", "").lower()

    new_state = (app_name, project_name, large_image)
    return new_state


if __name__ == "__main__":
    print("[+] made by ddeeaaddllyy [+]")
    while True:
        app_name, project, exe = get_running_app()

        if app_name:
            details = f"Работа в {app_name}"
            state = project or "Без проекта"
            large_image = app_name.replace(" ", "").lower()
            new_state = (details, state, large_image)

            if new_state != last_state:
                rpc.update(
                    details=details,
                    state=state,
                    large_image=large_image,
                    large_text=app_name,
                    start=int(time.time())
                )
                last_state = new_state
                last_app_name = app_name
        else:
            if last_state is not None:
                rpc.clear()
                last_state = None
                last_app_name = None

        time.sleep(5)