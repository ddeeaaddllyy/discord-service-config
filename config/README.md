# Configuration files

This directory contains Starlark configuration files that define the Discord Rich Presence behaviour.

## Files

| File | Purpose |
|------|---------|
| `client.star` | Discord application credentials (client ID and public key). |
| `presence.star` | Polling interval, application definitions, title parsing rules, and presence templates. |
| `autor.star` | Author metadata (encoded). |

## `client.star`

Holds the Discord application credentials required for Rich Presence:

```python
# client.star
CLIENT = {
    "id": "1522675721246478536",
    "public_key": "983e95a6eb09f546b0f5c9264310861af65d5ef9d6488c64e1e49d06384dc160",
}
```

Replace the `id` and `public_key` values with those from your own Discord application.

## `presence.star`

Defines how the daemon detects IDEs and what it sends to Discord. The top‑level `CONFIG` dictionary contains:

* `poll_interval` — how often (in seconds) the daemon scans running processes.
* `applications` — list of IDE definitions. Each definition includes:
  * `id` — internal identifier.
  * `name` — display name.
  * `processes` — list of executable names to match (case‑insensitive).
  * `title_rules` — regex patterns with priorities used to extract the project name from the window title.
  * `presence` — templates for Discord status fields (`details`, `state`, `large_image`, `large_text`).

Example entry for IntelliJ IDEA:

```python
# presence.star
{
    "id": "idea",
    "name": "IntelliJ IDEA",
    "processes": ["idea.exe", "idea64.exe"],
    "title_rules": [
        {"pattern": "^(?P<project>.+?)\\s+[–-]\\s+IntelliJ IDEA$", "priority": 100},
        {"pattern": "^(?P<project>.+?)\\s+[–-]\\s+.*IntelliJ IDEA.*$", "priority": 80},
    ],
    "presence": {
        "details": "Работа в {app}",
        "state": "{project}",
        "large_image": "intellijidea",
        "large_text": "IntelliJ IDEA",
    },
}
```

To add a new IDE, append an entry to the `applications` list following the same structure.

## `autor.star`

Contains author metadata in an encoded form. It is not intended for manual editing.
