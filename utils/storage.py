import json
import os

FILE_NAME = "agent.json"

def save_agent(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file)

def load_agent():
    if not os.path.exists(FILE_NAME):
        return None

    with open(FILE_NAME, "r") as file:
        return json.load(file)