import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands
from dotenv import load_dotenv
import os
import requests

load_dotenv()

client = commands.Bot(command_prefix="s!", intents=discord.Intents.all())

slash = SlashCommand(client, sync_commands=True)

guild_ids = [644875385452101633]

lastFMBaseURL = "http://ws.audioscrobbler.com/2.0/"
lastFMAPIKey = os.getenv("LASTFMTOKEN")
lastFMUser = "keanucode"


@client.event
async def on_ready():
    print("Ready!")
    print(f"Logged in as {client.user.name} ({client.user.id})")


@slash.slash(name="lastfm", guild_ids=guild_ids)
async def _lastfm(ctx):
    await ctx.respond()
    await ctx.send('triggered')


@slash.subcommand(base="lastfm", name="latest", guild_ids=guild_ids, options=[
    manage_commands.create_option("user", "User whose tracks to fetch.", 3, True)  # noqa
])
async def _latest(ctx, user):
    text = ""
    indexes = [1, 2, 3, 4]
    req = requests.get(
        f'{lastFMBaseURL}?method=user.getrecenttracks&user={user}&api_key={lastFMAPIKey}&limit=5&format=json')  # noqa
    r = req.json()
    recent = r["recenttracks"]
    tracks = recent["track"]
    print(tracks[0])

    try:
        if tracks[0]["@attr"]:
            text += f"**Now Playing:** {tracks[0]['name']} | {tracks[0]['artist']['#text']}\n"  # noqa
    except KeyError:
        text += f"{tracks[0]['name']} | {tracks[0]['artist']['#text']}\n"

    for i in indexes:
        text += f"{tracks[i]['name']} | {tracks[i]['artist']['#text']}\n"
    await ctx.respond()
    await ctx.send(text)

client.run(os.getenv("TOKEN"))
