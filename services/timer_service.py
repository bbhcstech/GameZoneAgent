import time
import threading
from datetime import datetime, timezone
from commands.lock_pc import LockPC
from services.api_service import ApiService
from utils.logger import logger

class TimerService:
    def __init__(self):
        self.ends_at = None
        self.session_id = None
        self.running = False
        self.thread = None
        self.api = ApiService()
        
    def start(self, session_id, ends_at):
        self.session_id = session_id
        self.ends_at = datetime.fromisoformat(ends_at.replace("Z", "+00:00"))

        if not self.running:
            self.running = True
            threading.Thread(target=self._run,daemon=True).start()
        logger.info(f"Session timer started until {self.ends_at}")

    def extend(self, ends_at):
        self.ends_at = datetime.fromisoformat(ends_at.replace("Z", "+00:00"))
        if not self.running:
            self.running = True
            threading.Thread(target=self._run, daemon=True).start()
        logger.info(f"Session timer extended until {self.ends_at}")

    def _run(self):
        while self.running:
            remaining = self.remaining_seconds()
            if remaining <= 0:
                logger.info("Session expired - locking PC")
                self.running = False
                LockPC().execute()
                self.api.session_expired(self.session_id)
                break
            time.sleep(0.1)

    def remaining_seconds(self):
        if not self.ends_at:
            return 0
        return max(0, (self.ends_at - datetime.now(timezone.utc)).total_seconds())
    
    def stop(self):
        self.running = False
        self.ends_at = None
        self.session_id = None
        logger.info("Session timer stopped")
