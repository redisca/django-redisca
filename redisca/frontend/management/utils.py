import sys


class ExitHook:
    def __init__(self):
        self.code = None
        self.orig_exit = sys.exit
        sys.exit = self.exit

    def exit(self, code=0):
        self.code = code
        self.orig_exit(code)
