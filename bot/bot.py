import discord
from discord import app_commands
from discord.app_commands import Choice
import os
import aiohttp
import json
import asyncio
import base64
import dotenv

#Load environment variables
dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GENEPLORE_KEY = os.getenv("GENEPLORE_KEY")


#Initialize bot with intents and command tree
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.AutoShardedClient(intents=intents)

tree = discord.app_commands.CommandTree(client=client)
client.tree = tree

#Headers for all calls to the Geneplore API
geneplore_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": GENEPLORE_KEY
}

#Embed functions
async def ErrorEmbed(error, message_id, user_id, command, title = "Unknown Error"):
    embed = discord.Embed(title=title, description=error + "\n\nNeed support? Join our support server at https://geneplore.com/discord", color=discord.Color.red())
    return embed


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "!sync":
        print("Syncing...")
        sync = await client.tree.sync()
        print(sync)
        await message.reply("Synced!")
        return

@tree.command(name="image", description="Generate an image from a prompt.")
@app_commands.describe(model='Choose the image generation model.')
@app_commands.choices(model=[
    Choice(name='Stable Diffusion XL v1.0', value="stable-diffusion-xl-1024-v1-0"),
    Choice(name='DALL-E 3', value="dall-e-3"),
    Choice(name='DALL-E 2', value="dall-e-2"),
    Choice(name='Anything v4', value="sd-anything-v4"),
    Choice(name='OpenJourney', value="sd-openjourney"),
    Choice(name='Kandinsky v2.1', value="kandinsky-v2")
])
async def image(interaction: discord.Interaction, model: Choice[str], prompt: str):
        await interaction.response.send_message("Generating image...")
        session = aiohttp.ClientSession()
        
        widths = {
            "stable-diffusion-xl-1024-v1-0": 1024,
            "dall-e-3": 1024,
            "dall-e-2": 1024,
            "sd-anything-v4": 512,
            "sd-openjourney": 512,
            "kandinsky-v2": 512
        }

        print(prompt)

        data = {
            "prompt": prompt,
            "model": model.value,
            "width": widths[model.value],
        }
        
        req = await session.post("https://api.geneplore.com/image/generate", headers=geneplore_headers, data=json.dumps(data))

        resp = await req.json()
        b64 = resp.get("base64")
        await session.close()
        if not b64:
            await interaction.edit_original_response(content=None, embed=await ErrorEmbed(str(resp), interaction.id, interaction.user.id, interaction.command.name))
            return
        
        image = base64.b64decode(b64)
        with open(str(interaction.id) + ".png", "wb") as f:
            f.write(image)

        await interaction.edit_original_response(content=interaction.user.mention + "\n" + prompt, attachments=[discord.File(str(interaction.id) + ".png")])

        os.remove(str(interaction.id) + ".png")
        return

client.run(DISCORD_TOKEN)