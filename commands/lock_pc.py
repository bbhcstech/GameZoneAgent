import ctypes

class LockPC:
    def execute(self):
        ctypes.windll.user32.LockWorkStation()