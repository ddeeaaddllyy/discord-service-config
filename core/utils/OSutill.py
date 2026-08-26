import platform
import json


class OSutill:
    @staticmethod
    def __get_os_bits() -> int:
        machine = platform.machine().lower()
        if '64' in machine or machine.startswith('armv8') or machine == 'aarch64':
            return 64
        else:
            return 32

    @staticmethod
    def get_apps_json() -> dict:
        os_bits = OSutill.__get_os_bits()
        if os_bits == 64:
            with open(r"..\data\projects64.json", "r", encoding="utf-8") as file:
                return json.load(file)

        elif os_bits == 32:
            with open(r"..\data\projects32.json", "r", encoding="utf-8") as file:
                return json.load(file)

        else:
            raise OSError("Your OS is not available yet")
