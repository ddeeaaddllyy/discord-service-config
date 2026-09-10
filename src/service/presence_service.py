from __future__ import annotations

import logging

from src.config.config_store import ConfigStore
from src.discord.presence import DiscordPresence
from src.domain.matcher import SmartMatcher
from src.platform.windows import WindowsWindowProvider

logger = logging.getLogger(__name__)


class PresenceService:
    def __init__(
        self,
        config_store: ConfigStore,
        windows: WindowsWindowProvider,
        matcher: SmartMatcher,
        presence: DiscordPresence,
    ) -> None:
        self._config_store = config_store
        self._windows = windows
        self._matcher = matcher
        self._presence = presence

    def run(self) -> None:
        while True:
            config, _ = (
                self._config_store.snapshot()
            )

            try:
                windows = (
                    self._windows.get_windows()
                )

                activity = self._matcher.match(
                    windows,
                    config,
                )

                if activity is None:
                    self._presence.clear()
                else:
                    self._presence.update(
                        activity
                    )

            except Exception:
                logger.exception(
                    "Presence iteration failed"
                )

            self._config_store.changed.wait(
                timeout=config.poll_interval
            )

            self._config_store.changed.clear()
