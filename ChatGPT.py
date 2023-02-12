import json
import requests

HOST = "ChatGPT_API_HOST"
PORT = "ChatGPT_API_PORT"
URL = f"http://{HOST}:{PORT}/conversation"


def chat(msg, conversation_id="", parent_msg_id=""):

    print(conversation_id)

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
