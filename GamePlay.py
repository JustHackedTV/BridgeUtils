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

def cancel(client, GUILDS):
    @client.command(name='cancelar', guild_ids=GUILDS)
    async def cancelar(ctx, gameid):
        with open("mod.json", "r") as f:
            mod = json.load(f)
        with open("games.json", "r") as f:
            games = json.load(f)
        if str(ctx.author.id) in mod:
            if gameid in games:
                pum = games[gameid]["Player1"]
                pdois = games[gameid]["Player2"]
                games.pop(gameid)
                embed=discord.Embed(title="Partida Cancelada", color=0xff0000)
                embed.add_field(name="Player 1", value=f'<@{pum}>')
                embed.add_field(name="Player 2", value=f'<@{pdois}>')
                embed.set_footer(text=f"Game ID: {gameid}")
                with open("games.json", "w") as f:
                    json.dump(games, f)
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(title=":red_circle: Erro", description="Esse jogo não existe.", color=0xff0000)
                embed.set_footer(text="Erro Code: GameNotFound")
                await ctx.reply(embed=embed)

def win(client, GUILDS):  
  @client.command(name='win', guild_ids=GUILDS)
  async def win(ctx, gameid):
      with open("mod.json", "r") as f:
          mod = json.load(f)
      with open("games.json", "r") as f:
          games = json.load(f)
      if str(ctx.author.id) in mod:
          if gameid in games:
              if games[gameid]["GameType"] == "Duel":
                  Team1 =Button(label="Player 1")
                  Team2 =Button(label="Player 2")
                  
                  async def T1C(interaction):
                      if ctx.author.id == interaction.user.id:
                          player1 = games[gameid]["Player1"]
                          player2 = games[gameid]["Player2"]
                          await interaction.message.delete()
                          embed=discord.Embed(title="Bridge :bridge_at_night:", color=0x00ffe1)
                          embed.set_footer(text=f"Game ID: {gameid}")
                          embed.add_field(name="Ganhador :trophy:", value=f'<@{player1}>')
                          await ctx.reply(embed=embed)
                          with open("elo.json", "r") as f:
                              level = json.load(f)
                          level[player1]["Partidas"] += 1
                          level[player2]["Partidas"] += 1
                          level[player1]["XP"] += 5
                          level[player1]["Win"] += 1
                          with open("elo.json", "w") as f:
                              json.dump(level, f, indent=4, sort_keys=True)
                          games.pop(gameid)
                          with open("games.json", "w") as f:
                              json.dump(games, f, indent=4, sort_keys=True)
                          with open("elo.json", "r") as f:
                              level = json.load(f)
                          if level[player1]["XP"] >= 50:
                              level[player1]["XP"] -= 50
                              level[player1]["Level"] += 1
                          with open("elo.json", "w") as f:
                              json.dump(level, f, indent=4, sort_keys=True)
                  async def T2C(interaction):
                      if ctx.author.id == interaction.user.id:
                          player1 = games[gameid]["Player1"]
                          player2 = games[gameid]["Player2"]
                          await interaction.message.delete()
                          embed=discord.Embed(title="Bridge :bridge_at_night:", color=0x00ffe1)
                          embed.set_footer(text=f"Game ID: {gameid}")
                          embed.add_field(name="Ganhador :trophy:", value=f'<@{player2}>')
                          await ctx.reply(embed=embed)
                          with open("elo.json", "r") as f:
                              level = json.load(f)
                          level[player2]["Partidas"] += 1
                          level[player1]["Partidas"] += 1
                          level[player2]["XP"] += 10
                          level[player2]["Win"] += 1
                          with open("elo.json", "w") as f:
                              json.dump(level, f, indent=4, sort_keys=True)
                          games.pop(gameid)
                          with open("games.json", "w") as f:
                              json.dump(games, f, indent=4, sort_keys=True)
                          with open("elo.json", "r") as f:
                              level = json.load(f)
                          if level[player1]["XP"] >= 50:
                              level[player1]["XP"] -= 50
                              level[player1]["Level"] += 1
                          with open("elo.json", "w") as f:
                              json.dump(level, f, indent=4, sort_keys=True)
                      
                  Team1.callback = T1C
                  Team2.callback = T2C
                  
                  view=View()
                  view.add_item(Team1)
                  view.add_item(Team2)
                  
                  embed=discord.Embed(title="Bridge :bridge_at_night:", color=0x00ffe1)
                  embed.set_footer(text=f"Game ID: {gameid}")
                  embed.add_field(name="Ganhador :trophy:", value=f'Selecione o ganhador.')
                  embed.add_field(name="Player 1", value=f'<@{games[gameid]["Player1"]}>')
                  embed.add_field(name="Player 2", value=f'<@{games[gameid]["Player2"]}>')
                  await ctx.reply(embed=embed, view=view)
              elif games[gameid]["GameType"] == "1v1":
                  Team1 =Button(label="Player 1")
                  Team2 =Button(label="Player 2")
                  
                  async def T1C(interaction):
                      if ctx.author.id == interaction.user.id:
                          player1 = games[gameid]["Player1"]
                          player2 = games[gameid]["Player2"]
                          await interaction.message.delete()
                          embed=discord.Embed(title="Bridge :bridge_at_night:", color=0x00ffe1)
                          embed.set_footer(text=f"Game ID: {gameid}")
                          embed.add_field(name="Ganhador :trophy:", value=f'<@{player1}>')
                          await ctx.reply(embed=embed)
                          with open("elo.json", "r") as f:
                              level = json.load(f)
                          level[player1]["Partidas"] += 1
                          level[player2]["Partidas"] += 1
                          level[player1]["XP"] += 5
                          level[player1]["Win"] += 1
                          with open("elo.json", "w") as f:
                              json.dump(level, f, indent=4, sort_keys=True)
                          games.pop(gameid)
                          with open("games.json", "w") as f:
                              json.dump(games, f, indent=4, sort_keys=True)
                          with open("elo.json", "r") as f:
                              level = json.load(f)
                          if level[player1]["XP"] >= 50:
                              level[player1]["XP"] -= 50
                              level[player1]["Level"] += 1
                          with open("elo.json", "w") as f:
                              json.dump(level, f, indent=4, sort_keys=True)
                  async def T2C(interaction):
                      if ctx.author.id == interaction.user.id:
                          player1 = games[gameid]["Player1"]
                          player2 = games[gameid]["Player2"]
                          await interaction.message.delete()
                          embed=discord.Embed(title="Bridge :bridge_at_night:", color=0x00ffe1)
                          embed.set_footer(text=f"Game ID: {gameid}")
                          embed.add_field(name="Ganhador :trophy:", value=f'<@{player2}>')
                          await ctx.reply(embed=embed)
                          with open("elo.json", "r") as f:
                              level = json.load(f)
                          level[player2]["Partidas"] += 1
                          level[player1]["Partidas"] += 1
                          level[player2]["XP"] += 5
                          level[player2]["Win"] += 1
                          with open("elo.json", "w") as f:
                              json.dump(level, f, indent=4, sort_keys=True)
                          games.pop(gameid)
                          with open("games.json", "w") as f:
                              json.dump(games, f, indent=4, sort_keys=True)
                          with open("elo.json", "r") as f:
                              level = json.load(f)
                          if level[player1]["XP"] >= 50:
                              level[player1]["XP"] -= 50
                              level[player1]["Level"] += 1
                          with open("elo.json", "w") as f:
                              json.dump(level, f, indent=4, sort_keys=True)
                      
                  Team1.callback = T1C
                  Team2.callback = T2C
                  
                  view=View()
                  view.add_item(Team1)
                  view.add_item(Team2)
                  
                  embed=discord.Embed(title="Bridge :bridge_at_night:", color=0x00ffe1)
                  embed.set_footer(text=f"Game ID: {gameid}")
                  embed.add_field(name="Ganhador :trophy:", value=f'Selecione o ganhador.')
                  embed.add_field(name="Player 1", value=f'<@{games[gameid]["Player1"]}>')
                  embed.add_field(name="Player 2", value=f'<@{games[gameid]["Player2"]}>')

