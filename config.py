import json


def config():

    config = {}

    try:
        with open("config.json", mode="r", encoding="UTF-8") as file:
            config = json.loads(file.read())
    except OSError as err:
        print(f"read config.json failed! {str(err)}")
        return

    if not config["bot"]["verifyKey"]:
        print("please provide your bot.verifyKey in config.json")
        return
    if not config["bot"]["account"]:
        print("please provide your bot.account in config.json")
        return

    config["bot"]["account"] = int(config["bot"]["account"])

    if config["ChatGPT"]["useSSL"] in ["false", "False"]:
        config["ChatGPT"]["useSSL"] = False
    elif config["ChatGPT"]["useSSL"] in ["true", "True"]:
        config["ChatGPT"]["useSSL"] = True
    else:
        print("please set useSSL to 'true'(True) or 'false'(False)")

    config = {
        "bot": {
            "verifyKey": config["bot"]["verifyKey"],
            "account": config["bot"]["account"]
        },
        "ChatGPT": {
            "host": config["ChatGPT"]["host"] or "localhost",
            "port": config["ChatGPT"]["port"] or "3000",
            "useSSL": config["ChatGPT"]["useSSL"],
        }
    }

    return config
