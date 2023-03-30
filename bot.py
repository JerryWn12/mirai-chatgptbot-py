from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config as ariadne_config
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Source
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Member
from graia.ariadne.model import Group
from graia.ariadne.connection.config import HttpClientConfig
from graia.ariadne.connection.config import WebsocketClientConfig

import chatgpt

from config import load_config

config = load_config()

ACCOUNT = config["bot"]["account"]
VERIFY_KEY = config["bot"]["verify_key"]
HTTP_HOST = config["mirai"]["http"]["host"]
HTTP_PORT = config["mirai"]["http"]["port"]
WS_HOST = config["mirai"]["ws"]["host"]
WS_PORT = config["mirai"]["ws"]["port"]

app = Ariadne(
    ariadne_config(
        ACCOUNT,
        VERIFY_KEY,
        HttpClientConfig(f"http://{HTTP_HOST}:{HTTP_PORT}/"),
        WebsocketClientConfig(f"http://{WS_HOST}:{WS_PORT}/")
    ),
)

convs = {}


@app.broadcast.receiver("GroupMessage", decorators=[DetectPrefix("/chat ")])
async def chat(group: Group, source: Source, member: Member, message: MessageChain):

    raw = message.as_persistent_string(binary=False)
    message = raw.removeprefix("/chat ")

    if len(message) != 0:
        member_id = str(member.id)
        if member_id not in convs:
            response = chatgpt.chat("", message)
            if response != None:
                convs[member_id] = response["id"]
                response_msg = response["message"]
                await app.send_group_message(target=group, message=response_msg, quote=source.id)
        else:
            id = convs[member_id]
            response = chatgpt.chat(id, message)
            if response != None:
                response_msg = response["message"]
                await app.send_group_message(target=group, message=response_msg, quote=source.id)

    # elif len(msg_str) != 0 and msg_str == "reset":
    #     convs = {}
    #     with open("conversations.json", mode="w", encoding="UTF-8") as file:
    #         file.write(json.dumps(convs))
    #     with open("conversations.json", mode="r", encoding="UTF-8") as file:
    #         convs = json.loads(file.read())
    #         member_id_str = str(member.id)
    #         if member_id_str in convs:
    #             key = convs.pop(member_id_str, None)
    #             if key is not None:
    #                 msg = MessageChain("reseted conversation")
    #                 await app.send_group_message(target=group, message=msg, quote=source.id)
    #         else:
    #             msg = MessageChain("no conversation current")
    #             await app.send_group_message(target=group, message=msg, quote=source.id)
    #     with open("conversations.json", mode="w", encoding="UTF-8") as file:
    #         file.write(json.dumps(convs))


app.launch_blocking()
