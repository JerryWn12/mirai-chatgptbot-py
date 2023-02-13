from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Source
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Member
from graia.ariadne.model import Group

import ChatGPT
import json

VERIFY_KEY = "12345678"  # replace it with your verify key
ACCOUNT = 12345678  # replace it with your bot number


app = Ariadne(
    config(
        verify_key=VERIFY_KEY,
        account=ACCOUNT,
    ),
)


@app.broadcast.receiver("GroupMessage", decorators=[DetectPrefix("/chat-")])
async def chat(group: Group, source: Source, member: Member, message: MessageChain):
    raw_msg_str = message.as_persistent_string(binary=False)
    msg_str = raw_msg_str.removeprefix("/chat-")
    if len(msg_str) != 0:
        if msg_str.startswith("msg "):
            chat_msg = msg_str.removeprefix("msg ")
            convs = {}
            with open("conversations.json", mode="w", encoding="UTF-8") as file:
                file.write(json.dumps(convs))
            with open("conversations.json", encoding="UTF-8") as file:
                convs = json.loads(file.read())
                member_id_str = str(member.id)
                if member_id_str not in convs:
                    response = ChatGPT.chat(chat_msg)
                    if response != None:
                        convs[member_id_str] = {
                            "con_id": response["conversationId"],
                            "msg_id": response["messageId"]
                        }
                        response_msg = response["response"]
                        await app.send_group_message(target=group, message=response_msg, quote=source.id)
                else:
                    con_id = convs[member_id_str]["con_id"]
                    msg_id = convs[member_id_str]["msg_id"]
                    response = ChatGPT.chat(chat_msg, con_id, msg_id)
                    if response != None:
                        convs.update({
                            member_id_str: {
                                "con_id": response["conversationId"],
                                "msg_id": response["messageId"]
                            }
                        })
                        response_msg = response["response"]
                        await app.send_group_message(target=group, message=response_msg, quote=source.id)
            with open("conversations.json", mode="w", encoding="UTF-8") as file:
                file.write(json.dumps(convs))
        elif msg_str.startswith("reset"):
            member_id_str = str(member.id)
            convs = {}
            with open("conversations.json", mode="w", encoding="UTF-8") as file:
                file.write(json.dumps(convs))
            with open("conversations.json", mode="r", encoding="UTF-8") as file:
                convs = json.loads(file.read())
                if member_id_str in convs:
                    key = convs.pop(member_id_str, None)
                    if key is not None:
                        msg = MessageChain("reseted conversation")
                        await app.send_group_message(target=group, message=msg, quote=source.id)
                else:
                    msg = MessageChain("have no conversation current")
                    await app.send_group_message(target=group, message=msg, quote=source.id)
            with open("conversations.json", mode="w", encoding="UTF-8") as file:
                file.write(json.dumps(convs))


app.launch_blocking()
