CONFIG = {
    "poll_interval": 1.0,

    "applications": [
        {
            "id": "idea",
            "name": "IntelliJ IDEA",

            "processes": [
                "idea.exe",
                "idea64.exe",
            ],

            "title_rules": [
                {
                    "pattern": "^(?P<project>.+?)\\s+[–-]\\s+IntelliJ IDEA$",
                    "priority": 100,
                },
                {
                    "pattern": "^(?P<project>.+?)\\s+[–-]\\s+.*IntelliJ IDEA.*$",
                    "priority": 80,
                },
            ],

            "presence": {
                "details": "Работа в {app}",
                "state": "{project}",
                "large_image": "intellijidea",
                "large_text": "IntelliJ IDEA",
            },
        },

        {
            "id": "pycharm",
            "name": "PyCharm",

            "processes": [
                "pycharm.exe",
                "pycharm64.exe",
            ],

            "title_rules": [
                {
                    "pattern": "^(?P<project>.+?)\\s+[–-]\\s+PyCharm.*$",
                    "priority": 100,
                },
            ],

            "presence": {
                "details": "Работа в {app}",
                "state": "{project}",
                "large_image": "pycharm",
                "large_text": "PyCharm",
            },
        },

        {
            "id": "android-studio",
            "name": "Android Studio",

            "processes": [
                "studio.exe",
                "studio64.exe",
            ],

            "title_rules": [
                {
                    "pattern": "^(?P<project>.+?)\\s+[–-]\\s+Android Studio.*$",
                    "priority": 100,
                },
            ],

            "presence": {
                "details": "Работа в {app}",
                "state": "{project}",
                "large_image": "androidstudio",
                "large_text": "Android Studio",
            },
        },

        {
            "id": "clion",
            "name": "CLion",

            "processes": [
                "clion.exe",
                "clion64.exe",
            ],

            "title_rules": [
                {
                    "pattern": "^(?P<project>.+?)\\s+[–-]\\s+CLion.*$",
                    "priority": 100,
                },
            ],

            "presence": {
                "details": "Работа в {app}",
                "state": "{project}",
                "large_image": "clion",
                "large_text": "CLion",
            },
        },
    ],
}
