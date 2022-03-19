import discord
import asyncio
import json

def ApplyDiv1(client, GUILDS):
    @client.command(name="applydiv1", guild_ids=GUILDS)
    async def _applydiv1(ctx):
        if ctx.channel.id == 885613928858665040:
            await ctx.respond("Caregando Perguntas", ephemeral=True)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            embed1 = discord.Embed(title=f"Escreva Abaixo seu Username no minecraft:")
            embed2 = discord.Embed(title=f"Escreva o motivo de sua aplicação, caso tenho prints de sua win conta um Div 1, coloque em sua resposta (Você tem 15 minutos, caso queira mais tempo, escreva primeiro, depois envie).")
            questions = [embed1, embed2]
            answers = []
            for i in questions:
                q_msg = await ctx.send(embed=i)
                try:
                    msg = await client.wait_for('message', timeout=900.0, check=check)
                except asyncio.TimeoutError:
                    await q_msg.delete()
                    return await ctx.respond("Você falhou em responder a pergunta a tempo.")
                else:
                    await q_msg.delete()
                    answers.append(msg.content)
                    await msg.delete()
    
            JsonOb = json.load(open("Div1Apps.json", "r"))
            JsonOb[str(ctx.author.id)] = {}
            JsonOb[str(ctx.author.id)]["App"] = answers[1]
            JsonOb[str(ctx.author.id)]["IGN"] = answers[0]
            json.dump(JsonOb, open("Div1Apps.json", "w"), indent=4, sort_keys=True)