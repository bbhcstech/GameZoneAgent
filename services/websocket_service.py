import websocket
import time
from services.command_service import CommandService
import json
from utils.logger import logger


class WebSocketService:
    def __init__(self, url, agent_key):
        self.url = url
        self.agent_key = agent_key
        self.ws = None
        self.command_service = CommandService()

    def on_message(self, ws, message):
        data = json.loads(message)
        print(repr(data.get("event")))
        if data.get("event") == "pusher:ping":
            ws.send(json.dumps({
                "event": "pusher:pong"
            }))
            return

        if data.get("event") != "agent.command":
            return

        payload = json.loads(data["data"])
        command_id = payload.get("command_id")
        print(command_id)
        command = payload.get("command")
        command_payload = payload.get("payload")

        print(command)
        print(command_payload)

        self.command_service.execute(
            command_id,
            command,
            command_payload
        )

    def on_error(self, ws, error):
        logger.info(error)

    def on_close(self, ws, close_status_code, close_msg):
        logger.info("websocket disconnected")

    def on_open(self, ws):
        logger.info("websocket connected")
        ws.send(json.dumps({
            "event" : "pusher:subscribe",
            "data" : {
                "channel" : f"agent.{self.agent_key}"
            }
        }))

    def connect(self):
        while True:
            try:
                self.ws = websocket.WebSocketApp(
                    self.url,
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close,
                )
                self.ws.run_forever()

            except Exception as e:
                logger.info(e)

            logger.info("Reconnecting in 5 seconds")
            time.sleep(5)