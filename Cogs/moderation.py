import discord
from discord.ext import commands
import asyncio
import json
import random

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command = True)
    @commands.has_permissions(administrator=True)
    async def muterole(self, ctx):
        await ctx.send("Following are the available muterole commands:\n```diff\n+ muterole set\n+ muterole remove```")
    
    @muterole.command()
    async def set(self, ctx, *, role: discord.Role):
        if isinstance(ctx.channel, discord.channel.DMChannel): 
            await ctx.send("This is a DM and not a server! Please run this command again in a server!")
            return

        else:
            with open("muterole.json","r") as f:
                mutedrole = json.load(f)

            if str(ctx.guild.id) not in mutedrole:
                mutedrole[str(ctx.guild.id)] = {}
                mutedrole[str(ctx.guild.id)]["muterole"] = role.id
                em = discord.Embed(description = f"**Succesfully set Mute Role to {role.name}**", color = ctx.author.color)
                await ctx.send(embed = em)

                with open("muterole.json","w") as f:
                    json.dump(mutedrole, f)

            else:
                mutedrole[str(ctx.guild.id)] = {}
                mutedrole[str(ctx.guild.id)]["muterole"] = role.id
                em = discord.Embed(description = f"**Succesfully updated Mute Role to {role.name}**", color = ctx.author.color)
                await ctx.send(embed = em)

                with open("muterole.json","w") as f:
                    json.dump(mutedrole, f)

    @muterole.command()
    async def remove(self, ctx, *, role: discord.Role):
        if isinstance(ctx.channel, discord.channel.DMChannel): 
            await ctx.send("This is a DM and not a server! Please run this command again in a server!")
            return

        else:
            with open("muterole.json","r") as f:
                mutedrole = json.load(f)

            if str(ctx.guild.id) not in mutedrole:
                mutedrole[str(ctx.guild.id)] = {}
                mutedrole[str(ctx.guild.id)]["muterole"] = "none"
                em = discord.Embed(description = f"**Succesfully removed Mute Role!**", color = ctx.author.color)
                await ctx.send(embed = em)

                with open("muterole.json","w") as f:
                    json.dump(mutedrole, f)

            else:
                mutedrole[str(ctx.guild.id)] = {}
                mutedrole[str(ctx.guild.id)]["muterole"] = "none"
                em = discord.Embed(description = f"**Succesfully removed mute role**", color = ctx.author.color)
                await ctx.send(embed = em)

                with open("muterole.json","w") as f:
                    json.dump(mutedrole, f)
    
    @commands.command()
    async def mute(self, ctx, *, member: discord.Member):
        if isinstance(ctx.channel, discord.channel.DMChannel): 
            await ctx.send("This is a DM and not a server! Please run this command again in a server!")
            return

        else:
            with open("muterole.json","r") as f:
                mutedrole = json.load(f)

            if mutedrole[str(ctx.guild.id)]["muterole"] == "none" or str(ctx.guild.id) not in mutedrole:
                await ctx.send("Muterole was not found in the database, please set it using the command `muterole set <role>`")
                return

            else:
                r_id = int(mutedrole[str(ctx.guild.id)]["muterole"])
                muterole = discord.utils.get(ctx.guild.roles, id = r_id)

                if muterole in member.roles:
                    emb = discord.Embed(title = "Error", description = "The given user is already muted!", color = discord.Color.red())
                    await ctx.send(embed = emb)
                    return

                elif ctx.author.top_role <= member.top_role:
                    emb = discord.Embed(title = "Error", description = "The given user is a mod/admin, so I cannot mute them!", color = discord.Color.red())
                    await ctx.send(embed = emb)
                    return

                else:
                    await ctx.send(f"`{member}` has been successfully muted!")
                    await member.add_roles(muterole)

    @commands.command()
    async def unmute(self, ctx, *, member: discord.Member):
        if isinstance(ctx.channel, discord.channel.DMChannel): 
            await ctx.send("This is a DM and not a server! Please run this command again in a server!")
            return

        else:
            with open("muterole.json","r") as f:
                mutedrole = json.load(f)

            if mutedrole[str(ctx.guild.id)]["muterole"] == "none" or str(ctx.guild.id) not in mutedrole:
                await ctx.send("Muterole was not found in the database, please set it using the command `muterole set <role>`")
                return

            else:
                r_id = int(mutedrole[str(ctx.guild.id)]["muterole"])
                muterole = discord.utils.get(ctx.guild.roles, id = r_id)

                if muterole not in member.roles:
                    emb = discord.Embed(title = "Error", description = "The given user was not muted!", color = discord.Color.red())
                    await ctx.send(embed = emb)
                    return

                elif ctx.author.top_role <= member.top_role:
                    emb = discord.Embed(title = "Error", description = "The given user is a mod/admin, so I cannot unmute them!", color = discord.Color.red())
                    await ctx.send(embed = emb)
                    return

                else:
                    await ctx.send(f"`{member}` has been successfully unmuted!")
                    await member.remove_roles(muterole)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(ban_members = True)
    async def warn(self, ctx):
        em = discord.Embed(description = "**Following are the warn commands:**\n```css\n1) warn low(1 point)\n2) warn medium(2 points)\n3) warn high(3 points)```\nOn reaching 6 points, the user will be banned automatically(To disable this the system will be made soon)", color = discord.Color.green())
        await ctx.send(embed = em)

    @warn.command()
    async def low(self, ctx, user: discord.Member, *, reason = None):
        if reason == None:
            reason = "Warned indefinitely!"

        with open("warn.json", "r") as f:
            warns = json.load(f)

        if str(ctx.guild.id) not in warns:
            warns[str(ctx.guild.id)] = {}
            warns[str(ctx.guild.id)]["autoban"] = "false"
            warns[str(ctx.guild.id)][str(user.id)] = {}
            warns[str(ctx.guild.id)][str(user.id)]["warns"] = 1

            em = discord.Embed(title = f"Warn case!", description = f"**Offender: {user}\nReason: {reason}\nResponsible Moderator: {ctx.author}**", color = discord.Color.red(), timestamp = ctx.message.created_at)

            await ctx.send(embed = em)

        else:
            if str(user.id) not in warns[str(ctx.guild.id)]:
                warns[str(ctx.guild.id)][str(user.id)] = {}
                warns[str(ctx.guild.id)][str(user.id)]["warns"] = 1

                em = discord.Embed(title = f"Warn case!", description = f"**Offender: {user}\nReason: {reason}\nResponsible Moderator: {ctx.author}**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)

            else:
                warns[str(ctx.guild.id)][str(user.id)]["warns"] += 1

                em = discord.Embed(title = f"Warn case!", description = f"**Offender: {user}\nReason: {reason}\nResponsible Moderator: {ctx.author}**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)
        
        if warns[str(ctx.guild.id)]["autoban"] == "true":
            if warns[str(ctx.guild.id)][str(user.id)]["warns"] == 6:
                await ctx.send("Banned the user for reaching 6 warns!")
                await user.ban(reason = "Reached 6 warns!")

        else:
            pass

        with open("warn.json","w") as f:
            json.dump(warns, f)

    @warn.command()
    async def medium(self, ctx, user: discord.Member, *, reason = None):
        if reason == None:
            reason = "Warned indefinitely!"

        with open("warn.json", "r") as f:
            warns = json.load(f)

        if str(ctx.guild.id) not in warns:
            warns[str(ctx.guild.id)] = {}
            warns[str(ctx.guild.id)]["autoban"] = "false"
            warns[str(ctx.guild.id)][str(user.id)] = {}
            warns[str(ctx.guild.id)][str(user.id)]["warns"] = 2

            em = discord.Embed(title = f"Warn case!", description = f"**Offender: {user}\nReason: {reason}\nResponsible Moderator: {ctx.author}**", color = discord.Color.red(), timestamp = ctx.message.created_at)

            await ctx.send(embed = em)

        else:
            if str(user.id) not in warns[str(ctx.guild.id)]:
                warns[str(ctx.guild.id)][str(user.id)] = {}
                warns[str(ctx.guild.id)][str(user.id)]["warns"] = 2

                em = discord.Embed(title = f"Warn case!", description = f"**Offender: {user}\nReason: {reason}\nResponsible Moderator: {ctx.author}**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)

            else:
                warns[str(ctx.guild.id)][str(user.id)]["warns"] += 2

                em = discord.Embed(title = f"Warn case!", description = f"**Offender: {user}\nReason: {reason}\nResponsible Moderator: {ctx.author}**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)
        
        if warns[str(ctx.guild.id)]["autoban"] == "true":
            if warns[str(ctx.guild.id)][str(user.id)]["warns"] == 6:
                await ctx.send("Banned the user for reaching 6 warns!")
                await user.ban(reason = "Reached 6 warns!")

        else:
            pass

        with open("warn.json","w") as f:
            json.dump(warns, f)

    @warn.command()
    async def high(self, ctx, user: discord.Member, *, reason = None):
        if reason == None:
            reason = "Warned indefinitely!"

        with open("warn.json", "r") as f:
            warns = json.load(f)

        if str(ctx.guild.id) not in warns:
            warns[str(ctx.guild.id)] = {}
            warns[str(ctx.guild.id)]["autoban"] = "false"
            warns[str(ctx.guild.id)][str(user.id)] = {}
            warns[str(ctx.guild.id)][str(user.id)]["warns"] = 3

            em = discord.Embed(title = f"Warn case!", description = f"**Offender: {user}\nReason: {reason}\nResponsible Moderator: {ctx.author}**", color = discord.Color.red(), timestamp = ctx.message.created_at)

            await ctx.send(embed = em)

        else:
            if str(user.id) not in warns[str(ctx.guild.id)]:
                warns[str(ctx.guild.id)][str(user.id)] = {}
                warns[str(ctx.guild.id)][str(user.id)]["warns"] = 3

                em = discord.Embed(title = f"Warn case!", description = f"**Offender: {user}\nReason: {reason}\nResponsible Moderator: {ctx.author}**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)

            else:
                warns[str(ctx.guild.id)][str(user.id)]["warns"] += 3

                em = discord.Embed(title = f"Warn case!", description = f"**Offender: {user}\nReason: {reason}\nResponsible Moderator: {ctx.author}**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)
        
        if warns[str(ctx.guild.id)]["autoban"] == "true":
            if warns[str(ctx.guild.id)][str(user.id)]["warns"] == 6:
                await ctx.send("Banned the user for reaching 6 warns!")
                await user.ban(reason = "Reached 6 warns!")

        else:
            pass

        with open("warn.json","w") as f:
            json.dump(warns, f)

    @warn.command()
    async def clear(self, ctx, user: discord.Member):
        with open("warn.json", "r") as f:
            warns = json.load(f)

        if str(ctx.guild.id) not in warns:
            warns[str(ctx.guild.id)] = {}
            warns[str(ctx.guild.id)]["autoban"] = "false"
            warns[str(ctx.guild.id)][str(user.id)] = {}
            warns[str(ctx.guild.id)][str(user.id)]["warns"] = 0

            em = discord.Embed(title = f"Warn clearance!", description = f"**Given user hasnt been warned!**", color = discord.Color.red(), timestamp = ctx.message.created_at)

            await ctx.send(embed = em)

        else:
            if str(user.id) not in warns[str(ctx.guild.id)]:
                warns[str(ctx.guild.id)][str(user.id)] = {}
                warns[str(ctx.guild.id)][str(user.id)]["warns"] = 0

                em = discord.Embed(title = f"Warn clearance!", description = f"**Given user hasnt been warned!**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)

            else:
                warns[str(ctx.guild.id)][str(user.id)]["warns"] = 0

                em = discord.Embed(title = f"Warn clearance!", description = f"**Successfully cleared {user.name}'s warns!**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)

        with open("warn.json","w") as f:
            json.dump(warns, f)
        
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def warns(self, ctx, *, user:discord.Member = None):
        if user == None:
            user = ctx.author

        with open("warn.json", "r") as f:
            warns = json.load(f)

        if str(ctx.guild.id) not in warns:
            warns[str(ctx.guild.id)] = {}
            warns[str(ctx.guild.id)]["autoban"] = "false"
            warns[str(ctx.guild.id)][str(user.id)] = {}

            em = discord.Embed(title = f"Warns for {user.name}", description = f"**Given user hasnt been warned yet!**", color = discord.Color.red(), timestamp = ctx.message.created_at)

            await ctx.send(embed = em)

        else:
            if str(user.id) not in warns[str(ctx.guild.id)]:
                warns[str(ctx.guild.id)][str(user.id)] = {}

                em = discord.Embed(title = f"Warns for {user.name}", description = f"**Given user hasnt been warned yet!**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)

            else:
                warns = warns[str(ctx.guild.id)][str(user.id)]["warns"]

                em = discord.Embed(title = f"Warns for {user.name}", description = f"**{user.mention} has `{warns}` warns!**", color = discord.Color.red(), timestamp = ctx.message.created_at)

                await ctx.send(embed = em)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def autoban(self, ctx, *, msg):
        with open("warn.json","r") as f:
            warns = json.load(f)

        if msg == "disable":
            if str(ctx.guild.id) not in warns:
                warns[str(ctx.guild.id)] = {}
                warns[str(ctx.guild.id)]["autoban"] = "false"

                await ctx.send("Disabled autoban on reaching 6 warns! <:rocktick:794474928195633193>")

            else:
                warns[str(ctx.guild.id)]["autoban"] = "false"

                await ctx.send("Disabled autoban on reaching 6 warns! <:rocktick:794474928195633193>")
                
        elif msg == "enable":
            if str(ctx.guild.id) not in warns:
                warns[str(ctx.guild.id)] = {}
                warns[str(ctx.guild.id)]["autoban"] = "true"

                await ctx.send("Enabled autoban on reaching 6 warns! <:rocktick:794474928195633193>")

            else:
                warns[str(ctx.guild.id)]["autoban"] = "true"

                await ctx.send("Enabled autoban on reaching 6 warns! <:rocktick:794474928195633193>")
        
        else:
            await ctx.send("That ain't an option buddy!")

        with open("warn.json","w") as f:
            json.dump(warns, f)


def setup(client):
    client.add_cog(Moderation(client))