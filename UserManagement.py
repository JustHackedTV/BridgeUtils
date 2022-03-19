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

def Stats(client, GUILDS):
  @client.command(name='stats', guild_ids=GUILDS)
  async def stats(ctx, user: discord.Option(discord.Member, description=None, required=False, default=None)):
          if user == None:
            user = ctx.author
          with open("elo.json", "r") as f:
              elo = json.load(f)
          if str(user.id) in elo:
              embed=discord.Embed(title=f"Nivel de {user.name}", description=f"{user.name}'s Stats:")
              embed.add_field(name="Level", value=elo[str(user.id)]["Level"])
              embed.add_field(name="Wins", value=elo[str(user.id)]["Win"])
              embed.add_field(name="Partidas Jogadas", value=elo[str(user.id)]["Partidas"])
              porcentagem=50 / 100
              final = elo[str(user.id)]["XP"] / porcentagem
              final2 = 10 - round(final/10)
              stringprogressao = f'{":blue_square:" * round(final/10)}{":white_large_square:" * final2} | XP: {elo[str(user.id)]["XP"]}'
              embed.add_field(name="Progression", value=stringprogressao)
              loses = elo[str(user.id)]["Partidas"] - elo[str(user.id)]["Win"]
              if int(loses) == 0:
                  wl = "Not Able to Calculate Win/Loss"
              else:
                  wl = elo[str(user.id)]["Win"] / loses
              embed.set_footer(text=f"Win/Loss: {wl}")
              if not user.avatar == None:
                      embed.set_thumbnail(url=user.avatar)
              else:
                  embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
              await ctx.respond(embed=embed)
          else:
              erro = reason("UserNotRegistered")
              embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
              embed.set_footer(text="ErroCode: UserNotRegistered")
              await ctx.respond(embed=embed)

def Rename(client, GUILDS):
  @client.command(name='rename', guild_ids=GUILDS)
  async def rename(ctx, *, name):
    with open("elo.json", "r") as f:
      user = json.load(f)
    if str(ctx.author.id) in user:
      user[str(ctx.author.id)]["Name"] = name
      with open("elo.json", "w") as f:
        json.dump(user, f)
      await ctx.author.edit(nick=f'{name}')
      await ctx.respond('FEITO! {}'.format(name))

