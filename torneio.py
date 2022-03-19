from discord.ext import commands
from discord.ui import Button, View, Select
from error import reason, ready
from discord import ButtonStyle
from discord.utils import get
import math
import string
import random
import asyncio
import discord
import json

def Log2(x):
    if x == 0:
        return False
 
    return (math.log10(x) /
            math.log10(2))

def isPowerOfTwo(n):
    if n == 0:
        return False
    return (math.ceil(Log2(n)) ==
            math.floor(Log2(n)))

def TorneioCreate(client, GUILDS):
  @client.command(name='torneio', guild_ids=GUILDS)
  async def _torneio(ctx):
      await ctx.respond("Carregando perguntas.", ephemeral=True)
      q_msg = await ctx.send("Carregando perguntas.")
      tor = json.load(open("torneios.json", 'r'))
      while True:
          TorneioID = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(10))
          if not TorneioID in tor:
              break
      
      embed1 = discord.Embed(title='Quantos times terá em seu torneio? (numero deve ser divisivel por 2.)')
      embed2 = discord.Embed(title='Quantos players por time?')
      embed3 = discord.Embed(title='Qual será o prémio? (Coloquei "null" para não ter um prémio.)')
      embed4 = discord.Embed(title='O nome do torneio:')
      embed5 = discord.Embed(title='Descrição do torneio:')
      embed6 = discord.Embed(title='Requerimento de nivel para entrar: (Coloquei "null" para não tenha um requerimento)')

      questions = [embed1, embed2, embed3, embed4, embed5, embed6]

      answers = []

      def check(m):
          return ctx.author == m.author and ctx.channel == m.channel
      
      for q in questions:
          await q_msg.edit(embed=q, content='')
          try:
              msg = await client.wait_for('message', timeout=300.0, check=check)
          except asyncio.TimeoutError:
              q_msg.delete()
              return await ctx.send("Failed to send message.")
          else:
              answers.append(msg.content)
              await msg.delete()

      await q_msg.delete()
      
      TorneioEmbed = discord.Embed(title=answers[3], description=answers[4])

      if math.ceil(math.log10(int(answers[0])) / math.log10(2)) == math.floor(math.log10(int(answers[0])) / math.log10(2)):
          TorneioEmbed.add_field(name='Times:', value=int(answers[0]))
      else:
          return await ctx.respond("Você não colocou uma numero de Times Valido", ephemeral=True)

      TorneioEmbed.add_field(name='Modo:', value=f'{answers[1]}v{answers[1]}')

      if answers[2] != 'null':
          TorneioEmbed.add_field(name='Premio', value=answers[2])

      TorneioEmbed.set_footer(text=f"TorneioID: {TorneioID}")

      TorneioEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/943795276160847882/943857336664088688/TurnyBridgeUtils.png')
      
      tor[TorneioID] = {}
      tor[TorneioID]['InfoTorneio'] = {}
      tor[TorneioID]['InfoTorneio']['Owner'] = ctx.author.id
      tor[TorneioID]['InfoTorneio']['Name']=answers[3]
      tor[TorneioID]['InfoTorneio']['Description']=answers[4]
      tor[TorneioID]['InfoTorneio']['Mode']=f'{answers[1]}v{answers[1]}'
      tor[TorneioID]['InfoTorneio']['LevelReq']=0
      tor[TorneioID]['InfoTorneio']['MaxTeams']=int(answers[0])
      tor[TorneioID]['InfoTorneio']['Teams'] = []
      tor[TorneioID]['InfoTorneio']['Moderadores'] = [ctx.author.id]
      tor[TorneioID]['InfoTorneio']['Status'] = "Not Started"
      tor[TorneioID]['Matches'] = []

      json.dump(tor, open("torneios.json", "w"), indent=4, sort_keys=True)
      

      await ctx.send(embed=TorneioEmbed)

def TorneioGUI(client, GUILDS):
  @client.command(name='torneios', guild_ids=GUILDS)
  async def meus_torneios(ctx):
      Matches=[]
      options= []
      operationOptions = [discord.SelectOption(label="Começar"), discord.SelectOption(label="Acabar"), discord.SelectOption(label="Banir Player"), discord.SelectOption(label="Configurações")]
      torneio = [None]
      actionsSelect = [None]
      view=View()
      embed=discord.Embed(title='Escolha seu torneio:', color=0x00fff0)
      tor = json.load(open("torneios.json","r"))
      for i in tor:
          if tor[i]['InfoTorneio']['Owner'] == ctx.author.id:
              options.append(discord.SelectOption(label=f'{i}'))

      if options == []:
          return await ctx.respond("Você não tem nenhum torneio.", ephemeral=True)
      
      SM = Select(options=options, max_values=1, min_values=1, placeholder='Esperando Seleção do seu campeonato...')
      startButton = Button(label="Fazer", style=discord.ButtonStyle.success)
      cancelButton = Button(label="Fechar", style=discord.ButtonStyle.red)
      action = Select(options=operationOptions, max_values=1, min_values=1, placeholder='Escolha sua ação...')

      async def action_callback(interaction):
          if interaction.user.id == ctx.author.id:
              actionsSelect[0] = action.values[0]

      action.callback = action_callback

      async def cancel_callback(interaction):
          startButton.disabled=True
          cancelButton.disabled=True
          action.disabled=True
          await interaction.message.edit(content="Finalizado.", embed=None, view=View())

      cancelButton.callback = cancel_callback

      async def start_callback(interaction):
          if interaction.user.id == ctx.author.id:
              if actionsSelect[0] == 'Começar':
                  teamsS = []
                  teams = tor[torneio[0]]['InfoTorneio']['Teams']
                  count = 0
                  for i in teams:
                      teamsS.append(i)
                      count += 1
                  if isPowerOfTwo(count) and tor[torneio[0]]['InfoTorneio']['Status'] == "Not Started":
                      msg = ''
                      for i in range(int(count/2)):
                          matchInfo = {}
                          Player1 = random.choice(teams)
                          matchInfo["Player1"] = Player1
                          teams.remove(Player1)
                          Player2 = random.choice(teams)
                          matchInfo["Player2"] = Player2
                          teams.remove(Player2)
                          matchInfo["MatchID"] = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(10))
                          tor[torneio[0]]["Matches"].append(matchInfo)
                          msg += f'**GAME ID:** ||{matchInfo["MatchID"]}||\n**Team 1:** {Player1}\n**Team 2:** {Player2}\n'
                      tor[torneio[0]]['InfoTorneio']['Teams'] = teamsS
                      tor[torneio[0]]['InfoTorneio']['Status'] = "Started"
                      json.dump(tor, open('torneios.json', "w"), indent=4, sort_keys=True)
                      await interaction.message.edit(content=msg, embed=None, view=None)
              elif actionsSelect[0] == 'Configurações':
                  print("FORA DE FUNCIONAMENTO.")

      startButton.callback = start_callback
      
      async def SM_callback(interaction):
          if interaction.user.id == ctx.author.id:
              embed=discord.Embed(title=f'{tor[SM.values[0]]["InfoTorneio"]["Name"]}',description=f'{tor[SM.values[0]]["InfoTorneio"]["Description"]}')
              embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/943795276160847882/943857336664088688/TurnyBridgeUtils.png')
              torneio[0] = SM.values[0]
              NewView = View()
              NewView.add_item(action)
              NewView.add_item(startButton)
              NewView.add_item(cancelButton)
              await interaction.message.edit(view=NewView, embed=embed)
      
      SM.callback=SM_callback

      view.add_item(SM)

      await ctx.respond(view=view, embed=embed)