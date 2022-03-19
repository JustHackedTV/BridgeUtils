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

def underline(client, GUILDS):
  @client.command(name='underline', guild_ids=GUILDS)
  async def newUnderlineCommand(ctx, username):
      max = 4
      await ctx.respond("Working on it!", ephemeral=True)
      while True:
          newUsername=''
          for i in username:
              a = ''.join('_' for i in range(random.randint(0, max)))
              b = ''.join('_' for i in range(random.randint(0, max)))
              newUsername += a + i
              newUsername += b
          letters = 0
          for i in newUsername:
              letters += 1
          if not letters > 16:
              break
          else:
              max -= 1
      await ctx.respond(f"`{newUsername}`")