import platform
import sys


class OSutill:
    @staticmethod
    def get_os_bits() -> int:
        machine = platform.machine().lower()
        if '64' in machine or machine.startswith('armv8') or machine == 'aarch64':
            return 64
        else:
            return 32
