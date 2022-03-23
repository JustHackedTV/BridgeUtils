import discord
import asyncio
import json

def ApplyDiv1(client, GUILDS):
    @client.command(name="apply", description="comando para aplicar pra divisão 1", guild_ids=GUILDS)
    async def app_(ctx):
        modal = discord.ui.Modal(title="Aplicação para Divisão 1:")
        modal.add_item(discord.ui.InputText(label=f"Escreva seu nick na caixa abaixo:", style=discord.InputTextStyle.short, placeholder="IGN"))
        modal.add_item(discord.ui.InputText(label="Escreva o motivo para você ser Divisão 1:", style=discord.InputTextStyle.long))
        async def callback(interaction):
            resposta1 = modal.children[0].value
            resposta2 = modal.children[1].value
            load = json.load(open("Div1Apps.json", "r"))
            load[str(ctx.author.id)] = {}
            load[str(ctx.author.id)]["IGN"] = resposta1
            load[str(ctx.author.id)]["Motivo"] = resposta2
            json.dump(load, open("Div1Apps.json", "w"), indent=4, sort_keys=True)
            await interaction.response.send_message(f""":tada: **Sucesso!**
`{ctx.author.name}` sua aplicação foi enviada com sucesso!""", ephemeral=True)
        modal.callback = callback
        await ctx.send_modal(modal)
