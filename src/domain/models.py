from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PresenceConfig:
    details: str
    state: str
    large_image: str
    large_text: str


@dataclass(frozen=True, slots=True)
class TitleRule:
    pattern: str
    priority: int = 0
    project_group: str = "project"


@dataclass(frozen=True, slots=True)
class ApplicationConfig:
    id: str
    name: str
    processes: frozenset[str]
    title_rules: tuple[TitleRule, ...]
    presence: PresenceConfig


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    poll_interval: float
    applications: tuple[ApplicationConfig, ...]


@dataclass(frozen=True, slots=True)
class WindowInfo:
    hwnd: int
    pid: int
    process_name: str
    title: str
    foreground: bool


@dataclass(frozen=True, slots=True)
class DetectedActivity:
    app: ApplicationConfig
    project: str
    window: WindowInfo
    score: int
