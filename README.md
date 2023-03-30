# mirai-chatgptbot-py

## Usage

1. Install & launch [chatgpt server](https://github.com/JerryWn12/chatgpt-server)

   - `npm install @jerrywn/chatgpt-server -g`
   - `chatgpt-server --key=<OPENAI_API_KEY>`

2. Install & launch mirai bot, see [mirai](https://github.com/mamoe/mirai)

3. `git clone https://github.com/JerryWn12/mirai-chatgptbot-py.git`

4. Install [ariadne](https://github.com/GraiaProject/Ariadne): `pip install graia-ariadne`
   > Note: mirai plugin [mirai-api-http](https://github.com/project-mirai/mirai-api-http) should be installed

5. Create config.json use example json
   - `mv config.example.json config.json`

6. Config
   - Set `account` to bot's account
   - Set `verify_key` to mirai-http's verify key

7. `python bot.py`

8. Enjoy!

## Credits

- [Ariadne](https://github.com/GraiaProject/Ariadne) - mirai bot framework
