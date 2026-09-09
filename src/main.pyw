from __future__ import annotations
import logging
from pathlib import Path
from src.config.config_store import ConfigStore
from src.config.config_watcher import ConfigWatcher
from src.config.starlark_loader import StarlarkConfigLoader
from src.discord.presence import DiscordPresence
from src.domain.matcher import SmartMatcher
from src.platform.windows import WindowsWindowProvider
from src.service.presence_service import PresenceService


CLIENT_ID = "1522675721246478536"


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    root = Path(__file__).resolve().parent.parent

    config_path = (
        root
        / "config"
        / "presence.star"
    )

    loader = StarlarkConfigLoader()

    initial_config = loader.load(
        config_path
    )

    store = ConfigStore(
        initial_config
    )

    watcher = ConfigWatcher(
        path=config_path,
        loader=loader,
        store=store,
    )

    presence = DiscordPresence(
        client_id=CLIENT_ID
    )

    service = PresenceService(
        config_store=store,
        windows=WindowsWindowProvider(),
        matcher=SmartMatcher(),
        presence=presence,
    )

    watcher.start()

    try:
        presence.connect()
        service.run()
    except KeyboardInterrupt:
        pass
    finally:
        watcher.stop()


if __name__ == "__main__":
    main()
