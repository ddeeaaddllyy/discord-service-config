from __future__ import annotations
import logging
from pathlib import Path
from threading import Lock, Timer
from typing import Callable
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver
from src.config.config_store import ConfigStore
from src.config.starlark_loader import (
    ConfigError,
    StarlarkConfigLoader,
)


logger = logging.getLogger(__name__)


class ConfigFileHandler(FileSystemEventHandler):
    def __init__(
        self,
        config_path: Path,
        callback: Callable[[], None],
        debounce_seconds: float = 0.25,
    ) -> None:
        super().__init__()

        self._config_path = config_path.resolve()
        self._callback = callback
        self._debounce_seconds = debounce_seconds

        self._timer: Timer | None = None
        self._timer_lock = Lock()

    def on_modified(self, event) -> None:
        self._handle(event)

    def on_created(self, event) -> None:
        self._handle(event)

    def on_moved(self, event) -> None:
        self._handle(event)

    def _handle(self, event) -> None:
        if event.is_directory:
            return

        paths: list[Path] = []

        if getattr(event, "src_path", None):
            paths.append(
                Path(event.src_path).resolve()
            )

        if getattr(event, "dest_path", None):
            paths.append(
                Path(event.dest_path).resolve()
            )

        if self._config_path not in paths:
            return

        self._debounce()

    def _debounce(self) -> None:
        with self._timer_lock:
            if self._timer is not None:
                self._timer.cancel()

            self._timer = Timer(
                self._debounce_seconds,
                self._callback,
            )

            self._timer.daemon = True
            self._timer.start()


class ConfigWatcher:
    def __init__(
        self,
        path: Path,
        loader: StarlarkConfigLoader,
        store: ConfigStore,
    ) -> None:
        self._path = path.resolve()
        self._loader = loader
        self._store = store

        self._observer: BaseObserver = Observer()

    def start(self) -> None:
        handler = ConfigFileHandler(
            config_path=self._path,
            callback=self._reload,
        )

        self._observer.schedule(
            handler,
            str(self._path.parent),
            recursive=False,
        )

        self._observer.start()

        logger.info(
            "Watching config: %s",
            self._path,
        )

    def stop(self) -> None:
        self._observer.stop()
        self._observer.join()

    def _reload(self) -> None:
        try:
            config = self._loader.load(
                self._path
            )
        except ConfigError:
            logger.exception(
                "Config reload failed. "
                "Keeping previous configuration."
            )
            return
        except Exception:
            logger.exception(
                "Unexpected config reload error. "
                "Keeping previous configuration."
            )
            return

        version = self._store.replace(config)

        logger.info(
            "Configuration reloaded successfully. "
            "Version=%d",
            version,
        )