def Moderar(client, GUILDS):
  @client.command(name='moderar', guild_ids=GUILDS)
  async def moderar(ctx, user: discord.Member):
      with open("mod.json", "r") as f:
          mod = json.load(f)
      if str(ctx.author.id) in mod:
          reset = Button(label="Resetar Jogador")
          blacklist = Button(label="Blacklist")
          givestats = Button(label="Modificar Stats")
          giveperm = Button(label="Adicionar Moderador")
          removeperm = Button(label="Retirar Moderador")
          fechar = Button(emoji="❌")
          
          async def reset_callback(interaction):
              if ctx.author.id == interaction.user.id:
                  with open("elo.json", "r") as f:
                      elo = json.load(f)
                  elo[str(user.id)]["Level"] = 0
                  elo[str(user.id)]["NextLevelXP"] = 10
                  elo[str(user.id)]["Win"] = 0
                  elo[str(user.id)]["Partidas"] = 0
                  elo[str(user.id)]["XP"] = 0
                  with open("elo.json","w") as f:
                      json.dump(elo, f, indent=4, sort_keys=True)
                  embed=discord.Embed(title="⚠️ Wipe", description=f"As estatisticas de {user.name}, foram resetadas.", color=0xffea00)
                  await interaction.message.edit(embed=embed)
                  await asyncio.sleep(3)
                  embed=discord.Embed(title=f"Painel de moderação para {user.name}", description="Utilize os botões abaixo para fazer sua escolha")
                  if not user.avatar == None:
                      embed.set_thumbnail(url=user.avatar)
                  else:
                      embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
                  await interaction.message.edit(embed=embed)
                  
                  
          async def blacklist_callback(interaction):
              if interaction.user.id == ctx.author.id:
                  with open("Blacklist.json", "r") as f:
                      bl = json.load(f)
                  with open("elo.json", "r") as f:
                      level = json.load(f)
                  if not str(user.id) in bl:
                      bl[str(user.id)] = "True"
                      embed=discord.Embed(title="⚠️ Blacklist", description=f"{user.name} foi colocado na blacklist.", color=0xffea00)
                      await interaction.message.edit(embed=embed)
                      if str(user.id) in level:
                          level = level.pop(str(user.id))
                          with open("elo.json", "w") as f:
                              json.dump(level, f, indent=4, sort_keys=True)
                      with open("Blacklist.json", "w") as f:
                          json.dump(bl, f, indent=4, sort_keys=True)
                      await asyncio.sleep(3)
                      embed=discord.Embed(title=f"Painel de moderação para {user.name}", description="Utilize os botões abaixo para fazer sua escolha")
          async def stats_callback(interaction):
              if interaction.user.id == ctx.author.id:
                  embed=discord.Embed(title="A possibilidade de editar stats será trazida em breve.")
                  await interaction.message.edit(embed=embed)
                  await asyncio.sleep(3)
                  embed=discord.Embed(title=f"Painel de moderação para {user.name}", description="Utilize os botões abaixo para fazer sua escolha")
                  if not user.avatar == None:
                    embed.set_thumbnail(url=user.avatar)
                  else:
                    embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
                  if not user.avatar == None:
                      embed.set_thumbnail(url=user.avatar)
                  else:
                      embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
                  await interaction.message.edit(embed=embed)
          async def perm_callback(interaction):
              if interaction.user.id == ctx.author.id:
                  with open("mod.json", "r") as f:
                      mod = json.load(f)
                  if not str(user.id) in mod:
                      mod[str(user.id)] = "True"
                      with open("mod.json", "w") as f:
                          json.dump(mod, f)
                      embed = discord.Embed(title=":partying_face: Ebá!", description=f"{user.name} agora é um moderador.", color=0xffea00)
                      await interaction.message.edit(embed=embed)
                      await asyncio.sleep(2)
                      embed=discord.Embed(title=f"Painel de moderação para {user.name}", description="Utilize os botões abaixo para fazer sua escolha")
                      if not user.avatar == None:
                          embed.set_thumbnail(url=user.avatar)
                      else:
                          embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
                      await interaction.message.edit(embed=embed)
                  else:
                      embed = discord.Embed(title=":red_circle: Erro", description=f"{user.name} já era um moderador.", color=0xff0000)
                      await interaction.message.edit(embed=embed)
                      await asyncio.sleep(2)
                      embed=discord.Embed(title=f"Painel de moderação para {user.name}", description="Utilize os botões abaixo para fazer sua escolha")
                      if not user.avatar == None:
                          embed.set_thumbnail(url=user.avatar)
                      else:
                          embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
                      await interaction.message.edit(embed=embed)
          async def removep_callback(interaction):
              if interaction.user.id == ctx.author.id:
                  with open("mod.json", "r") as f:
                      mod = json.load(f)
                  if str(user.id) in mod:
                      mod.pop(str(user.id))
                      with open("mod.json", "w") as f:
                          json.dump(mod, f)
                      embed = discord.Embed(title=":rotating_light: Mod", description=f"{user.name} deixou de ser um moderador.", color=0xffea00)
                      await interaction.message.edit(embed=embed)
                      await asyncio.sleep(2)
                      embed=discord.Embed(title=f"Painel de moderação para {user.name}", description="Utilize os botões abaixo para fazer sua escolha")
                      if not user.avatar == None:
                          embed.set_thumbnail(url=user.avatar)
                      else:
                          embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
                      await interaction.message.edit(embed=embed)
                  else:
                      embed = discord.Embed(title=":red_circle: Erro", description=f"{user.name} não é um moderador.", color=0xff0000)
                      await interaction.message.edit(embed=embed)
                      await asyncio.sleep(2)
                      embed=discord.Embed(title=f"Painel de moderação para {user.name}", description="Utilize os botões abaixo para fazer sua escolha")
                      if not user.avatar == None:
                          embed.set_thumbnail(url=user.avatar)
                      else:
                          embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
                      await interaction.message.edit(embed=embed)
          
          async def close_callback(interaction):
              if ctx.author.id == interaction.user.id:
                  await interaction.message.delete()
              
          reset.callback = reset_callback
          blacklist.callback = blacklist_callback
          givestats.callback = stats_callback
          giveperm.callback = perm_callback
          fechar.callback = close_callback
          
          view = View()
          view.add_item(reset)
          view.add_item(blacklist)
          view.add_item(givestats)
          view.add_item(giveperm)
          view.add_item(fechar)
          embed=discord.Embed(title=f"Painel de moderação para {user.name}", description="Utilize os botões abaixo para fazer sua escolha")
          if not user.avatar == None:
            embed.set_thumbnail(url=user.avatar)
          else:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
          embed.set_thumbnail(url=user.avatar)
          msg = await ctx.respond(embed=embed, view=view)
      else:
          embed = discord.Embed(title=":red_circle: Erro", description=reason("MissingPermissions"), color=0xff0000)
          embed.set_footer(text="Erro Code: MissingPermissions")
          await ctx.respond(embed=embed)

