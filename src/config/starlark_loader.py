from collections.abc import Mapping, Sequence
from pathlib import Path
import re
import starlark
from core.exceptions.config_error import ConfigError
from src.domain.models import (
    ApplicationConfig,
    PresenceConfig,
    RuntimeConfig,
    TitleRule,
)


class StarlarkConfigLoader:
    def load(self, path: Path) -> RuntimeConfig:
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ConfigError(
                f"Cannot read config: {path}"
            ) from exc

        try:
            module = starlark.exec_file(source)
        except Exception as exc:
            raise ConfigError(
                f"Starlark execution failed: {exc}"
            ) from exc

        try:
            raw_config = module.globals["CONFIG"]
        except KeyError as exc:
            raise ConfigError(
                "presence.star must export global CONFIG"
            ) from exc

        raw_config = self._to_python(raw_config)

        return self._parse_config(raw_config)

    def _parse_config(self, raw: dict) -> RuntimeConfig:
        if not isinstance(raw, dict):
            raise ConfigError("CONFIG must be a dictionary")

        poll_interval = float(raw.get("poll_interval", 1.0))

        if poll_interval < 0.1:
            raise ConfigError(
                "poll_interval must be >= 0.1 seconds"
            )

        raw_apps = raw.get("applications")

        if not isinstance(raw_apps, list):
            raise ConfigError(
                "CONFIG['applications'] must be a list"
            )

        applications = tuple(
            self._parse_application(app)
            for app in raw_apps
        )

        ids = [app.id for app in applications]

        if len(ids) != len(set(ids)):
            raise ConfigError(
                "Application ids must be unique"
            )

        return RuntimeConfig(
            poll_interval=poll_interval,
            applications=applications,
        )

    def _parse_application(
        self,
        raw: dict,
    ) -> ApplicationConfig:

        try:
            app_id = str(raw["id"])
            name = str(raw["name"])
        except KeyError as exc:
            raise ConfigError(
                f"Application misses field {exc}"
            ) from exc

        processes = frozenset(
            str(process).lower()
            for process in raw.get("processes", [])
        )

        raw_title_rules = raw.get("title_rules", [])

        title_rules: list[TitleRule] = []

        for rule in raw_title_rules:
            pattern = str(rule["pattern"])
            priority = int(rule.get("priority", 0))
            project_group = str(
                rule.get("project_group", "project")
            )

            try:
                re.compile(pattern)
            except re.error as exc:
                raise ConfigError(
                    f"Invalid regex for {app_id}: "
                    f"{pattern}: {exc}"
                ) from exc

            title_rules.append(
                TitleRule(
                    pattern=pattern,
                    priority=priority,
                    project_group=project_group,
                )
            )

        presence_raw = raw.get("presence", {})

        presence = PresenceConfig(
            details=str(
                presence_raw.get(
                    "details",
                    "Работа в {app}",
                )
            ),
            state=str(
                presence_raw.get(
                    "state",
                    "{project}",
                )
            ),
            large_image=str(
                presence_raw.get(
                    "large_image",
                    app_id,
                )
            ),
            large_text=str(
                presence_raw.get(
                    "large_text",
                    name,
                )
            ),
        )

        if not processes and not title_rules:
            raise ConfigError(
                f"{app_id}: processes or title_rules "
                f"must be specified"
            )

        return ApplicationConfig(
            id=app_id,
            name=name,
            processes=processes,
            title_rules=tuple(title_rules),
            presence=presence,
        )

    def _to_python(self, value):
        if value is None or isinstance(
            value,
            (str, int, float, bool),
        ):
            return value

        if isinstance(value, Mapping):
            return {
                self._to_python(key): self._to_python(item)
                for key, item in value.items()
            }

        if isinstance(value, Sequence):
            return [
                self._to_python(item)
                for item in value
            ]

        if hasattr(value, "items"):
            return {
                self._to_python(key): self._to_python(item)
                for key, item in value.items()
            }

        if hasattr(value, "__iter__"):
            return [
                self._to_python(item)
                for item in value
            ]

        raise ConfigError(
            f"Unsupported Starlark value: {type(value)!r}"
        )
