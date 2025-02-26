import discord
from discord.ext import commands
import asyncio
import json
import random

class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def log(self, ctx, msg = None, channel: discord.TextChannel = None):
        with open("./data/logs.json","r") as f:
            logs = json.load(f)

        if msg == None:
            em = discord.Embed(title = "Log commands!", description = "```css\n1) plz log set <#channel>\n2) plz log remove <#channel>```", color = ctx.author.color)

            await ctx.send(embed = em)

        elif msg == "set":
            if channel == None:
                await ctx.send(f"Hey dum, mention a channel like this: {ctx.channel.mention}")
                return
            
            else:
                if str(ctx.guild.id) not in logs:
                    logs[str(ctx.guild.id)] = {}
                    logs[str(ctx.guild.id)]["log"] = channel.id

                    em = discord.Embed(title = "Log channel set!", description = f"<:rocktick:794474928195633193> Log channel set to `#{channel.name}`", color = ctx.author.color)

                    await ctx.send(embed = em)

                else:
                    logs[str(ctx.guild.id)]["log"] = channel.id

                    em = discord.Embed(title = "Log channel updated!", description = f"<:rocktick:794474928195633193> Log channel updated to `#{channel.name}`", color = ctx.author.color)

                    await ctx.send(embed = em)

        elif msg == "remove":
            if str(ctx.guild.id) not in logs:
                logs[str(ctx.guild.id)] = {}
                logs[str(ctx.guild.id)]["log"] = "false"

                em = discord.Embed(title = "Log channel not found!", description = f"<:rockcross:794808762501824542> No channel found for logs in this server!", color = ctx.author.color)

                await ctx.send(embed = em)

            else:
                logs[str(ctx.guild.id)]["log"] = "false"

                em = discord.Embed(title = "Log channel removed!", description = f"<:rocktick:794474928195633193> Log channel removed!", color = ctx.author.color)

                await ctx.send(embed = em)

        with open("./data/logs.json","w") as f:
            json.dump(logs, f)

      
def setup(client):
    client.add_cog(Logs(client))