import discord
import json
import time

def WannaPlay(client, GUILDS):
    @client.event
    async def on_voice_state_update(member, before, after):
        load = json.load(open("querojogar.json", "r"))
        if time.time() > load["LastEntered"] + 120:
            if after.channel != None and len(after.channel.members) == 1 and after.channel.id == 955764408171257886:
                channel = client.get_channel(902307895096512512)
                await channel.send(f"""**Quero Jogar!**
    
    - `{member.name}` entrou no canal {after.channel.mention}
    Entre no canal caso queira jogar.
    
    ||<@&903244550557020180>||""")
                load["LastEntered"] = time.time()
                json.dump(load, open("querojogar.json", "w"))