def duel(client, GUILDS):
    @client.command(name='duel', guild_ids=GUILDS)
    async def duel(ctx, user: discord.Member):
        if not user.id == ctx.author.id:
            with open("elo.json", "r") as f:
                elo = json.load(f)
            if str(user.id) in elo:
                if str(ctx.author.id) in elo:
                    with open("duels.json", "r") as f:
                        d = json.load(f)
                    running = True
                    while running == True:
                        code = ''.join(random.choice(string.ascii_uppercase) for i in range(10))
                        if not code in d:
                            running = False
                    d[code] = {}
                    d[code]["Requester"] = str(ctx.author.id)
                    d[code]["Requested"] = str(user.id)
                    d[code]["Status"] = "Pending"
                    with open("duels.json", "w") as f:
                        json.dump(d, f, indent=4, sort_keys=True)
                        
                    accept=Button(label="Accept", emoji="👍", style=ButtonStyle.green)
                    deny=Button(label="Deny", emoji="👎", style=ButtonStyle.red)
                    
                    async def accept_callback(interaction):
                        if user.id == interaction.user.id:
                            with open("games.json", "r") as f:
                                games = json.load(f)
                            Running = True
                            while Running == True:
                                GameID = ''.join(random.choice(string.digits + string.ascii_uppercase) for i in range(10))
                                if GameID not in games:
                                    Running = False
                            games[GameID] = {}
                            games[GameID]["Player1"] = str(ctx.author.id)
                            games[GameID]["Player2"] = str(user.id)
                            games[GameID]["GameType"] = "Duel"
                            embed=discord.Embed(title="Bridge 🌉", description=f"Game ID: {GameID}", color=0x00ff00)
                            embed.add_field(name="Player 1", value=ctx.author.mention)
                            embed.add_field(name="Player 2", value=user.mention)
                            embed.set_footer(text="Gamemode: Duel")
                            with open("games.json", "w") as f:
                                json.dump(games, f)
                            await ctx.send(embed=embed)
                            await interaction.message.delete()
                
                    async def deny_callback(interaction):
                        if interaction.user.id == user.id:
                            await interaction.message.delete()
                            embed=discord.Embed(title="Duel Negado", description=f"{user.name} negou seu pedido de duelo")
                            await ctx.author.send(embed=embed)
                            with open("duels.json", "r") as f:
                                d = json.load(f)
                            d.pop(code)
                            with open("duels.json", "w") as f:
                                json.dump(d, f, indent=4, sort_keys=True)               
                    
                    accept.callback = accept_callback
                    deny.callback = deny_callback
                    
                    view=View()
                    view.add_item(accept)
                    view.add_item(deny)
                    
                    embed=discord.Embed(title=":crossed_swords: Duel", description=f"{user.mention}, você foi convidado para um duelo contra {ctx.author.mention}, clicke no botão **accept** para começar o duelo. O convite será deletado daqui 5 minutos.", color=0xffea00)
                    await ctx.send(user.mention, embed=embed, view=view)
                else:
                    erro = "Você não está registrado, utilize **b!register** para se registrar."
                    embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
                    embed.set_footer(text="Erro Code: UserNotRegistered")
                    await ctx.respond(embed=embed)  
            else:
                erro = "Você não está registrado, utilize **b!register** para se registrar."
                embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
                embed.set_footer(text="Erro Code: UserNotRegistered")
                await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title=":red_circle: Erro", description="Você não pode convidar você mesmo.", color=0xff0000)
            embed.set_footer(text="Erro Code: InvitedThemselfs")
            await ctx.respond(embed=embed)

