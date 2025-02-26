import discord
from discord.ext import commands
import asyncio
import json
import random
import qrcode
import aiohttp

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["stat"])
    async def statistics(self, ctx):
        members = 0
        for i in self.client.guilds:
            members += i.member_count
            
        colors = [0x1abc9c, 0xffff00, 0xfff000, 0xBF6666, 0xDE5151, 0xFE0000]
        color =  random.choice(colors)
        emb = discord.Embed(color = color , timestamp = ctx.message.created_at)

        emb.set_author(name = "My Statistics!", icon_url = "https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")
        emb.add_field(name = "Statistics:", value = f"```diff\n+ Servers: {len(self.client.guilds)}\n+ Users: {members}\n+ Number of commands made till date(Some commands are not visible to users): 110\n+ Developer: Rock Developer#6969 (ID:639048582531383307)```",inline=False)
        emb.add_field(name = "Important Links:", value = "<a:pointer:772736004222091305> [**Invite link**](https://discord.com/api/oauth2/authorize?client_id=743444065743405066&permissions=2080894199&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fcallback&scope=bot)\n<a:pointer:772736004222091305> [**Support Server**](https://discord.gg/6SRNBQv)\n<a:pointer:772736004222091305> [**Upvote :)**](https://top.gg/bot/743444065743405066/vote)")

        await ctx.send(embed = emb)

    @commands.command()
    async def qrcode(self, ctx, *, msg):
        msg1 = msg.replace(' ','')

        em = discord.Embed(title = "QR code generator!", description = f"Generated code for: `{msg}`", color = discord.Color.green())

        em.set_image(url = f"https://api.qrserver.com/v1/create-qr-code/?size=350x350&data={msg1}")

        await ctx.send(embed = em)

    @commands.command(pass_context=True)
    async def giphy(self, ctx, *, search):
        color = [0x1abc9c, 0xffff00, 0xfff000, 0xBF6666]
        colors = random.choice(color)
        embed = discord.Embed(title = f"Gif for {search}", color = colors)
        session = aiohttp.ClientSession()

        if search == '':
            response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=I53WBBiyyxofeFLJ5xPQ7tjIgTPDzPuc')
            data = json.loads(await response.text())
            embed.set_image(url=data['data']['images']['original']['url'])
        else:
            search.replace(' ', '+')
            response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=I53WBBiyyxofeFLJ5xPQ7tjIgTPDzPuc&limit=10')
            data = json.loads(await response.text())
            gif_choice = random.randint(0, 9)
            embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

        await session.close()

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Stats(client))