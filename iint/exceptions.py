# =========================================================
# Create by ddeeaaddllyy (https://github.com/ddeeaaddllyy)
# All rights reserved
# UNDER APACHE-2.0 AND GPLv3 LICENSE
# =========================================================

class NamelessException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "NamelessException said: {0}.".format(self.message)

        return "NamelessException raised an empty error."

    def __repr__(self):
        return "NamelessException raised with '{0}' args. Raised by __repr__.".format(self.message)