def play(client, GUILDS):
    @client.command(name='play')
    async def play(ctx):
        with open("elo.json", "r") as f:
            elo = json.load(f)
        if str(ctx.author.id) in elo:
            umvum = Button(label="1v1", style=ButtonStyle.green)
            doisvdois = Button(label="Vindo Embreve", style=ButtonStyle.red)
            fecharmenu = Button(emoji="❌")
            
            async def umcallback(interaction):
                if ctx.author.id == interaction.user.id:
                    await interaction.message.delete()
                    user = interaction.user
                    with open("elo.json" , "r") as f:
                        level = json.load(f)
                    with open("games.json", "r") as f:
                        games = json.load(f)
                    with open("queue.json", "r") as f:
                        queue = json.load(f)
                    if str(user.id) in level:
                        if not queue["1v1"]["Player"] == str(user.id):
                            if queue["1v1"]["InQueue"] == "True":
                                Running = True
                                while Running == True:
                                    GameID = ''.join(random.choice(string.digits + string.ascii_uppercase) for _ in range(10))
                                    if GameID not in games:
                                        Running = False
                                games[GameID] = {}
                                games[GameID]["Player1"] = queue["1v1"]["Player"]
                                games[GameID]["Player2"] = str(user.id)
                                games[GameID]["GameType"] = "1v1"
                                embed=discord.Embed(title="Bridge :bridge_at_night:", description=f"Game ID: {GameID}", color=0x00ff00)
                                embed.set_footer(text="Gamemode: 1v1")
                                Player2Stats = queue["1v1"]["Player"]
                                embed.add_field(name="Player 1", value=f"<@{Player2Stats}>", inline=True)
                                embed.add_field(name="Player 2", value=f"{user.mention}", inline=True)
                                queue["1v1"]["Player"] = "Null"
                                queue["1v1"]["InQueue"] = "False"
                                await ctx.send(embed=embed)
                                with open("games.json", "w") as f:
                                    json.dump(games, f)
                                with open("queue.json", "w") as f:
                                    json.dump(queue, f)
                            else:
                                queue["1v1"]["Player"] = str(user.id)
                                queue["1v1"]["InQueue"] = "True"
                            with open("queue.json", "w") as f:
                                json.dump(queue, f)
                            embed=discord.Embed(title=":bridge_at_night: [1/2] Na fila.", description=f"Alguem entrou.", color=0x00ffe1)
                            await ctx.send(embed=embed)
                            with open("queue.json", "w") as f:
                                json.dump(queue, f)
                        else:
                            embed=discord.Embed(title=f":red_circle: Erro", description="Você já está na fila.", color=0xff0000)
                            msg = await ctx.send(embed=embed)
                            await asyncio.sleep(3)
                            await msg.delete()
                    else:
                        embed=discord.Embed(title=f":red_circle: Erro", description="Você não está Registrado.", color=0xff0000)
                        msg = await ctx.send(embed=embed)
                        await asyncio.sleep(3)
                        await msg.delete()
                    
            async def doiscallback(interaction):
                if ctx.author.id == interaction.user.id:
                    await interaction.message.delete()
                    embed=discord.Embed(title=":warning: Desculpa", description="Desculpa, porém esse modo ainda não é jogavel.")
                    msg = ctx.send(embed=embed)
                    await msg.delete()
            
            async def CloseMenuCallback(interaction):
                if ctx.author.id == interaction.user.id:
                    await interaction.message.delete()

            umvum.callback = umcallback
            doisvdois.callback = doiscallback
            fecharmenu.callback = CloseMenuCallback
            
            view = View()
            view.add_item(umvum)
            view.add_item(fecharmenu)
            
            embed=discord.Embed(title="🌉 Bridge", description="Selecione abaixo o\nsistema de jogo que\ngostaria de jogar.", color=0x00eeff)
            await ctx.respond(embed=embed, view=view)