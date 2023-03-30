import json


def load_config():

    config = {}

    try:
        with open("config.json", mode="r", encoding="UTF-8") as file:
            config = json.loads(file.read())
    except OSError as err:
        print(f"read config.json failed! {str(err)}")
        exit()

    config["bot"]["account"] = int(config["bot"]["account"])

    return config
