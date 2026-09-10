from __future__ import annotations

import logging
import time

from pypresence import Presence

from src.domain.models import DetectedActivity

logger = logging.getLogger(__name__)


class DiscordPresence:
    def __init__(
        self,
        client_id: str,
    ) -> None:
        self._client_id = client_id

        self._rpc: Presence | None = None

        self._last_payload: tuple | None = None
        self._active_app_id: str | None = None
        self._started_at: int | None = None

    def connect(self) -> None:
        rpc = Presence(self._client_id)
        rpc.connect()

        self._rpc = rpc

        logger.info(
            "Connected to Discord RPC"
        )

    def update(self, activity: DetectedActivity) -> None:
        app = activity.app

        if self._active_app_id != app.id:
            self._active_app_id = app.id
            self._started_at = int(time.time())

        presence = app.presence

        details = presence.details.format(
            app=app.name,
            project=activity.project,
        )

        state = presence.state.format(
            app=app.name,
            project=activity.project,
        )

        payload = (
            app.id,
            details,
            state,
            presence.large_image,
            presence.large_text,
        )

        if payload == self._last_payload:
            return

        if self._rpc is None:
            self.connect()

        assert self._rpc is not None

        self._rpc.update(
            details=details,
            state=state,
            large_image=presence.large_image,
            large_text=presence.large_text,
            start=self._started_at,
        )

        self._last_payload = payload

    def clear(self) -> None:
        if (
            self._rpc is not None
            and self._last_payload is not None
        ):
            self._rpc.clear()

        self._last_payload = None
        self._active_app_id = None
        self._started_at = None
