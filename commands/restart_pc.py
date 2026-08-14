import os

class RestartPC:
    def execute(self):
        os.system("shutdown /r /t 0")