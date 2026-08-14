import time
from services.api_service import ApiService
from services.heartbeat_data import HeartbeatData  # ADD THIS

class HeartbeatService:
    def __init__(self):
        self.api = ApiService()

    def start(self, agent_key):
        while True:
            # Collect system data
            data = HeartbeatData.collect()
            
            if data:
                # Send heartbeat with system data
                self.api.heartbeat({
                    "agent_key": agent_key,
                    **data  # Merge data into payload
                })
            else:
                # Send minimal heartbeat if data collection fails
                self.api.heartbeat({"agent_key": agent_key})
            
            time.sleep(30)