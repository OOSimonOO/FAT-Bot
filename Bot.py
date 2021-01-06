import discord
import re

GUILD_ID = GUILD_ID
ADMIN_ROLE = "FAT Admin"
PREFIX = "FAT!"

intents = discord.Intents.default()
intents.members = True

roles = {
    "FAT Junior" : "Herzlichen Glückwunsch an {0}. Du hast die Probezeit erfolgreich gemeistert und bist nun ein echter FAT bzw. ein echter FATy. Mega cool, das du Teil unserer FAT Crew bist!",
    "FAT Member" : "Herzlichen Glückwunsch an {0}. Du hast die Probezeit erfolgreich gemeistert und bist nun ein echter FAT bzw. ein echter FATy. Mega cool, das du Teil unserer FAT Crew bist!",
    "FAT Junior Anwärter" : "{0} willkommen in der Probezeit,viel Glück sie zu meistern.Sei respektvoll und benehm dich bitte gegenüber den anderen.",
    "FAT Anwärter" : "{0} willkommen in der Probezeit,viel Glück sie zu meistern.Sei respektvoll und benehm dich bitte gegenüber den anderen."
    }
     
class DiscordBot(discord.Client):
    
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type =discord.ActivityType.playing , name="Arbeitet füt FAT"))
        print("online")
        

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.guild.id != GUILD_ID:
            return
        if message.content.startswith(f"{PREFIX}help"):
            await message.channel.send(
                "```Hallo, ich bin der FAT Bot.\n"
                "Commands:\n"
                f"\t{PREFIX}bind channel : Bindet den Bot an einen Channel\n\n"
                "Schaut auch gerne bei meinem GitHub vorbei um den Sourcecode zu erhalten und andere Projekte von mir zu begutachten.\n"
                "https://github.com/OOSimonOO```"
                )
            
            
        if message.content.startswith(f"{PREFIX}bind"):
            if ADMIN_ROLE in [str(role) for role in message.author.roles]:
                parts = message.content.split()
                if len(parts) == 1:  
                    await message.channel.send(f"Du musst den Namen des Channels angeben")
                    return
                
                pattern = re.compile(r"<#([0-9]+)>")
                match = pattern.match(parts[1])
                if match == None:
                    await message.channel.send(f"{parts[1]} ist kein Channel")                    
                    return

                channel = discord.utils.get(message.guild.channels, id = int(match.group(1)))
                if channel == None:
                    await message.channel.send(f"{parts[1]} ist kein Channel")                    
                    return
                file = open(r"channel", "w")
                file.write(str(channel.id))
                file.close()
                await message.channel.send(f"Der Bot schreibt nun alle Nachrichten in {match.group()}")   
                
                
                
            else:
                await message.channel.send(f"Dazu hast du keine Rechte {message.author.mention}")
        
            
    
    async def on_member_update(self, before, after):
        if after.guild.id == GUILD_ID:
            file = open(r"channel", "r")
            channel_id = file.read()
            file.close()
            if channel_id == "":
                print("No channel selected")
                return
            channel = discord.utils.get(after.guild.channels, id = int(channel_id))
            if channel == None:
                print(f"No channel with id {channel_id}")
                return
            try:
                role = next((role for role in after.roles if role not in before.roles))
            except StopIteration:
                return
            if str(role) in roles:
                msg = roles[str(role)]
                msg = msg.replace("{0}", after.mention)  
                await channel.send(msg)
            
            
bot = DiscordBot(intents=intents)
bot.run(TOKEN)
