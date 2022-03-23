import discord
import json
import asyncio
from KeepAlive import Reping
from discord.ui import Button, View
import random

from modmail import modMail
from error import ready
from underline import underline
from banSys import UnbanSys
from reportSys import reportSys
from torneio import TorneioCreate, TorneioGUI
from Div1Sys import ApplyDiv1
from QueroJogar import WannaPlay

#------------------------------------------------------

intents = discord.Intents.all()

client = discord.Bot(intents=intents)
GUILDS = [813781490731188224]
#GUILDS = [918582279499034664]

@client.event
async def on_ready():
    ready()
    print("[Discord API] Ready.")
    await client.change_presence(status=discord.Status.idle, activity=None)
        

@client.event
async def on_message(message):
    if "bridge" in message.content:
        if random.randint(1, 100000) == 7:
            await message.reply("PQP SEU CAGADO, TU PEGOU A CHANCE DE 1/100000 de receber esse mensagem, ou 0.001%")

@client.command(name="live", guild_ids=GUILDS)
async def LiveStream(ctx, link):
    if link.startswith('https://www.twitch.tv/'):
        await client.change_presence(activity=discord.Streaming(name=f'{link.replace("https://www.twitch.tv/", "")} está em live!', url=link))
        await ctx.respond("Seu link foi divulgado no Bot com sucesso!", ephemeral=True)
    else:
        await ctx.respond("Link da twitch **INVALIDO**.", ephemeral=True)

@client.command(name='sobre', guild_ids=GUILDS)
async def sobre(ctx):
    embed=discord.Embed(title=":bridge_at_night: Sobre eu!", description="Sou um bot morto.")
    embed.set_image(url="https://media.discordapp.net/attachments/813151767284940892/917452631415337080/About.png")
    botao = Button(label="Invite do server!", emoji="✉️", url="https://dsc.gg/bridge-brasil")
    
    view = View()
    view.add_item(botao)
    await ctx.respond(embed=embed, view=view)
    
modMail(client, GUILDS)
underline(client, GUILDS)
UnbanSys(client, GUILDS)
reportSys(client, GUILDS)
TorneioCreate(client, GUILDS)
TorneioGUI(client, GUILDS)
ApplyDiv1(client, GUILDS)
WannaPlay(client, GUILDS)

Reping()

with open("token.json", "r") as f:
    load = json.load(f)
token = load["token"]
client.run(token)
