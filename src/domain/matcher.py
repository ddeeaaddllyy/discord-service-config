from __future__ import annotations

import re

from src.domain.models import (
    ApplicationConfig,
    DetectedActivity,
    RuntimeConfig,
    WindowInfo,
)


class SmartMatcher:
    PROCESS_SCORE = 1000
    FOREGROUND_SCORE = 500

    def match(
        self,
        windows: list[WindowInfo],
        config: RuntimeConfig,
    ) -> DetectedActivity | None:

        best: DetectedActivity | None = None

        for window in windows:
            for app in config.applications:
                candidate = self._match_app(
                    window,
                    app,
                )

                if candidate is None:
                    continue

                if (
                    best is None
                    or candidate.score > best.score
                ):
                    best = candidate

        return best

    def _match_app(
        self,
        window: WindowInfo,
        app: ApplicationConfig,
    ) -> DetectedActivity | None:

        process_matches = (
            window.process_name
            in app.processes
        )

        # Если processes заданы, чужой процесс
        # не может притвориться этой IDE только
        # из-за похожего title.
        if app.processes and not process_matches:
            return None

        score = 0

        if process_matches:
            score += self.PROCESS_SCORE

        if window.foreground:
            score += self.FOREGROUND_SCORE

        best_project: str | None = None
        best_rule_score = -1

        for rule in app.title_rules:
            match = re.search(
                rule.pattern,
                window.title,
                flags=re.IGNORECASE,
            )

            if match is None:
                continue

            if rule.priority > best_rule_score:
                best_rule_score = rule.priority
                best_project = (
                    self._extract_project(
                        match,
                        rule.project_group,
                    )
                )

        if best_rule_score >= 0:
            score += best_rule_score
        elif app.title_rules:
            # Процесс соответствует, но title
            # ни одному правилу не соответствует.
            #
            # Оставляем process fallback,
            # но сильно понижаем его качество.
            score -= 200

        project = (
            best_project
            or self._fallback_project(
                window.title,
                app,
            )
            or "Без проекта"
        )

        return DetectedActivity(
            app=app,
            project=project,
            window=window,
            score=score,
        )

    @staticmethod
    def _extract_project(
        match: re.Match,
        group: str,
    ) -> str | None:

        try:
            value = match.group(group)
        except (IndexError, KeyError):
            return None

        if value is None:
            return None

        value = value.strip()

        return value or None

    @staticmethod
    def _fallback_project(
        title: str,
        app: ApplicationConfig,
    ) -> str | None:

        separators = (
            " - ",
            " – ",
            " — ",
        )

        for separator in separators:
            if separator in title:
                first, _ = title.split(
                    separator,
                    1,
                )

                first = first.strip()

                if first:
                    return first

        if title.lower() == app.name.lower():
            return None

        return title.strip() or None