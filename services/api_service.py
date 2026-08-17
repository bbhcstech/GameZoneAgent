import requests
from config import API_BASE_URL
from utils.logger import logger

class ApiService:

    def register(self, data):
        try:
            url = f"{API_BASE_URL}/agent/register"
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"registration failed: {e}")
            return None

    def heartbeat(self, data):
        try:
            url = f"{API_BASE_URL}/agent/heartbeat"
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"heartbeat failed: {e}")
            return None

    def command_ack(self, command_id, status):
        try:
            url = f"{API_BASE_URL}/agent/command/ack"
            response = requests.post(
                url,
                json={
                    "command_id": command_id,
                    "status": status
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Command ACK failed: {e}")
            return None


    def command_result(self, command_id, result):
        try:
            url = f"{API_BASE_URL}/agent/command/result"
            response = requests.post(
                url,
                json={
                    "command_id": command_id,
                    "result": result
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Command Result failed: {e}")
            return None

    def session_expired(self, session_id):
        try:
            url = f"{API_BASE_URL}/agent/session/expired"

            response = requests.post(
                url,
                json={
                    "session_id": session_id
                }
            )

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error(f"Session expiry failed: {e}")
            return None
