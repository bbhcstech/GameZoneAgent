from commands.game_launcher import GameLauncher
from commands.lock_pc import LockPC
from commands.kill_process import KillProcess
from commands.open_url import OpenURL
from commands.execute_cmd import ExecuteCMD
from commands.get_processes import GetProcesses
from commands.get_active_games import GetActiveGames
from commands.get_system_info import GetSystemInfo
from commands.get_idle_status import GetIdleStatus
from commands.send_popup import SendPopup
import threading
from services.api_service import ApiService
from services.timer_service import TimerService

from utils.logger import logger


class CommandService:
    def __init__(self):
        self.timer = TimerService()
    def execute(self, command_id, command, payload=None):
        if command == "launch_game":
            result = GameLauncher().launch(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "lock_pc":
            LockPC().execute()
            ApiService().command_ack(command_id, "success")

        elif command == "kill_process":
            result = KillProcess().execute(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "open_url":
            result = OpenURL().execute(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "execute_cmd":
            result = ExecuteCMD().execute(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "get_processes":
            result = GetProcesses().execute(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "get_active_games":
            result = GetActiveGames().execute(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "get_system_info":
            result = GetSystemInfo().execute(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "get_idle_status":
            result = GetIdleStatus().execute(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "send_popup":
            result = SendPopup().execute(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "alert":
            result = SendPopup().execute(payload)
            ApiService().command_ack(
                command_id,
                "success" if result["success"] else "failure"
            )
            ApiService().command_result(command_id, result)

        elif command == "start":
            print("TIMER ENDS AT:", payload["ends_at"])
            threading.Thread(target=self.timer.start,
                args=(
                    payload["session_id"],
                    payload["ends_at"]
                ),
                daemon=True
            ).start()
            print(f"✅ Session started until {payload['ends_at']}")
            ApiService().command_ack(command_id, "success")

        elif command == "extend":
            self.timer.extend(payload["ends_at"])
            print(f"✅ Session extended until {payload['ends_at']}")
            ApiService().command_ack(command_id, "success")

        elif command == "test":
            print("✅ Test command received")
            ApiService().command_ack(command_id, "success")

        elif command == "stop":
            self.timer.stop()
            ApiService().command_ack(command_id, "success")

        else:
            logger.info(f"Unknown command: {command}")
            ApiService().command_ack(command_id, "failure")