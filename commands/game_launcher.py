import os
import subprocess
from utils.logger import logger


class GameLauncher:
    def launch(self, payload):
        game_path = payload.get("game_path")

        if not game_path:
            return {
                "success": False,
                "message": "Game path not provided"
            }

        if not os.path.exists(game_path):
            return {
                "success": False,
                "message": "Game not found"
            }

        try:
            subprocess.Popen(game_path)
            logger.info(f"Game launched: {game_path}")

            return {
                "success": True,
                "message": "Game launched successfully"
            }

        except Exception as e:
            logger.info(f"Failed to launch game: {e}")

            return {
                "success": False,
                "message": str(e)
            }
