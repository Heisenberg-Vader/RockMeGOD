import discord
from discord.ext import commands, tasks

import dbl


class TopGG(commands.Cog):
    """
    This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 30 minutes.
    """

    def __init__(self, client):
        self.client = client
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc0MzQ0NDA2NTc0MzQwNTA2NiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEwMzAzMTEwfQ.DsSxBBdFehXL4BqFyjX-KrsTVWWSvYn8FTOjsIqarGY'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.client, self.token)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        await self.client.wait_until_ready()
        try:
            server_count = len(self.client.guilds)
            await self.dblpy.post_guild_count(server_count)
            print('Posted server count ({})'.format(server_count))
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        if isinstance(msg.channel, discord.channel.DMChannel):
            if "https://" in msg.content:
                await msg.channel.send("Hey, I have detected a server link, would you like to add me? https://discord.com/api/oauth2/authorize?client_id=743444065743405066&permissions=2080894198&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fcallback&scope=bot")
                
            else:
                return
        
        else:
            return

def setup(client):
    client.add_cog(TopGG(client)) 