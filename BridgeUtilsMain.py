from discord import player
from discord.enums import ButtonStyle
from discord.ui import Button, View 
from error import reason, ready
import string
import random
import asyncio
import discord
import json
from discord import Option

from discord.ext import commands

ids = [918582279499034664]

level1 = "<:level1:916830405284470825>"
level10 = "<:level10:916833448126189578>"
level20 = "<:level20:916836522853019688>"

client = discord.Bot()

@client.event
async def on_ready():
    ready()
    print("[Discord API] Ready.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="All Bridge Brazil Players"))

"""@client.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandNotFound):
        erro = reason("CommandNotFound")
        embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
        embed.set_footer(text="Error Code: CommandNotFound")
        await ctx.reply(embed=embed)"""

@client.command(name="sair", description="comando para sair da fila.", guild_ids=ids)
async def _sair(ctx):
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
        await ctx.respond("Você saiu da fila.", ephemeral=True)
    else:
        msg = await ctx.respond("Você não está na fila.", ephemeral=True)
        await asyncio.sleep(3)
        await msg.delete()

@client.command(name="registrar", description="comando para se registrar.", guild_ids=ids)
async def _registrar(ctx, *, name):
    with open("Blacklist.json", "r") as f:
        bl = json.load(f)
    with open("elo.json", "r") as f:
        elo = json.load(f)
    if not str(ctx.author.id) in bl:
        if str(ctx.author.id) in elo:
            erro = reason("UserAlredyRegister")
            embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
            embed.set_footer(text="Error Code: UserAlredyRegister")
            msg = await ctx.respond(embed=embed, ephemeral=True)
            await asyncio.sleep(5)
            await msg.delete()
        else:
            elo[str(ctx.author.id)] = {}
            elo[str(ctx.author.id)]["Level"] = 1
            elo[str(ctx.author.id)]["Name"] = name
            elo[str(ctx.author.id)]["LevelToggle"] = "Off"
            elo[str(ctx.author.id)]["Win"] = 0
            elo[str(ctx.author.id)]["Partidas"] = 0
            elo[str(ctx.author.id)]["XP"] = 0
            embed=discord.Embed(title=f":partying_face: | {name} foi registrado com sucesso!")
            await ctx.respond(embed=embed, ephemeral=True)
            with open("elo.json", "w") as f:
                json.dump(elo, f, indent=4, sort_keys=True)
        
        
@client.command(name="toggle", description="utilize esse comando para ativar/desativar alguns aspectos do bot.", guild_ids=ids)
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
            await ctx.respond("Feito.", ephemeral=True)
        else:
            erro = reason("UserNotRegistered")
            embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
            embed.set_footer(text="ErroCode: UserNotRegistered")
            await ctx.respond(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title=":red_circle: Erro", description=reason("TypeNotSpecified"), color=0xff0000)
        embed.set_footer(text="Error Code: TypeNotSpecified")
        ctx.respond(embed=embed, ephemeral=True)

@client.command(name="stats", description="veja os stats de um jogador ou o seu mesmo.", guild_ids=ids)
async def _stats(ctx, user:Option(
    discord.Member,
    description="um membro do discord.",
    required=False
)):
    if user == None:
        user =ctx.author
    with open("elo.json", "r") as f:
        elo = json.load(f)
    if str(user.id) in elo:
        embed=discord.Embed(title=f"{level20} Nivel de {user.name}", description=f"{user.name}'s Stats:")
        embed.add_field(name="Level", value=elo[str(user.id)]["Level"])
        embed.add_field(name="Wins", value=elo[str(user.id)]["Win"])
        embed.add_field(name="Partidas Jogadas", value=elo[str(user.id)]["Partidas"])
        porcentagem=50 / 100
        final = elo[str(user.id)]["XP"] / porcentagem
        final2 = 10 - round(final/10)
        stringprogressao = f'{":blue_square:" * round(final/10)}{":white_large_square:" * final2}'
        embed.add_field(name="Progression", value=stringprogressao)
        loses = elo[str(user.id)]["Win"] - elo[str(user.id)]["Partidas"]
        if int(loses) == 0:
            wl = "No Able to Calculate Win/Loss"
        else:
            wl = elo[str(user.id)]["Win"] / loses
        embed.set_footer(text=f"Win/Loss: {wl}")
        if not user.avatar == None:
                embed.set_thumbnail(url=user.avatar)
        else:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/813151767284940892/917600053017837638/Logo.png")
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        erro = reason("UserNotRegistered")
        embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
        embed.set_footer(text="ErroCode: UserNotRegistered")
        await ctx.respond(embed=embed, ephemeral=True)

@client.command(name="moderar", description="moderar um membro.", guild_ids=ids)
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
                await interaction.message.edit(embed=embed)
        async def givep_callback(interaction):
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
                await ctx.message.delete()
                await interaction.message.delete()
            
        reset.callback = reset_callback
        blacklist.callback = blacklist_callback
        givestats.callback = stats_callback
        giveperm.callback = givep_callback
        removeperm.callback = removep_callback
        fechar.callback = close_callback
        
        view = View()
        view.add_item(reset)
        view.add_item(blacklist)
        view.add_item(givestats)
        view.add_item(giveperm)
        view.add_item(removeperm)
        view.add_item(fechar)
        embed=discord.Embed(title=f"Painel de moderação para {user.name}", description="Utilize os botões abaixo para fazer sua escolha")
        embed.set_thumbnail(url=user.avatar)
        msg = await ctx.respond(embed=embed, view=view, ephemeral=True)
    else:
        embed = discord.Embed(title=":red_circle: Erro", description=reason("MissingPermissions"), color=0xff0000)
        embed.set_footer(text="Erro Code: MissingPermissions")
        await ctx.respond(embed=embed, ephemeral=True)

@client.command(name="jogar", description="Utilize esse comando para jogar.", guild_ids=ids)
async def play(ctx):
    if ctx.author.id == 536210308591779890:
        umvum = Button(label="1v1", style=ButtonStyle.green)
        doisvdois = Button(label="2v2", style=ButtonStyle.green)
        
        async def umcallback(interaction):
            if ctx.author.id == interaction.user.id:
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
                        await ctx.respond("Você entrou na fila.", ephemeral=True)
                        with open("queue.json", "w") as f:
                            json.dump(queue, f)
                    else:
                        embed=discord.Embed(title=f":red_circle: Erro", description="Você já está na fila.", color=0xff0000)
                        msg = await ctx.respond(embed=embed, ephemeral=True)
                else:
                    embed=discord.Embed(title=f":red_circle: Erro", description="Você não está Registrado.", color=0xff0000)
                    msg = await ctx.respond(embed=embed, ephemeral=True)
                
        async def doiscallback(interaction):
            if ctx.author.id == interaction.user.id:
                await interaction.message.delete()
                embed=discord.Embed(title=":warning: Desculpa", description="Desculpa, porém esse modo ainda não é jogavel.")
                msg = ctx.respond(embed=embed)
        
        umvum.callback = umcallback
        doisvdois.callback = doiscallback
        
        view = View()
        view.add_item(umvum)
        view.add_item(doisvdois)
        
        embed=discord.Embed(title="🌉 Bridge", description="Selecione abaixo o\nsistema de jogo que\ngostaria de jogar.", color=0x00eeff)
        await ctx.respond(embed=embed, view=view, ephemeral=True)

@client.command(name="sobre", description="informação sobre o bot.", guild_ids=ids)
async def sobre(ctx):
    embed=discord.Embed(title=":bridge_at_night: Sobre eu!", description="Olá!\nEu sou um bot criado pelo Hacked TV, eu crio partidas e duels, originalmente eu julgava tudo por elo, porém agora, utilizo um sistema de nivel, caso tenha alguma pergunta, clicke no link abaixo para saber mais sobre o motivo de eu ter cido criado!")
    embed.set_image(url="https://media.discordapp.net/attachments/813151767284940892/917452631415337080/About.png")
    botao = Button(label="Invite do server!", emoji="🎟️", url="https://dsc.gg/bridge-brasil")
    
    view = View()
    view.add_item(botao)
    await ctx.respond(embed=embed, view=view, ephemeral=True)

@client.command(name="duel", description="duelar alguem.", guild_ids=ids)
async def _duel(ctx, user: discord.Member):
    if not user.id == ctx.author.id:
        with open("elo.json", "r") as f:
            elo = json.load(f)
        if str(user.id) in elo:
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
            deny=Button(label="deny", emoji="👎", style=ButtonStyle.red)
            
            async def accept_callback(interaction):
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
            erro = reason("UserNotRegistered")
            embed = discord.Embed(title=":red_circle: Erro", description=erro, color=0xff0000)
            embed.set_footer(text="Erro Code: UserNotRegistered")
            await ctx.respond(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title=":red_circle: Erro", description=reason("InvitedThemselfs"), color=0xff0000)
        embed.set_footer(text="Erro Code: InvitedThemselfs")
        await ctx.respond(embed=embed, ephemeral=True)

@client.command(name="win", description="comando para decidir o ganhador de uma partida.")
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
                await ctx.respond(embed=embed, view=view, ephemeral=True)

with open("token.json", "r") as f:
    load = json.load(f)
token = load["token"]
client.run(token)