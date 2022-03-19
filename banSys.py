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

def UnbanSys(client, GUILDS):
  @client.command(name='unban', guild_ids=GUILDS)
  async def _unban(ctx, user: discord.Member):
      if ctx.channel.id == 943296918463844413:
          role = get(ctx.guild.roles, id=943270098121162803)
          await user.remove_roles(role)
      else:
          await ctx.respond('failed', ephemeral=True)

  @client.command(name="role", guild_ids=GUILDS)
  async def rolecommand(ctx,mode,player: discord.Member, role: discord.Role, reason: str):
      if ctx.author.id == 536210308591779890:
          if mode == "add":
              await player.add_roles(role, reason=reason)
              return await ctx.respond("DONE!", ephemeral=True)
          elif mode == "remove":
              await player.remove_roles(role, reason=reason)
              return await ctx.respond("DONE!", ephemeral=True)