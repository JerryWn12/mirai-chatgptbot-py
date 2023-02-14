# mirai-chatgptbot-py

## Usage:

1. install & launch ChatGPT API Server, recommend: [node-chatgpt-api](https://github.com/waylaidwanderer/node-chatgpt-api)
2. install & launch bot refer [mirai-console-loader](https://github.com/iTXTech/mirai-console-loader) ([mirai-api-http](https://github.com/project-mirai/mirai-api-http) should be installed!)
3. `git clone https://github.com/JerryWn12/mirai-chatgptbot-py.git`
4. `pip install graia-ariadne`
5. rename _config.example.json_ to _config.json_
   - set `bot.verifyKey` to mirai-http's verify key
   - set `bot.account` to bot's account
   - set `ChatGPT.host` to ChatGPT API Server host ('localhost' by default)
   - set `ChatGPT.port` to ChatGPT API Server port ('3000' by default)
   - if you want use https request, set `ChatGPT.useSSL` to 'ture', 'false' by default (need api server's support)
6. `python bot.py`
7. enjoy!

## Credits:

- [Ariadne](https://github.com/GraiaProject/Ariadne) - bot framework
- [node-chatgpt-api](https://github.com/waylaidwanderer/node-chatgpt-api) - ChatGPT API Server
