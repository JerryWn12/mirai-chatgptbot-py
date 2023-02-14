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


def chat(msg, conversation_id="", parent_msg_id=""):

    response = requests.post(URL, json={
        "message": msg,
        "conversationId": conversation_id,
        "parentMessageId": parent_msg_id
    })

    if response.status_code == 200:
        response_data = json.loads(response.text)
        return response_data
    else:
        print(json.loads(response.text)["error"])
        return None
