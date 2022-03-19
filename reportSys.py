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

def reportSys(client, GUILDS):
  @client.command(name='report', guild_ids=GUILDS)
  async def _report(ctx, user: discord.Member, reason):
      xitRole = get(ctx.guild.roles, id=943270098121162803)
      if not xitRole in user.roles:
          ReportID = ''.join(random.choice(string.ascii_uppercase+string.digits) for i in range(10))
          channelStaff = client.get_channel(943296918463844413)
          users = json.load(open("reports.json"))

          users[ReportID] = {}
          users[ReportID]['ReportedBy'] = str(ctx.author.id)
          users[ReportID]['Reported'] = str(user.id)
          users[ReportID]['Motivo'] = reason
          embed=discord.Embed(title=f'Report {user.nick}', color=0x00ff00)
          embed.add_field(name='Motivo:', value=reason)
          embed.set_thumbnail(url=user.avatar)
          embed.set_footer(text='ReportID: {}'.format(ReportID))
          await ctx.respond(embed=embed, ephemeral=True)
          await channelStaff.send(embed=embed)
          json.dump(users, open('reports.json', 'w'))
      else:
          embed=discord.Embed(title=':x: Já foi confirmado como Hacker.', color=0xff0000)
          await ctx.respond(embed=embed, ephemeral=True)

  @client.command(name='reports', guild_ids=GUILDS)
  async def _reports(ctx):
      if ctx.channel.id == 943296918463844413:
          options = []
          users = json.load(open("reports.json", 'r'))
          for i in users:
              options.append(discord.SelectOption(label=f'{i}'))

          if options == []:
              return await ctx.respond("Nenhum Report Disponivel.", ephemeral=True)
          
          view = View()
          SM = Select(options=options, max_values=1, min_values=1, placeholder='Esperando Seleção do report.')
          ACP = Button(label='Legit', emoji='✔️')
          DNY = Button(label='Hack', emoji='❌')

          report = [None]

          async def SM_callback(interaction):
              if ctx.author.id == interaction.user.id:
                  report[0] = SM.values[0]
                  embed= discord.Embed(title=report[0])
                  embed.add_field(name='Usuario Reportado', value=f"<@!{users[report[0]]['Reported']}>")
                  embed.add_field(name='Motivo', value=users[report[0]]['Motivo'])
                  await interaction.message.edit(embed=embed)

          async def Cheatin_Callback(interaction):
              if ctx.author.id == interaction.user.id:
                  if report[0] != None:
                      cheatinchat = client.get_channel(943271715771916359)
                      user = get(ctx.guild.members, id=int(users[report[0]]['Reported']))
                      xit_role = get(ctx.guild.roles, id=943270098121162803)

                      await user.add_roles(xit_role)
                      users.pop(report[0])
                      json.dump(users, open('reports.json', 'w'))
                      await interaction.message.delete()


          async def Legit_callback(interaction):
              if ctx.author.id == interaction.user.id:
                  if report[0] != None:
                      users.pop(report[0])
                      json.dump(users, open('reports.json', 'w'))
                      await interaction.message.edit(view=View())
          
          SM.callback = SM_callback
          ACP.callback = Legit_callback
          DNY.callback = Cheatin_Callback

          view.add_item(SM)
          view.add_item(ACP)
          view.add_item(DNY)

          embed=discord.Embed(title='Escolha um report...')
          await ctx.respond(embed=embed, view=view)