import json
import requests
import sys

import config

config = config.config()

if config is None:
    sys.exit()

HOST = config["ChatGPT"]["host"]
PORT = config["ChatGPT"]["port"]
USESSL = config["ChatGPT"]["useSSL"]

URL = f"http://{HOST}:{PORT}/conversation"

if USESSL:
    URL = f"https://{HOST}:{PORT}/conversation"


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
        return None
