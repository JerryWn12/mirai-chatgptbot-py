import json
import requests

from config import load_config

config = load_config()

HOST = config["chatgpt"]["host"]
PORT = config["chatgpt"]["port"]

URL = f"http://{HOST}:{PORT}/"


def chat(id, msg):
    response = ""
    if id is None:
        response = requests.post(URL, json={
            "message": msg,
        })
    else:
        response = requests.post(URL, json={
            "id": id,
            "message": msg,
        })

    if response.status_code == 200:
        response_data = json.loads(response.text)
        return response_data
    else:
        print(json.loads(response.text)["error"])
        exit()
