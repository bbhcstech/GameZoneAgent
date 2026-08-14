from services.api_service import ApiService
from services.websocket_service import WebSocketService
from services.heartbeat_service import HeartbeatService

from utils.helpers import get_hostname
from utils.storage import load_agent, save_agent
from utils.logger import logger

from config import AGENT_KEY, WEBSOCKET_URL

import threading
import signal
import sys
import time


def shutdown(signum, frame):
    print("Shutting down agent...")
    sys.exit(0)


def main():
    api = ApiService()

    agent = load_agent()

    if AGENT_KEY:
        agent_key = AGENT_KEY
        websocket_url = WEBSOCKET_URL

        print("Using configured Agent Key:", agent_key)

    elif agent:
        agent_key = agent["agent_key"]
        websocket_url = agent["websocket_url"]

        print("Using saved Agent Key:", agent_key)

    else:
        response = api.register({
            "station_name": get_hostname()
        })

        print(response)

        if not response:
            print("Agent registration failed.")
            return

        save_agent(response)

        agent_key = response["agent_key"]
        websocket_url = response["websocket_url"]

        print("Registered Agent Key:", agent_key)

    websocket = WebSocketService(
        websocket_url,
        agent_key
    )

    threading.Thread(
        target=websocket.connect,
        daemon=True
    ).start()

    heartbeat = HeartbeatService()

    threading.Thread(
        target=heartbeat.start,
        args=(agent_key,),
        daemon=True
    ).start()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info("GameZone Agent Running")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()








# from services.api_service import ApiService
# from services.websocket_service import WebSocketService
# from services.heartbeat_service import HeartbeatService

# from utils.helpers import get_hostname
# from utils.storage import load_agent, save_agent
# from utils.logger import logger

# import threading
# import signal
# import sys
# import time


# def shutdown(signum, frame):
#     print("Shutting down agent...")
#     sys.exit(0)


# def main():
#     api = ApiService()
#     agent = load_agent()

#     if agent:
#         agent_key = agent["agent_key"]
#         websocket_url = agent["websocket_url"]
#         print("Agent Key:", agent_key)
#     else:
#         response = api.register({"station_name": get_hostname()})
#         print(response)
#         save_agent(response)

#         print("Agent Key:", response["agent_key"])

#         agent_key = response["agent_key"]
#         websocket_url = response["websocket_url"]



#     websocket = WebSocketService(websocket_url, agent_key)

#     threading.Thread(
#         target=websocket.connect,
#         daemon=True
#     ).start()

#     heartbeat = HeartbeatService()

#     threading.Thread(
#         target=heartbeat.start,
#         args=(agent_key,),
#         daemon=True
#     ).start()

#     signal.signal(signal.SIGINT, shutdown)
#     signal.signal(signal.SIGTERM, shutdown)

#     logger.info("GameZone Agent Running")

#     while True:
#         time.sleep(1)


# if __name__ == "__main__":
#     main()
