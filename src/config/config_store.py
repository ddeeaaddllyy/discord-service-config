from __future__ import annotations

from threading import Event, RLock

from src.domain.models import RuntimeConfig


class ConfigStore:
    def __init__(
        self,
        initial_config: RuntimeConfig,
    ) -> None:
        self._lock = RLock()
        self._config = initial_config
        self._version = 1

        self.changed = Event()

    def snapshot(self) -> tuple[RuntimeConfig, int]:
        with self._lock:
            return self._config, self._version

    def replace(self, config: RuntimeConfig) -> int:
        with self._lock:
            self._config = config
            self._version += 1
            version = self._version

        self.changed.set()

        return version
