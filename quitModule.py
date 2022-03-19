from discord.ext import commands
from discord.ui import Button, View, Select
from error import reason, ready
from discord import ButtonStyle
from discord.utils import get
import string
import random
import asyncio
import discord
import json

def quiter(client, GUILDS):
  @client.command(name='quit', guild_ids=GUILDS)
  async def quit(ctx):
      await ctx.message.delete()
      with open("queue.json", "r") as f:
          queue = json.load(f)
      FoundInQueue = False
      for i in queue["1v1"]:
          if str(ctx.author.id) in queue["1v1"][i]:
              FoundInQueue = True
              FoundID = i
      if FoundInQueue == True:
          queue["1v1"][FoundID] = "Null"
          queue["1v1"]["InQueue"] = "False"
          with open("queue.json", "w") as f:
              json.dump(queue, f)
          embed=discord.Embed(title=":bridge_at_night: [0/2] Na fila.", description=f"Alguem saiu.", color=0x00ffe1)
          await ctx.send(embed=embed)
      else:
          msg = await ctx.send("Você não está na fila.")
          await asyncio.sleep(3)
          await msg.delete()