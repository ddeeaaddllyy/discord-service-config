# JetBrains Discord Rich Presence

A lightweight daemon that broadcasts your active JetBrains IDE session to Discord via Rich Presence. The application detects which IDE is currently running, extracts the project name from the window title, and updates your Discord status accordingly — no manual interaction required.

---

## Table of contents

- [What problem does it solve?](#what-problem-does-it-solve)
- [How it works](#how-it-works)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Configuration](#configuration)
- [Installation](#installation)
  - [Local development](#local-development)
  - [Docker](#docker)
- [Usage](#usage)
- [License](#license)

---

## What problem does it solve?

When you work in an IDE for hours, your Discord status stays static. Other people see you as “online” but have no idea what you are actually doing. This daemon bridges that gap:

- It watches for running JetBrains processes.
- When it detects an active IDE, it updates your Discord profile with the project name.
- When you close the IDE, the status clears automatically.

The result is a live, accurate status that tells your teammates or friends exactly what you are working on — without you ever having to type a single command.

---

## How it works

The daemon polls the running processes at a fixed interval. For each process, it checks whether the executable name matches any entry in a local JSON mapping file. When a match is found, it retrieves the active window title, parses out the project name, and sends an update to Discord via the Rich Presence API.

The application supports both 32-bit and 64-bit Windows environments. The appropriate JSON mapping file is selected automatically based on the system architecture.

---

## Architecture

The project follows a straightforward separation of concerns:

| Component | Responsibility |
|-----------|----------------|
| `OSutill` | Detects the system architecture (32-bit vs 64-bit) and loads the corresponding JSON mapping file. |
| `client_discord_tokens` | Holds the Discord application credentials (client ID and public key). |
| `main` | Orchestrates the polling loop: enumerates processes, matches against the mapping, extracts the window title, and updates Discord. |
| JSON data files | Define the relationship between executable names and human-readable IDE names. |

The daemon runs as a long-lived process and updates Discord only when the active application or project changes — it does not spam the API on every poll.

---


---

## Configuration

### Discord application

You need a Discord application with Rich Presence enabled. The client ID and public key are stored in `core/entity/client_tokens.py`:

```python
@dataclass
class client_discord_tokens:
    CLIENT_ID: str = "1522675721246478536"
    CLIENT_PUBLIC_KEY: str = "983e95a6eb09f546b0f5c9264310861af65d5ef9d6488c64e1e49d06384dc160"
```
Replace these values with your own Discord application credentials.

### IDE mappings

The JSON files in the data/ directory define which executable names correspond to which IDE display names:
```json
{
  "ds": "made by ddeeaaddllyy",
  "apps": {
    "PyCharm": "pycharm64.exe",
    "IntelliJ IDEA": "idea64.exe",
    "CLion": "clion64.exe"
  }
}
```
Add or remove entries as needed. The daemon matches executables case-insensitively.

---

## Installation

### Local development

1. Clone the repository: 
    ```bash 
    git clone https://github.com/ddeeaaddllyy/discord-service-config.git
    cd discord-service-config
    ```
2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the daemon:
    ```bash 
    python main.pyw
    ```

---

## License

This project is provided as-is. Refer to the repository for licensing information.

## Autor 

Made by ddeeaaddllyy with love