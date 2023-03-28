import json

from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config as ariadne_config
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Source
from graia.ariadne.message.element import Plain
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Member
from graia.ariadne.model import Group

import ChatGPT
import config

config = config.config()

VERIFY_KEY = config["bot"]["verifyKey"]
ACCOUNT = config["bot"]["account"]

app = Ariadne(
    ariadne_config(
        ACCOUNT,
        VERIFY_KEY,
    ),
)


@app.broadcast.receiver("GroupMessage", decorators=[DetectPrefix("/chat ")])
async def chat(group: Group, source: Source, member: Member, message: MessageChain):

    raw = message.as_persistent_string(binary=False, include=(Plain()))
    message = raw.removeprefix("/chat ")

    if len(message) != 0:
        convs = {}
        member_id = str(member.id)

        if member_id not in convs:
            response = ChatGPT.chat(message)
            if response != None:
                convs.update({
                    "id": response["id"]
                })
                response_msg = response["message"]
                await app.send_group_message(target=group, message=response_msg, quote=source.id)
        else:
            id = convs[member_id]
            response = ChatGPT.chat(id, message)
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
