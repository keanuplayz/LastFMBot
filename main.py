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
    nowplaying = ""
    indexes = [1, 2, 3, 4, 5]
    req = requests.get(
        f'{lastFMBaseURL}?method=user.getrecenttracks&user={user}&api_key={lastFMAPIKey}&limit=10&format=json')  # noqa
    r = req.json()
    recent = r["recenttracks"]
    tracks = recent["track"]

    try:
        if tracks[0]["@attr"]:
            nowplaying += f"{tracks[0]['name']} | {tracks[0]['artist']['#text']}\n"  # noqa
    except KeyError:
        text += f"{tracks[0]['name']} | {tracks[0]['artist']['#text']}\n"

    for i in indexes:
        text += f"{tracks[i]['name']} | {tracks[i]['artist']['#text']}\n"

    embed = discord.Embed(
        title=f"**{user}**'s latest tracks", type="rich", color=0xE4141E, url=f"https://lastfm.com/user/{user}")  # noqa
    if not nowplaying:
        pass
    else:
        embed.add_field(name="**Now Playing**", value=nowplaying, inline=False)
    embed.add_field(name="**History**", value=text, inline=False)
    embed.set_author(
        name="LastFM", icon_url="https://www.last.fm/static/images/lastfm_avatar_twitter.52a5d69a85ac.png")  # noqa

    await ctx.respond()
    await ctx.send(content=None, embed=embed)


@slash.subcommand(base="lastfm", name="weekly", guild_ids=guild_ids, options=[
    manage_commands.create_option(
        "user", "User whose weekly graph to fetch.", 3, True)
])
async def _weekly(ctx, user):
    text = ""
    indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    req = requests.get(
        f'{lastFMBaseURL}?method=user.getweeklytrackchart&user={user}&api_key={lastFMAPIKey}&format=json'  # noqa
    )
    r = req.json()
    tracklist = r['weeklytrackchart']['track']

    for i in indexes:
        text += f"{tracklist[i]['name']} | {tracklist[i]['artist']['#text']}\n"

    embed = discord.Embed(title=f"**{user}**'s Weekly Top 10 Tracks", description=text, type="rich", color=0xE4141E, url=f"https://lastfm.com/user/{user}")  # noqa
    embed.set_author(
        name="LastFM", icon_url="https://www.last.fm/static/images/lastfm_avatar_twitter.52a5d69a85ac.png")  # noqa

    await ctx.respond()
    await ctx.send(content=None, embed=embed)

client.run(os.getenv("TOKEN"))
