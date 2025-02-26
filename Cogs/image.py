import discord
from discord.ext import commands
import asyncio

class image_cmd(commands.Cog, name = "Image Commands"):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wasted(self, ctx, member: discord.Member):
        if member == None:
            member = ctx.author

        avatar_url = member.avatar_url_as(format="png")

        URL = f'https://some-random-api.ml/canvas/wasted?avatar={avatar_url}'

        em = discord.Embed(title = "Wasted!!", color = 0x1abc9c, timestamp = ctx.message.created_at)
        em.set_image(url = URL)
        em.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)

    @commands.command()
    async def glass(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        avatar_url = member.avatar_url_as(format="png")

        URL = f'https://some-random-api.ml/canvas/glass?avatar={avatar_url}'

        em = discord.Embed(title = "Glassed? Eh.....", color = 0x1abc9c, timestamp = ctx.message.created_at)
        em.set_image(url = URL)
        em.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)

    @commands.command()
    async def gay(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        avatar_url = member.avatar_url_as(format="png")

        URL = f'https://some-random-api.ml/canvas/gay?avatar={avatar_url}'

        em = discord.Embed(title = "Hmmm... Gay?", color = 0x1abc9c, timestamp = ctx.message.created_at)
        em.set_image(url = URL)
        em.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)

    @commands.command()
    async def invert(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        avatar_url = member.avatar_url_as(format="png")

        URL = f'https://some-random-api.ml/canvas/invert?avatar={avatar_url}'

        em = discord.Embed(title = "Inverted", color = 0x1abc9c, timestamp = ctx.message.created_at)
        em.set_image(url = URL)
        em.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def leave(self, ctx, guild: discord.Guild):
        await self.client.leave_guild(guild)
        await ctx.send(f":thumbsup: Left guild: {guild.name} ({guild.id})")

def setup(client):
    client.add_cog(image_cmd(client))