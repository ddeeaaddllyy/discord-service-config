# =========================================================
# Create by ddeeaaddllyy (https://github.com/ddeeaaddllyy)
# All rights reserved
# UNDER APACHE-2.0 AND GPLv3 LICENSE
# =========================================================

class iint:
    """iint means iterable integer"""

    def __init__(self, value) -> None:
        self._int = int(value)
        self._float = float(value)
        self._string = str(self._int)

    def __iter__(self):
        for digit_char in self._string:
            yield iint(digit_char)

    def __add__(self, other):
        """Always return iter int or string or float"""

        if isinstance(other, int):
            return iint(self._int + other)

        if isinstance(other, float):
            return float(self._float + other)

        if isinstance(other, str):
            try:
                return iint(self._string + other)

            except ValueError:
                return str(self._string + other)

            except:
                raise NameError("Nameless error")

        if isinstance(other, iint):
            return self._int + other._int

        raise TypeError(f"expected type iint|int|float|str, got {type(other)} instead")

    def __radd__(self, other):
        if isinstance(other, int):
            return iint(other + self._int)

        if isinstance(other, float):
            return float(other + self._float)

        if isinstance(other, str):
            try:
                return iint(other + self._string)

            except ValueError:
                return str(other + self._string)

            except:
                raise NameError("Nameless error")

        if isinstance(other, iint):
            return other._int + self._int

        raise TypeError(f"expected type iint|int|float|str, got {type(other)} instead")

    def to_int(self):
        return self._int

    def to_str(self):
        return self._string

    def to_float(self):
        return self._float

    def __str__(self):
        return self._string

    def __int__(self):
        return self._int

    def __float__(self):
        return self._float

    def __len__(self):
        return len(self._string)

    def __repr__(self):
        return f"{self._int}"

    def __abs__(self):
        return abs(self._int)

    def __hex__(self):
        return hex(int(self._int))
        # troubles idk why

    def __pos__(self):
        return

    def __bool__(self):
        return bool(self._int)

    def __and__(self, other):
        if isinstance(other, int):
            return self._int and other

        if isinstance(other, float):
            return self._float and other

        if isinstance(other, iint):
            return self._int and other._int

        else:
            return self._int and other

