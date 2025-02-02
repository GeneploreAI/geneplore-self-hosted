# geneplore-self-hosted
Geneplore AI's Discord bot that you can host yourself.

**NOTICE: Archived due to the depreciation of the Geneplore API as of July 1, 2024.**

To run, follow these steps:

1. Install Python 3.8 or higher.
2. Install the required packages with `pip install -r bot/requirements.txt`.
3. Create a Discord bot by following step 1 at https://discord.com/developers/docs/getting-started - When you invite the bot to your server, make sure both `applications.commands` and `bot` are checked. Also, select Administrator under Bot Permissions to avoid any errors.
4. Enable the Message Content intent in the Bot tab.
5. Copy the bot token and paste it in the `DISCORD_TOKEN` variable in `bot/bot.py`, or use environmental variables with `os.getenv()`.
6. Get your Geneplore API token by going to our [Discord server](https://geneplore.com/discord) and typing `/api` in the #gpt-bot-1 channel. Then, select API Keys from the dropdown and click Create One. Copy this key, as it won't be shown again.
7. Then, paste this key into the `GENEPLORE_KEY` variable in `bot/bot.py`, or use environmental variables with `os.getenv()`.
8. Run the bot with `python bot/bot.py`, or select Run and Debug in your favorite IDE.
9. Ensure your bot is online, in your server, and ready to use. If the bot is offline, check the console for any errors. If the bot is online but no commands appear, type `!sync` in a DM with the bot to sync the commands. It might take a few minutes, but be patient. Feel free to ask us in our [Discord server](https://geneplore.com/discord) if you need any help.
