from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config as ariadne_config
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Source
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.message.parser.base import MatchContent
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


@app.broadcast.receiver("GroupMessage", decorators=[MatchContent("/reset")])
async def reset(group: Group, source: Source, member: Member):

    member_id = str(member.id)
    if member_id in convs:
        convs.pop(member_id)
        await app.send_group_message(target=group, message="已重置对话", quote=source.id)
    else:
        await app.send_group_message(target=group, message="当前无对话", quote=source.id)

# git test

app.launch_blocking()