def toggle(client, GUILDS):
  @client.command(name='toggle', guild_ids=GUILDS)
  async def toggle(ctx, tipo):
      if tipo == "level":
          with open("elo.json", "r") as f:
              elo = json.load(f)
          if str(ctx.author.id) in elo:
              if elo[str(ctx.author.id)]["LevelToggle"] == "Off":
                  await ctx.author.edit(nick=f'{elo[str(ctx.author.id)]["Level"]} | {elo[str(ctx.author.id)]["Name"]}')
                  elo[str(ctx.author.id)]["LevelToggle"] = "On"
                  with open("elo.json", "w") as f:
                      json.dump(elo, f, indent=4, sort_keys=True)
              elif elo[str(ctx.author.id)]["LevelToggle"] == "On":
                  await ctx.author.edit(nick=elo[str(ctx.author.id)]["Name"])
                  elo[str(ctx.author.id)]["LevelToggle"] = "Off"
                  with open("elo.json", "w") as f:
                      json.dump(elo, f, indent=4, sort_keys=True)
          else:
              erro = reason("UserNotRegistered")
              embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
              embed.set_footer(text="ErroCode: UserNotRegistered")
              await ctx.respond(embed=embed)
      else:
          erro = reason("UnknownError")
          embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
          embed.set_footer(text="ErroCode: UserNotRegistered")
          await ctx.respond(embed=embed)

def register(client, GUILDS):
  @client.command(name='register', guild_ids=GUILDS)
  async def register(ctx, *, name):
      guild = ctx.guild
      rankedrole = discord.utils.get(guild.roles, name="Ranked")
      with open("Blacklist.json", "r") as f:
          bl = json.load(f)
      with open("elo.json", "r") as f:
          elo = json.load(f)
      if not str(ctx.author.id) in bl:
          if str(ctx.author.id) in elo:
              erro = reason("UserAlredyRegister")
              embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
              embed.set_footer(text="Error Code: UserAlredyRegister")
              msg = await ctx.respond(embed=embed)
          else:
              elo[str(ctx.author.id)] = {}
              elo[str(ctx.author.id)]["Level"] = 1
              elo[str(ctx.author.id)]["Name"] = name
              elo[str(ctx.author.id)]["LevelToggle"] = "Off"
              elo[str(ctx.author.id)]["Win"] = 0
              elo[str(ctx.author.id)]["Partidas"] = 0
              elo[str(ctx.author.id)]["XP"] = 0
              embed=discord.Embed(title=f":partying_face: | {name} foi registrado com sucesso!")
              await ctx.respond(embed=embed)
              await ctx.author.add_roles(rankedrole, reason="=register")
              with open("elo.json", "w") as f:
                  json.dump(elo, f, indent=4, sort_keys=True)