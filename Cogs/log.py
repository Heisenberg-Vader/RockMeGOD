import discord
from discord.ext import commands
import asyncio
import json
import random
from discord.utils import get
from dhooks import Webhook

colors = [0x1abc9c, 0xffff00, 0xe90000, 0x00e931, 0x0057e9, 0x00ffff, 0xf3f3f3, 0xff0091]

color = random.choice(colors)

class Log(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if isinstance(msg.channel, discord.channel.DMChannel):
            return

        if msg.author.bot:
            return

        if str(msg.guild.id) not in logs:
            return

        elif logs[str(msg.guild.id)]["log"] == "false":
            return

        else:
            c_id = int(logs[str(msg.guild.id)]["log"]) 
            channel = self.client.get_channel(c_id)

            em = discord.Embed(color = color, timestamp = msg.created_at)

            em.set_author(name = msg.author, icon_url = msg.author.avatar_url)

            em.add_field(name = f"Message deleted in #{msg.channel.name}", value = msg.content)

            wlist = []
            for w in await channel.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")
            
        
    @commands.Cog.listener()
    async def on_message_edit(self, msg1, msg2):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if isinstance(msg1.channel, discord.channel.DMChannel):
            return

        if msg1.author.bot:
            return        

        if str(msg1.guild.id) not in logs:
            return

        elif logs[str(msg1.guild.id)]["log"] == "false":
            return

        elif msg1.content == msg2.content:
            return

        else:
            c_id = int(logs[str(msg1.guild.id)]["log"]) 
            channel = self.client.get_channel(c_id)

            em = discord.Embed(description = f"**<a:rockthonkspin:795681585604853800> Message edited in #{msg1.channel.name} **",color = color, timestamp = msg1.created_at)

            em.set_author(name = msg1.author, icon_url = msg1.author.avatar_url)

            em.add_field(name = f"Before:", value = msg1.content, inline = False)

            em.add_field(name = f"After:", value = msg2.content, inline = False)

            wlist = []
            for w in await channel.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if str(channel.guild.id) not in logs:
            return

        elif logs[str(channel.guild.id)]["log"] == "false":
            return

        else:
            c_id = int(logs[str(channel.guild.id)]["log"]) 
            channel_1 = self.client.get_channel(c_id)

            em = discord.Embed(description = f":new: **New channel created: #{channel.name}**", color = color, timestamp = channel.created_at)
            
            async for entry in channel.guild.audit_logs(limit=5):
                if entry.action == discord.AuditLogAction.channel_create:
                    em.set_author(name = entry.user, icon_url = entry.user.avatar_url)

                    em.add_field(name="Channel Created By:", value=f"{entry.user.mention}")

                    break

            em.add_field(name = "Category:",value = channel.category, inline = False)

            wlist = []
            for w in await channel_1.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel_1.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if str(channel.guild.id) not in logs:
            return

        elif logs[str(channel.guild.id)]["log"] == "false":
            return

        else:
            c_id = int(logs[str(channel.guild.id)]["log"]) 
            channel_1 = self.client.get_channel(c_id)

            em = discord.Embed(description = f"<:rockcross:794808762501824542> **Channel deleted: #{channel.name}**", color = color, timestamp = channel.created_at)
            
            async for entry in channel.guild.audit_logs(limit=5):
                if entry.action == discord.AuditLogAction.channel_create:
                    em.set_author(name = entry.user, icon_url = entry.user.avatar_url)

                    em.add_field(name="Channel deleted By:", value=f"{entry.user.mention}")

                    break

            em.add_field(name = "Category:",value = channel.category, inline = False)

            wlist = []
            for w in await channel_1.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel_1.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if str(before.guild.id) not in logs:
            return

        elif logs[str(before.guild.id)]["log"] == "false":
            return

        else:
            c_id = int(logs[str(before.guild.id)]["log"]) 
            channel_1 = self.client.get_channel(c_id)

            em = discord.Embed(description = f"<a:rockthonkspin:795681585604853800> **Channel edited:**", color = color, timestamp = before.created_at)

            if before.name != after.name:
                em.add_field(name = "**Name Change of channel:**", value = f"\n**{before.name}** --> **{after.name}**")
            
            else:
                return

            wlist = []
            for w in await channel_1.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel_1.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if str(role.guild.id) not in logs:
            return

        elif logs[str(role.guild.id)]["log"] == "false":
            return

        else:
            c_id = int(logs[str(role.guild.id)]["log"]) 
            channel_1 = self.client.get_channel(c_id)

            em = discord.Embed(description = f"**New role created:**\n`{role.name}`", color = color, timestamp = role.created_at)
            
            async for entry in role.guild.audit_logs(limit=5):
                if entry.action == discord.AuditLogAction.role_create:
                    em.set_author(name = entry.user, icon_url = entry.user.avatar_url)

                    em.add_field(name="Role Created By:", value=f"{entry.user.mention}")

                    break

            em.add_field(name = "Color:", value = f"{role.color}")

            wlist = []
            for w in await channel_1.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel_1.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")    

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if str(role.guild.id) not in logs:
            return

        elif logs[str(role.guild.id)]["log"] == "false":
            return

        else:
            c_id = int(logs[str(role.guild.id)]["log"]) 
            channel_1 = self.client.get_channel(c_id)

            em = discord.Embed(description = f"**Role deleted:**\n`{role.name}`", color = color, timestamp = role.created_at)
            
            async for entry in role.guild.audit_logs(limit=5):
                if entry.action == discord.AuditLogAction.role_create:
                    em.set_author(name = entry.user, icon_url = entry.user.avatar_url)

                    em.add_field(name="Role deleted By:", value=f"{entry.user.mention}")

                    break

            em.add_field(name = "Color:", value = f"{role.color}")

            wlist = []
            for w in await channel_1.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel_1.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")   

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if str(before.guild.id) not in logs:
            return

        elif logs[str(before.guild.id)]["log"] == "false":
            return

        else:
            c_id = int(logs[str(before.guild.id)]["log"]) 
            channel_1 = self.client.get_channel(c_id)

            em = discord.Embed(description = f"<a:rockthonkspin:795681585604853800> **Role edited:**", color = color, timestamp = before.created_at)

            if before.name != after.name:
                em.add_field(name = "**Name Change of role:**", value = f"\n**{before.name}** --> **{after.name}**")

            elif before.color != after.color:
                em.add_field(name = "**Color Change of role:**", value = f"{before.color} --> {after.color}")
            
            else:
                return

            wlist = []
            for w in await channel_1.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel_1.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")   

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if str(before.id) not in logs:
            return

        elif logs[str(before.id)]["log"] == "false":
            return

        else:
            c_id = int(logs[str(before.id)]["log"]) 
            channel_1 = self.client.get_channel(c_id)

            em = discord.Embed(description = f"<a:rockthonkspin:795681585604853800> **Server edited:**", color = color, timestamp = before.created_at)

            if before.name != after.name:
                em.add_field(name = "**Name Change of server:**", value = f"\n**{before.name}** --> **{after.name}**")

            elif before.icon != after.icon:
                em.add_field(name = "Icon Update:", value  = "Given below is new icon!")
                em.set_image(url = after.icon_url)
            
            else:
                return

            wlist = []
            for w in await channel_1.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel_1.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")   
    
    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        with open("./data/logs.json", "r") as f:
            logs = json.load(f)

        if str(invite.guild.id) not in logs:
            return

        elif logs[str(invite.guild.id)]["log"] == "false":
            return

        else:
            c_id = int(logs[str(invite.guild.id)]["log"]) 
            channel_1 = self.client.get_channel(c_id)

            em = discord.Embed(description = f"**Invite deleted:**\n\n{invite.code}", color = color)

            wlist = []
            for w in await channel_1.webhooks():
                wlist.append(f"{w.name}")

            if "A webhook" in wlist:
                webhook_url = w.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

            else:
                hook = await channel_1.create_webhook(name="A webhook")

                webhook_url = hook.url
                webhook = Webhook(webhook_url)

                webhook.send(embed=em, username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024") 

def setup(client):
    client.add_cog(Log(client))