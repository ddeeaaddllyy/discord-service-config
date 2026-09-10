from __future__ import annotations

import logging

import psutil
import win32gui
import win32process

from src.domain.models import WindowInfo

logger = logging.getLogger(__name__)


class WindowsWindowProvider:
    def get_windows(self) -> list[WindowInfo]:
        windows: list[WindowInfo] = []

        foreground_hwnd = win32gui.GetForegroundWindow()

        def callback(hwnd: int, _: object) -> bool:
            try:
                if not win32gui.IsWindowVisible(hwnd):
                    return True

                title = win32gui.GetWindowText(hwnd).strip()

                if not title:
                    return True

                _, pid = win32process.GetWindowThreadProcessId(hwnd)

                if not pid:
                    return True

                try:
                    process_name = psutil.Process(pid).name().lower()
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                ):
                    return True

                windows.append(
                    WindowInfo(
                        hwnd=hwnd,
                        pid=pid,
                        process_name=process_name,
                        title=title,
                        foreground=(hwnd == foreground_hwnd),
                    )
                )

            except Exception:
                logger.debug(
                    "Failed reading hwnd=%s",
                    hwnd,
                    exc_info=True,
                )

            return True

        win32gui.EnumWindows(
            callback,
            None,
        )

        return windows
