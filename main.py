import discord
import json
import random
from discord.ext import commands, tasks
from discord.ext.commands import when_mentioned_or
from itertools import cycle
import asyncio
import time
import math
import keep_alive
import aiohttp
import datetime
import os
import logging
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
from discord.utils import get
from dhooks import Webhook

get_prefix = "plz "
var = "Plz "

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = commands.Bot(command_prefix = when_mentioned_or(get_prefix, var), case_insensitive=True, intents = intents)
client.remove_command('help')
status = cycle(['Snek','Flapping Bird','plz help'])
money = cycle(['Hello','You are dumb',"bruh"]) #This is unnecessary. I tried something and removed the code. Ignore it.


mainshop  = [{"name" : "Watch", "price" : 100, "description": "Time"},
             {"name" : "Laptop", "price" : 2000, "description": "Work"},
             {"name" : "PC", "price" : 20000, "description": "Gaming"},
             {"name" : "IPhone_Xs", "price" : 100000, "description": "Show Off Bro!!"},
             {"name" : "Fishing_pole", "price" : 20000, "description": "Fishing for some money!"},
             {"name" : "Hunting_Rifle", "price" : 10000, "description": "Hunt some animals for money!!"}] 

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1

    try:
        val = int(time[:-1])
    
    except:
        return -2

    return val * time_dict[unit]

@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Hello there!'))
    print("Bot is ready.")

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            em = discord.Embed(title = 'Hello all!', 
            description = "Thank you for inviting me! My prefix is 'plz' and for knowing more about me, you can type `plz help`",
            color = discord.Color.blue())
            await channel.send(embed = em)
        break

    channel_1 = client.get_channel(797041673884139551)

    wlist = []
    for w in await channel_1.webhooks():
        wlist.append(f"{w.name}")

    if "A webhook" in wlist:
        webhook_url = w.url
        webhook = Webhook(webhook_url)

        webhook.send(content = f"I have been invited to **{guild.name}** which has **{guild.member_count} members**! Cool people as they invited me!!", username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

    else:
        hook = await channel_1.create_webhook(name="A webhook")

        webhook_url = hook.url
        webhook = Webhook(webhook_url)

        webhook.send(content = f"I have been invited to **{guild.name}** which has **{guild.member_count} members**! Cool people as they invited me!!", username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")


@client.event
async def on_guild_remove(guild):
    channel_1 = client.get_channel(797041673884139551)

    wlist = []
    for w in await channel_1.webhooks():
        wlist.append(f"{w.name}")

    if "A webhook" in wlist:
        webhook_url = w.url
        webhook = Webhook(webhook_url)

        webhook.send(content = f"I have been remove from **{guild.name}** which has **{guild.member_count} members**! Dum people as they removed me!!", username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

    else:
        hook = await channel_1.create_webhook(name="A webhook")

        webhook_url = hook.url
        webhook = Webhook(webhook_url)

        webhook.send(content = f"I have been remove from **{guild.name}** which has **{guild.member_count} members**! Dum people as they removed me!!", username="RockMeGOD logging", avatar_url="https://cdn.discordapp.com/avatars/743444065743405066/a3ffcf8f184b6ea7c2dfee91cdfe9155.webp?size=1024")

@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            e = discord.Embed(title=f'Woah stop!',description = f" You must wait {int(s)} seconds to use this command! For further help you can join my support server --> https://discord.gg/6SRNBQv !",color=discord.Colour.red())
            await ctx.send(embed = e)
           
        elif int(h) == 0 and int(m) != 0:
            e = discord.Embed(title=f'Woah stop!',description = f" You must wait {int(s)} seconds to use this command! For further help you can join my support server --> https://discord.gg/6SRNBQv !",color=discord.Colour.red())
            await ctx.send(embed = e)

        else:
            e = discord.Embed(title=f"Woah stop!", description = f"You must wait {int(h)} hours , {int(m)} minutes to use this command! For further help you can join my support server --> https://discord.gg/6SRNBQv !",color=discord.Colour.red())
            await ctx.send(embed = e)

    elif isinstance(error, commands.CheckFailure):
        emb = discord.Embed(title = None, color = discord.Colour.red())
        emb.add_field(name = "** <a:redcross:781023853807271946> You dont have permissions to use this command!!**", value = "If you are still having issues, you can join my support server --> https://discord.gg/6SRNBQv !")
        await ctx.send(embed = emb)

    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title = None, color = discord.Colour.red())
        em.add_field(name = "** <a:redcross:781023853807271946> You are missing the required arguements. Please check if your command requires an addition arguement.**", value = "If you are still having issues, you can join my support server --> https://discord.gg/6SRNBQv !")
        await ctx.send(embed = em)

    elif isinstance(error, commands.RoleNotFound):
        em = discord.Embed(title = None, color = discord.Colour.red())
        em.add_field(name = "** <a:redcross:781023853807271946> No such role was found! Please mention a valid role!**", value = "If you are still having issues, you can join my support server --> https://discord.gg/6SRNBQv !")
        await ctx.send(embed = em)

@client.event
async def on_message_delete(msg):
    if msg.author.bot:
      return

    with open("snipe.json","r") as f:
        snipe = json.load(f)

    snipe[str(msg.channel.id)] = f"{msg.content}", f"{msg.author}", f"{msg.author.avatar_url}"

    with open("snipe.json","w") as f:
        json.dump(snipe, f)

    await asyncio.sleep(300)

    with open("snipe.json","r") as f:
        snipe = json.load(f)

    snipe[str(msg.channel.id)][0] = "none"

    with open("snipe.json","w") as f:
        json.dump(snipe, f)

@client.command(aliases = ['af','afact','animalf'], brief = "Gives you facts on random animals!")
async def animalfact(ctx):
    animal = ["dog","cat","panda","fox","bird","koala"]    
    a = random.choice(animal)
    
    URL = f'https://some-random-api.ml/facts/{a.lower()}'
    async with aiohttp.ClientSession() as cs:
        async with cs.get(URL) as r:
            data = await r.json()
            fact = data["fact"]
            em = discord.Embed(title = f"A fact on **{a}**", description = fact, color = 0x1abc9c, timestamp = ctx.message.created_at)
            em.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

@client.command(aliases = ["aimage",'animali'])
async def animal(ctx):
  animal = ["dog","cat","panda","fox","bird","koala"]    
  a = random.choice(animal)
  
  URL = f'https://some-random-api.ml/img/{a.lower()}'
  async with aiohttp.ClientSession() as cs:
      async with cs.get(URL) as r:
          data = await r.json()
          img = data["link"]
          em = discord.Embed(title = f"Awww! Or is it........", color = 0x1abc9c, timestamp = ctx.message.created_at)
          em.set_image(url = img)
          em.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
          await ctx.send(embed = em)

@client.command()
async def snipe(ctx):
    with open("snipe.json","r") as f:
        snipe = json.load(f)

    if snipe[str(ctx.channel.id)][0] == "none" or str(ctx.channel.id) not in snipe:
        await ctx.send("There is nothing to snipe!")

    else:
        message = snipe[str(ctx.channel.id)][0]

        em = discord.Embed(color = ctx.author.color, timestamp = ctx.message.created_at, description = message)
        em.set_author(name = snipe[str(ctx.channel.id)][1], icon_url = snipe[str(ctx.channel.id)][2])

        await ctx.send(embed = em)

@client.command(aliases = ['pl'])
async def poll(ctx, channel: discord.TextChannel = None, msg = None, question = None,*,reason = None):
    
    if reason is None or msg is None or question is None:
        await ctx.send("Bruh! Enter the correct credentials `plz poll <text_channel> <option1> <option2> <poll_for>`!")

    else:
        em = discord.Embed(title="Poll",colour = discord.Colour.blurple())
        em.add_field(name = "Poll for:", value = f"{reason}", inline = False)
        em.add_field(name = "Option 1:", value = f"React with ✅ for {msg}", inline = False)
        em.add_field(name = "Option 2:", value = f"React with ❌ for {question}", inline = False)
        message_ = await channel.send(embed=em)
        await message_.add_reaction("✅")
        await message_.add_reaction("❌")
        await ctx.message.delete()

@client.command()
async def help(ctx, msg = None):
    author = ctx.message.author
    em = discord.Embed(
            title = "RockMeGOD's Commands:",
            description = "Type `plz help <command_name>` for much defined help!\n***NOTE:*** **Economy has been disabled temporarily for the renovation of it!!**",
            colour = discord.Colour.green()
            )

    if msg == None:
            em.add_field(name = "Fun", value = "`ping`,`8ball`,`meme`,`am-i-cool`,`rps(rock paper scissor)`,`kill`,`hack`,`camel`", inline = False)
            em.add_field(name = "Currency", value = "`use pc`,`bal`,`with`,`dep`,`rob`,`slots`,`shop`,`buy`,`sell`,`fish`,`hunt`,`pm`,`inv`,`weekly`,`daily`,`search`,`work`", inline = False)
            em.add_field(name = "Moderation", value = "`mute`,`unmute`,`warn`,`ban`,`unban`,`kick`,`clear`,`changenick`,`addrole`,`removerole`", inline = False)
            em.add_field(name = "Maths", value = "`add`,`subtract`,`multiply`,`divide`,`sqrt(square root)`,`sq(square)`")
            em.add_field(name = "Utility", value = "`user-info`,`invite`,`say`,`poll`,`announce`,`servers`,`embed`,`em`,`vote`", inline = False)
            em.add_field(name = "Image", value = "`wasted`,`glass`,`gay`,`invert`,`spank`,`slap`,`rip`,`achievement`,`god`,`illuminati`,`hbday`", inline = False)
            em.add_field(name = "Giveaway", value = "`gstart`,`gcreate`,`reroll`")
            em.add_field(name = "Bot Related", value = "`suggest`,`report`", inline = False)
            em.add_field(name = "Important Links", value = "[Vote In BFD](https://botsfordiscord.com/bot/743444065743405066/vote) • [Invite](https://discord.com/api/oauth2/authorize?client_id=743444065743405066&permissions=8&scope=bot) • [Website](https://rockmegod.netlify.app) • [Vote in top.gg](https://top.gg/bot/743444065743405066/vote) • [Patreon](https://www.patreon.com/user?u=45394750&fan_landing=true)")
        
            try:
                await author.send(embed = em)
                mbed = discord.Embed(title = "Mail", description = "You have recieved a mail ✉️ !", color = discord.Color.green())
                await ctx.send(embed = mbed)
                await ctx.message.add_reaction('✉️')
            
            except:
                await ctx.send(embed = em)

    elif msg == 'ping':
        em.add_field(name = "Ping Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Fun", inline = False)
        em.add_field(name = "Usage:", value = "`plz ping`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == '8ball':
        em.add_field(name = "8ball Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Fun", inline = False)
        em.add_field(name = "Usage:", value = "`plz 8ball <your question>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "meme":
        em.add_field(name = "Meme Command", value = "Here is the help! This command is laggy!", inline = False)
        em.add_field(name = "Category:", value = "Fun", inline = False)
        em.add_field(name = "Usage:", value = "`plz meme`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'am-i-cool':
        em.add_field(name = "Am-i-cool Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Fun", inline = False)
        em.add_field(name = "Usage:", value = "`plz am-i-cool`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'reroll':
        em.add_field(name = "Giveaway Reroll Command", value = "Rerolls a giveaway and chooses new winner", inline = False)
        em.add_field(name = "Category:", value = "Giveaway", inline = False)
        em.add_field(name = "Usage:", value = "`plz reroll <message_id>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == 'rock paper scissors' or msg == "rps":
        em.add_field(name = "Rock Paper Scissor Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Fun", inline = False)
        em.add_field(name = "Usage:", value = "`plz rps <your choice>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "kill":
        em.add_field(name = "Kill Command", value = "Kill an annoying person(not real tho)!", inline = False)
        em.add_field(name = "Category:", value = "Fun", inline = False)
        em.add_field(name = "Usage:", value = "`plz kill <user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)


    elif msg == "mute":
        em.add_field(name = "Mute Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz mute <user> <time(optional)>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "unmute":
        em.add_field(name = "Mute Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz unmute <user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "warn":
        em.add_field(name = "Warn Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz warn <user> <reason>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "ban":
        em.add_field(name = "Ban Command", value = "Ban a bad boi!!", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz ban <user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "unban":
        em.add_field(name = "Unban Command", value = "Unban if you feel any sympathy(not a fully efficient command)!", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz unban <user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "kick":
        em.add_field(name = "Kick Command", value = "Kick a bad boi!", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz kick <user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "clear":
        em.add_field(name = "Clear Command", value = "Clear messages(default_value = 2)!", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz clear <amount(optional)>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "user-info":
        em.add_field(name = "User information Command", value = "Check a person's user information!", inline = False)
        em.add_field(name = "Category:", value = "Utility", inline = False)
        em.add_field(name = "Usage:", value = "`plz user-info <user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "add":
        em.add_field(name = "Addition Command", value = "Add numbers! Lol why would you use it! Homework?", inline = False)
        em.add_field(name = "Category:", value = "Maths", inline = False)
        em.add_field(name = "Usage:", value = "`plz add <num1> <num2>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "subtract":
        em.add_field(name = "Subtraction Command", value = "Subtract numbers! Lol why would you use it! Homework?", inline = False)
        em.add_field(name = "Category:", value = "Maths", inline = False)
        em.add_field(name = "Usage:", value = "`plz subtract <num1> <num2>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "multiply":
        em.add_field(name = "Multiplication Command", value = "Multiply numbers! Useful maybe. Maybe?", inline = False)
        em.add_field(name = "Category:", value = "Maths", inline = False)
        em.add_field(name = "Usage:", value = "`plz multiply <num1> <num2>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "div" or msg == "division":
        em.add_field(name = "Division Command", value = "Divide numbers! Literally the easiest, why would you need it?", inline = False)
        em.add_field(name = "Category:", value = "Maths", inline = False)
        em.add_field(name = "Usage:", value = "`plz div <num1> <num2>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "sqrt" or msg == "square root":
        em.add_field(name = "Square root Command", value = "Square root numbers! Maybe its useful!", inline = False)
        em.add_field(name = "Category:", value = "Maths", inline = False)
        em.add_field(name = "Usage:", value = "`plz sqrt <number>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "square" or msg == "sq":
        em.add_field(name = "Square Command", value = "Square numbers!", inline = False)
        em.add_field(name = "Category:", value = "Maths", inline = False)
        em.add_field(name = "Usage:", value = "`plz sq <number>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "say" :
        em.add_field(name = "Say Command", value = "Say something with more emphasis!", inline = False)
        em.add_field(name = "Category:", value = "Utility", inline = False)
        em.add_field(name = "Usage:", value = "`plz say <message>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "hack" :
        em.add_field(name = "Hack Command", value = "Hack someone!", inline = False)
        em.add_field(name = "Category:", value = "Fun", inline = False)
        em.add_field(name = "Usage:", value = "`plz hack <user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "addrole" or msg == "ar" :
        em.add_field(name = "AddRole Command", value = "Add roles to members using this command! Alias : 'ar' ", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz addrole <member> <role>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "removerole" or msg == "rr" :
        em.add_field(name = "RemoveRole Command", value = "Remove roles from members using this command! Alias : 'rr' ", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz removerole <member> <role>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "poll" :
        em.add_field(name = "Poll Command", value = "Make polls using this command!", inline = False)
        em.add_field(name = "Category:", value = "Utility", inline = False)
        em.add_field(name = "Usage:", value = "`plz poll <text_channel_name> <option1> <option2> <poll_for>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "Announce" or msg == "announce":
        em.add_field(name = "Announce Command", value = "Announce whatever you want but make sure to mention the channel!", inline = False)
        em.add_field(name = "Category:", value = "Utility", inline = False)
        em.add_field(name = "Usage:", value = "`plz announce <channel_name> <announcement>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "changenick" or msg == "cn" or msg == "changenickname":
        em.add_field(name = "Change Nickname Command", value = "Change Utility nicknames only if needed!", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Aliases:", value = "`cn`,`changenickname`")
        em.add_field(name = "Usage:", value = "`plz changenick <@user> <new_nickname>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "camel" or msg == "hump" or msg == "lol":
        em.add_field(name = "Camel Command", value = "Make a text somewhat like - 'hElLo'!", inline = False)
        em.add_field(name = "Category:", value = "Fun", inline = False)
        em.add_field(name = "Usage:", value = "`plz camel <text>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "gstart" or msg == "giveaway":
        em.add_field(name = "Giveaway Command", value = "Make giveaways with this command! YAY!!", inline = False)
        em.add_field(name = "Category:", value = "Giveaway", inline = False)
        em.add_field(name = "Usage:", value = "`plz gstart <time> <time_in_minutes/seconds> <winners> <prize>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "reminder" or msg == "remind":
        em.add_field(name = "Reminder Command", value = "Take the help of bot to remind you about your works if you have a habit of forgetting!", inline = False)
        em.add_field(name = "Category:", value = "Utiity", inline = False)
        em.add_field(name = "Usage:", value = "`plz reminder <time> <d/h/m/s> <reminder_for>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "rolemember" or msg == "rm":
        em.add_field(name = "Role Member Command", value = "Tells you about people having the particular role(do not mention the role, just type its name)!", inline = False)
        em.add_field(name = "Category:", value = "Moderation", inline = False)
        em.add_field(name = "Usage:", value = "`plz rm <member_name>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "gcreate":
        em.add_field(name = "Giveaway Create Command", value = "It is an interactive giveaway setup, but it is used only for single winner giveaway :)", inline = False)
        em.add_field(name = "Category:", value = "Giveaway", inline = False)
        em.add_field(name = "Usage:", value = "`plz gcreate`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "embed":
        em.add_field(name = "Embed Command", value = "An easy way to make embed without images!", inline = False)
        em.add_field(name = "Category:", value = "Utiity", inline = False)
        em.add_field(name = "Usage:", value = "`plz embed <title> | <description>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "em":
        em.add_field(name = "Embed Command#2", value = "It is an interactive embed setup with adding images!", inline = False)
        em.add_field(name = "Category:", value = "Utiity", inline = False)
        em.add_field(name = "Usage:", value = "`plz em`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "autofeed":
        em.add_field(name = "Autofeed Command", value = "Set the timer, set the limit and channel thats all, and autofeed is ready!", inline = False)
        em.add_field(name = "Category:", value = "Utiity", inline = False)
        em.add_field(name = "Usage:", value = "`plz autofeed <time> <limit> <channel> <message>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "report":
        em.add_field(name = "Report Command", value = "Reports a problem!", inline = False)
        em.add_field(name = "Category:", value = "Bot Related", inline = False)
        em.add_field(name = "Usage:", value = "`plz report <suggestion>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "suggest":
        em.add_field(name = "Suggestion Command", value = "We always consider your suggestion.", inline = False)
        em.add_field(name = "Category:", value = "Bot Related", inline = False)
        em.add_field(name = "Usage:", value = "`plz suggest <suggestion>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'bal' or msg == "balance":
        em.add_field(name = "Balance Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz bal`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'with' or msg == "withdraw":
        em.add_field(name = "Withdraw Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz with <amount>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'dep' or msg == "deposit":
        em.add_field(name = "Deposit Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz dep <amount>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'with' or msg == "withdraw":
        em.add_field(name = "Withdraw Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz with <amount>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "rob":
        em.add_field(name = "Rob Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz rob <user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == "slots":
        em.add_field(name = "Slots Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz slots <amount>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "shop":
        em.add_field(name = "Shop Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz shop`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "buy":
        em.add_field(name = "Buy Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz buy <item_in_shop>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "sell":
        em.add_field(name = "Sell Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz sell <item_in_shop>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == 'inventory' or msg == 'inv':
        em.add_field(name = "Inventory Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz inv`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "daily":
        em.add_field(name = "Daily Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz daily`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "weekly":
        em.add_field(name = "Weekly Command", value = "Here is the help!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz weekly`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "use pc":
        em.add_field(name = "Use Command", value = "Buy a pc and use it!", inline = False)
        em.add_field(name = "Category:", value = "Currency", inline = False)
        em.add_field(name = "Usage:", value = "`plz use pc`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'god':
        em.add_field(name = "God image Command", value = "Sends an image of a minecraft god containing the avatar of mentioned user!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz god <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'achievement':
        em.add_field(name = "Achievement image Command", value = "Sends an image of a minecraft achievement containing the avatar of mentioned user!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz achievement <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'spank':
        em.add_field(name = "Spank image Command", value = "Sends an image of the author's avatar spanking the avatar of mentioned user!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz spank <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)  

    elif msg == 'slap':
        em.add_field(name = "Slap image Command", value = "Sends an image of a author's avatar slapping the avatar of mentioned user!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz slap <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'hbday':
        em.add_field(name = "Happy Birthday image Command", value = "Sends a funny image of mentioned user's bday card!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz hbday <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'delete':
        em.add_field(name = "Delete image Command", value = "Sends a meme of deleting the mentioned user's avatar!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz delete <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'rip' or msg == "dead":
        em.add_field(name = "RIP image Command", value = "Sends an image with a grave containing avatar of the mentioned user!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz rip <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'Illuminati':
        em.add_field(name = "Illuminati image Command", value = "Sends an image of a illuminati sign with the author's avatar pic!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz illuminati <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'qrcode':
        em.add_field(name = "QRcode image Command", value = "Sends an image of the qrcode generated for a specific text!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz qrcode <text>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'invert':
        em.add_field(name = "Invert image Command", value = "Sends an image of the mentioned user's inverted color avatar!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz invert <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'gay':
        em.add_field(name = "Gay image Command", value = "Sends an image containing an overlay of rainbow colors on avatar of the mentioned user!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz gay <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)
    
    elif msg == 'wasted':
        em.add_field(name = "Wasted image Command", value = "Sends an image containing an overlay of GTA's wasted on mentioned user's avatar!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz wasted <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == 'glass':
        em.add_field(name = "Glass image Command", value = "Glass overlay on mentioned user's avatar!", inline = False)
        em.add_field(name = "Category:", value = "Image", inline = False)
        em.add_field(name = "Usage:", value = "`plz glass <@user>`", inline = False)
        em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = em)

    elif msg == "search":
        await ctx.send("I dont think you need help for this.")

    elif msg == "servers":
        await ctx.send("Owner command!")

    else:
        await ctx.send(f"No such command named: `{msg}`, was found!")

@client.command()
async def ping(ctx):
    await ctx.send(f'{ctx.message.author.mention} my ping is {round(client.latency * 1000)}ms!!')


@client.command(aliases = ['am-i-cool'])
async def am_i_cool(ctx):
    reply = ['Hmm! According to my data you are dumb!!! LOL','You are cool man!','Dumb guy asks me,"Am I Cool? XD"','Hmm ask later!','Somewhat']
    await ctx.send(f'{ctx.message.author.mention}, {random.choice(reply)}') 

@client.command(aliases=['8ball'])
async def _8ball(ctx,*,question):
    responses = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Reply hazy', 'try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Dont count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
    await ctx.send(f'Question: {question}\nAnswer: {ctx.message.author.mention}, {random.choice(responses)}')

@client.command(aliases = ["purge"])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 2):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"**{amount}** messages have been cleared!", delete_after = 5)


@client.command()
@commands.has_permissions(kick_members = True)
@commands.cooldown(1, 15, commands.BucketType.user)
async def kick(ctx, member : discord.Member, *, reason = None):
  if ctx.author.top_role <= member.top_role:
      em = discord.Embed(description = "**Hey dum, stop trying to kick people of higher roles or same role as you!**", color = discord.Color.red())
      await ctx.send(embed = em)

  else:
      await member.kick(reason = reason)
      await ctx.send(f'Kicked {member.name}#{member.discriminator}')


@client.command()
@commands.has_permissions(ban_members = True)
@commands.cooldown(1, 15, commands.BucketType.user)
async def ban(ctx, member : discord.Member, *, reason = None):
  if ctx.author.top_role <= member.top_role:
      em = discord.Embed(description = "**Hey dum, stop trying to ban people of higher roles or same role as you!**", color = discord.Color.red())
      await ctx.send(embed = em)

  else:
      await member.ban(reason = reason)
      await ctx.send(f'<a:pepeban:754216088610406462> Banned {member.name}#{member.discriminator}')

@client.command()
@commands.has_permissions(ban_members = True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def unban(ctx, *, member):
  if ctx.author.top_role <= member.top_role:
        em = discord.Embed(description = "**Hey dum, stop trying to unban people of higher roles or same role as you!**", color = discord.Color.red())
        await ctx.send(embed = em)

  else:
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')

@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.reddit.com/r/dankmemes/top.json") as response:
            j = await response.json()

    data = j["data"]["children"][random.randint(0, 25)]["data"]
    image_url = data["url"]
    title = data["title"]
    em = discord.Embed(title=title, color = discord.Color.blurple())
    em.set_image(url=image_url)
    em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed=em)


@client.command(aliases = ['user-info'])
@commands.has_permissions(manage_messages = True)
async def userinfo(ctx, member : discord.Member):

    roles = [role for role in member.roles]

    em = discord.Embed(colour = member.color , timestamp = ctx.message.author.created_at)
    
    
    em.set_author(name = f"User Info - {member}")
    em.set_thumbnail(url = member.avatar_url)
    em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)

    em.add_field(name = "ID :", value = member.id)
    em.add_field(name = "Username : ", value = member.display_name)

    em.add_field(name = "Created at : ", value = member.created_at.strftime("%a, %#d %B %Y, %I: %M %p UTC"))
    em.add_field(name = "Joined at : ", value = member.created_at.strftime("%a, %#d %B %Y, %I: %M %p UTC")) 

    em.add_field(name = f"Roles ({len(roles)})", value = " ".join([role.mention for role in roles]))
    em.add_field(name = "Top Role: ", value = member.top_role.mention)

    em.add_field(name = "Bot?", value = member.bot)

    await ctx.send(embed = em)   
            
@client.command()
async def vanish(ctx):
    await ctx.message.add_reaction('✅')
    time.sleep(0.5)
    await ctx.author.kick(reason='You have vanished')
    await ctx.author.send('You have vanished')

@client.command(aliases = ['add'])
async def addition(ctx, msg : int = None, question : int = None):
    a = msg + question

    em = discord.Embed(title = "Addition:" , colour = discord.Color.blue())
    em.add_field(name = "Added", value = f"{msg} + {question} = {a}")
    em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = em)

@client.command(aliases = ['sub'])
async def subtract(ctx, msg : int = None, question : int = None):
    a = msg - question

    em = discord.Embed(title = "Subtraction:" , colour = discord.Color.blue())
    em.add_field(name = "Subtracted", value = f"{msg} - {question} = {a}")
    em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = em)

@client.command(aliases = ['multiply'])
async def multiplication(ctx, msg : int = None, question : int = None):
    a = msg * question

    em = discord.Embed(title = "Multiplication:" , colour = discord.Color.blue())
    em.add_field(name = "Multiplied", value = f"{msg} x {question} = {a}")
    em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = em)

@client.command(aliases = ['div','divide'])
async def division(ctx, msg : int = None, question : int = None):
    a = msg / question

    em = discord.Embed(title = "Division:" , colour = discord.Color.blue())
    em.add_field(name = "Divided", value = f"{msg} ÷ {question} = {a}")
    em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = em)

@client.command(aliases = ['sqrt','square-root'])
async def square_root(ctx, msg : int = None):
    a = math.sqrt(msg)

    em = discord.Embed(title = "Square Root:" , colour = discord.Color.blue())
    em.add_field(name = "Square root of:", value = f"√{msg} = {a}")
    em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = em)

@client.command(aliases = ['sq'])
async def square(ctx, msg : int = None):
    a = msg * msg

    em = discord.Embed(title = "Square:" , colour = discord.Color.blue())
    em.add_field(name = "Square of:", value = f"({msg})^2 = {a}")
    em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed = em)

@client.command()
async def ticket(ctx):
    em = discord.Embed(title = 'Ticket', colour = discord.Colour.green())
    role = discord.utils.get(ctx.guild.roles, name="Ticket")
    await ctx.message.author.add_roles(role)
    em.add_field(name = 'Ticket Opened', value = "Success")
    await ctx.send(embed =em)

@client.command(aliases = ['ticket-close'])
async def ticket_close(ctx,member : discord.Member):
    em = discord.Embed(title = 'Ticket', colour = discord.Colour.green())
    role = discord.utils.get(ctx.guild.roles, name="Ticket")
    await member.remove_roles(role)
    em.add_field(name = 'Ticket Closed', value = "Success")
    await ctx.send(embed =em)

@client.command()
async def say(ctx,*,question = None):
    if question is None:
        await ctx.send("Please send a message to say!")
    else:
        em = discord.Embed(title = f"Message", colour = discord.Colour.blurple())
        em.add_field(name = f"{question}",value = f"Message by {ctx.author}")
        await ctx.send(embed = em)

@client.command()
async def rules(ctx):
	em = discord.Embed(title = "Rules", colour = discord.Colour.blue())
	em.add_field(name = "Rock Rules" ,value = """Rock's Official is a support server made for RockMeGOD:
	1. Discord TOS
	You must follow the discord TOs.
	https://discord.com/terms
	2. No Hate Speech
	    Hate speech isn't tolerated in this server.
	3. Religion
	    No religion talk in this server.
	5. Do not ping the owner randomly.
        Do not ping the owner for stupid reasons.
	6. NSFW Content
	    No NSFW Content by users is tolerated.
	7. Names
	    Names should be SFW and mentionable.
	8. Scamming
	    Do not scam anyone, not even bots!
	9. Respect Staff
	    Respect all staff, they are here to help you! Treat them with respect!
    10. No Racism/Black Lives Matter
        Do not subject anyone to racism as it may lead to ban!""")
	await ctx.send(embed = em)

@client.command()
async def rps(ctx, message):
	a = ['rock','paper','scissor']
	b = random.choice(a)

	em = discord.Embed(title = "Rock Paper Scissors", colour = discord.Colour.red())
	if message == "rock":
		if b == message:
			em.add_field(name = "You had chosen : 🗿(rock)", value = f"I had chosen {b}",inline = False)
			em.add_field(name = "Draw", value = "It was a draw!",inline = False)
			await ctx.send(embed = em)
		elif b == "scissor":
			em.add_field(name = "You had chosen : 🗿(rock)", value = f"I had chosen {b}",inline = False)
			em.add_field(name = "You won!", value = "<a:blobhappy:766652668743254017> Congrats!You won!",inline = False)
			await ctx.send(embed = em)
		elif b == "paper":
			em.add_field(name = "You had chosen : 🗿(rock)", value = f"I had chosen {b}",inline = False)
			em.add_field(name = "You Lost!", value = "Lmao you suck at this game!",inline = False)
			await ctx.send(embed = em)

	elif message == "paper":
		if b == message:
			em.add_field(name = "You had chosen : :page_facing_up:(paper)", value = f"I had chosen {b}",inline = False)
			em.add_field(name = "Draw", value = "It was a draw!",inline = False)
			await ctx.send(embed = em)
		elif b == "rock":
			em.add_field(name = "You had chosen : :page_facing_up:(paper)", value = f"I had chosen {b}",inline = False)
			em.add_field(name = "You won!", value = "<a:blobhappy:766652668743254017> Congrats!You won!",inline = False)
			await ctx.send(embed = em)
		elif b == "scissor":
			em.add_field(name = "You had chosen : :page_facing_up:(paper)", value = f"I had chosen {b}",inline = False)
			em.add_field(name = "You lost!", value = "Lmao you suck at this game!",inline = False)
			await ctx.send(embed = em)

	elif message == "scissors" or message == "scissor":
		if b == message:
			em.add_field(name = "You had chosen : :scissors:(scissor)", value = f"I had chosen {b}",inline = False)
			em.add_field(name = "Draw", value = "It was a draw!",inline = False)
			await ctx.send(embed = em)
		elif b == "paper":
			em.add_field(name = "You had chosen : :scissors:(scissor)", value = f"I had chosen {b}",inline = False)
			em.add_field(name = "You won!", value = "<a:blobhappy:766652668743254017> Congrats!You won!",inline = False)
			await ctx.send(embed = em)
		elif b == "rock":
			em.add_field(name = "You had chosen : :scissors:(scissor)", value = f"I had chosen {b}",inline = False)
			em.add_field(name = "You lost!", value = "Lmao you suck at this game!",inline = False)
			await ctx.send(embed = em)


@client.command(aliases = ['server'])
async def invite(ctx):
    embed = discord.Embed(colour = discord.Colour.blurple())
    embed.add_field(name = "Join my Discord support server!", value = "[Click Here to join](https://discord.gg/vkvsSXq)", inline=False)
    embed.add_field(name="Invite me if you like me!", value  = "[Click here to invite it](https://discord.com/api/oauth2/authorize?client_id=743444065743405066&permissions=8&scope=bot)", inline=False)
    embed.add_field(name = "Check out my website!", value = "[Click Here to see](https://rockmegod.netlify.app/)", inline=False)
    await ctx.send(embed = embed)

@client.command()
async def kill(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send('Ok you died, now mention someone else to be killed!')
    else:
        user = ctx.message.author
        kills = [f'{member.mention} dabbed too hard and lost their hands, and hence died',f'{member.mention} forgot to keep a parachute and jumped off their plane!',f'{member.mention} died',f'{member.mention} was eaten by zombies as they forgot to wear their armor. How dumb!',f"{member.mention} tried to cook but hmm..... didn't turn out well",f'{ctx.author.mention} tried killing {member} but they died instead!',f'{member.mention} jumped into the wishing well and drowned',f'{member.mention} was thrown into the sky by a cannon......they were never found',f'{member.mention} fell into a manhole',f'{member.mention} tried robbing a fat woman...........RIP',f'{member.mention} died while playing fortnite! Noob!',f'{member.mention} shot themselves!',f'{member.mention} thought it would be great to run naked on the road........Well guess what? They died.',f'{member.mention} threw ate a bomb thinking it was a chocolate!',f'{member.mention} tried to scam bots but the bots scammed them instead and {member.mention} died.']
        a = random.choice(kills)
        if member is None or member == user:
            await ctx.send("Ok you have been killed, please mention someone else to kill!")
        else:
            await ctx.send(a)

@client.command()
async def hack(ctx, member:discord.Member = None):
    if member is None:
        await ctx.send("TF, Why do you wanna hack yourself?")

    else:
        a = ['akoemdkea','87y21unfjkm','uiadnedam','fByEpCmf','Ls3NRHDdx','xFrrkcYA','9F44wVGX','z5UJFpwn']
        responses = ['NEWBOI','HUNTER','NOBRO','DANKY','HALLO','SALLY','MANNY','GREG','MELMSIE','DREAM','NOU']
        ip = ["192.168.3.1",'192.168.1.1','192.168.100.234','192.168.67.23','192.168.7.2']
        media = ['Youtube','Facebook','Reddit','Tinder','LinkedIn']
        l = random.choice(media)
        s = random.choice(ip)
        time = 2
        c = random.choice(responses)
        b = random.choice(a)
        message = ['She is so hot','I am eating burger','wha...I hate you','Bullshit','bro my friend f*cked my gf','I am depressed','oof what a tiring day']
        m = random.choice(message)
        msg = await ctx.send(f"Hacking **{member}**!")
        await asyncio.sleep(time)
        await msg.edit(content= f"Getting details....")
        await asyncio.sleep(time)
        await msg.edit(content= f"Username : '**{member}**', Password : '**{b}**' ")
        await asyncio.sleep(time)
        await msg.edit(content= f"Getting messages..")
        await asyncio.sleep(time)
        await msg.edit(content= f"Last DM with: **{c}** , message: '{m}' ")
        await asyncio.sleep(time)
        await msg.edit(content= f"Getting IP..........")
        await asyncio.sleep(time)
        await msg.edit(content= f"IP address : '**{s}**'")
        await asyncio.sleep(time)
        await msg.edit(content= f"Getting accounts......")
        await asyncio.sleep(time)
        await msg.edit(content= f"Accounts on : **{l}**")
        await asyncio.sleep(time)
        await msg.edit(content= f"Injecting Spyware")
        await asyncio.sleep(time)
        await msg.edit(content= f" :thumbsup: Getting emotes....")
        await asyncio.sleep(time)
        await msg.edit(content= f"Emotes found.. <:rocktick:794474928195633193>")
        await asyncio.sleep(time)
        await msg.edit(content= f"Sending data to discord officials.")
        await asyncio.sleep(time)
        await msg.edit(content= f"You have saved the **Discord TOS** by reporting this hacker and they have awarded you with Nitro :tada:!")
        await asyncio.sleep(time)
        await msg.edit(content=f'''Hacking **{member}** is done''')
        await asyncio.sleep(time)
        await ctx.send("A totally dangerous hack is complete!")

@client.command(aliases = ['ar'])
@commands.has_permissions(manage_roles = True)
async def addrole(ctx,member: discord.Member = None, role : discord.Role = None):
    if ctx.author.top_role <= member.top_role:
        em = discord.Embed(description = "**Hey dum, stop trying to add high roles than you or same as you!**", color = discord.Color.red())
        await ctx.send(embed = em)

    else:
        if role is None or member is None:
            await ctx.send("You are missing some credentials\n`plz addrole <user> <role_name>`")
        
        else:
            addrole = discord.utils.get(member.guild.roles, name = f"{role}")
            await member.add_roles(role)
            await ctx.send(f"{member.mention} has been given the role!")

@client.command(aliases = ['rr'])
@commands.has_permissions(manage_roles = True)
async def removerole(ctx,member: discord.Member = None, role : discord.Role = None):
    if ctx.author.top_role <= member.top_role:
        em = discord.Embed(description = "**Hey dum, stop trying to remove roles people of higher roles or same role as you!**", color = discord.Color.red())
        await ctx.send(embed = em)

    else:
        if role is None or member is None:
            await ctx.send("You are missing some credentials\n`plz removerole <user> <role_name>`")
        
        else:
            removerole = discord.utils.get(member.guild.roles, name = f"{role}")
            await member.remove_roles(role)
            await ctx.send(f"The role has been removed from {member.mention}!")

@client.command()
async def announce(ctx, channel: discord.TextChannel,* ,message = None):
    if message is None:
        await ctx.send("What The Flip DO YOU WANNA ANNOUNCE!")
    
    else:
        channel_ = discord.utils.get(ctx.guild.channels, name = str(channel))
        em = discord.Embed(title = "ANNOUNCEMENT", color = discord.Color.blue())
        em.add_field(name = f"{ctx.author} wants to announce: ", value = f"{message}! Make sure to react with ✅ if you have read it!", inline = False)
        message_ = await channel_.send(embed = em)
        await message_.add_reaction('✅')
        await ctx.message.delete()

@client.command()
async def servers(ctx):
    await ctx.send(f'I am in `{len(client.guilds)}` servers')

@client.command(aliases = ['changenick','cn'])
@commands.has_permissions(manage_nicknames = True)
async def changenickname(ctx,member: discord.Member, *, msg):
    if msg is None:
        await ctx.send("Please mention a new nickname!")

    else:    
        await member.edit(nick = msg)
        await ctx.send(f"New nickname: {member.mention}!")

@client.command()
@commands.has_permissions(manage_channels = True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(":white_check_mark: Locked ")

@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(":white_check_mark: Unlocked ")

@client.command(aliases = ['s','slow'])
@commands.has_permissions(manage_messages = True, manage_channels = True)
async def slowmode(ctx, seconds):
    if seconds == "off":
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send(f"Slowmode removed!")
    
    else:     
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

@client.command()
async def fakekick(ctx, member: discord.Member = None):

    responses = ['https://media.tenor.com/images/fa3b490fd1f50266282559882737898a/tenor.gif','https://media.tenor.com/images/898a1c4bb77b0c85a2ece8a4b039fdd3/tenor.gif','https://media1.tenor.com/images/fb2a19c9b689123e6254ad9ac6719e96/tenor.gif?itemid=4922649']
    
    if member is not None:
        embed = discord.Embed(title='Wapow!',description=f'**{ctx.author}** kicks **{member}**', colour = discord.Color.green())
        embed.set_image(url = random.choice(responses))
        await ctx.send(embed=embed)
 

@client.command(aliases = ['lol','hump'])
async def camel(ctx,*,msg):
    msg = list(msg)
    converted = []
    for x in msg:
        try:
            qt = random.randint(0,1)
            if qt == 1:
                convert = x.upper()
                converted.append(convert)
            elif qt == 0:
                convert = x.lower()
                converted.append(convert)
        except:
            pass

    final = ''.join(converted)
    await ctx.send(final)

@client.command()
@commands.has_permissions(manage_messages = True, manage_guild = True)
async def gstart(ctx, time : int, msg , winners: int, * , prize: str):
    if msg == "sec" or msg == "seconds" or msg == "secs" or msg == "s":
        embed = discord.Embed(title = f"{prize}",
        description =  f"""React with 🎉 to enter.
        Time remaining: {time} seconds
        Hosted by: {ctx.author.mention}""",
        color = discord.Color.green())

        end = datetime.datetime.utcnow() + datetime.timedelta(seconds = time) 

        embed.set_footer(text = f"Ends At: {end} UTC")

        my_msg = await ctx.send(embed = embed)


        await my_msg.add_reaction("🎉")


        await asyncio.sleep(time)


        new_msg = await ctx.channel.fetch_message(my_msg.id)


        users = await new_msg.reactions[0].users().flatten()

        users.pop(users.index(client.user))

        for i in range(winners):

            winner = random.choice(users)

            await ctx.send(f"Congratulations! {winner.mention} won {prize}!")

    elif msg == "mins" or msg == "minutes" or msg == "m":
        embed = discord.Embed(title = f"{prize}",
        description =  f"""React with 🎉 to enter.
        Time remaining: {time} minutes
        Hosted by: {ctx.author.mention}""",
        color = discord.Color.green())

        end = datetime.datetime.utcnow() + datetime.timedelta(seconds = time*60) 

        embed.set_footer(text = f"Ends At: {end} UTC")


        my_msg = await ctx.send(embed = embed)


        await my_msg.add_reaction("🎉")


        await asyncio.sleep(time*60)


        new_msg = await ctx.channel.fetch_message(my_msg.id)


        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))

        for i in range(winners):

            winner = random.choice(users)

            await ctx.send(f"Congratulations! {winner.mention} won {prize}!")

@client.command(aliases = ['av'])
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(title = f"{ctx.message.author}'s avatar!", color = discord.Color.green())
        embed.set_image(url = ctx.message.author.avatar_url)
        embed.set_footer(text = f"Requested by {ctx.author}")
        await ctx.send(embed = embed)

    else:
        embed = discord.Embed(title = f"{member}'s avatar!", color = discord.Color.blurple())
        embed.set_image(url = member.avatar_url)
        embed.set_footer(text = f"Requested by {ctx.author}") 
        await ctx.send(embed = embed)       

@client.command(aliases = ['remind','remindme'])
async def reminder(ctx, time: int, msg = None, *, reason):
    if msg == None:
        await ctx.send("Tell me the timer to remind you! Example: <days(d)/hours(h)/minutes(m)>")

    elif msg == "d" or msg == "days":
        embed = discord.Embed(title = "Reminder set!", description = f"`I will remind you in {time} days!`", color = discord.Color.green())
        await ctx.send(embed = embed)

        await asyncio.sleep(time*86400)

        em =  discord.Embed(title = "Reminder", description = f"`{reason}``", color = discord.Color.blue())
        await ctx.author.send(embed = em)

    elif msg == "h" or msg == "hours":
        embed = discord.Embed(title = "Reminder set!", description = f"`I will remind you in {time} hours!`", color = discord.Color.green())
        await ctx.send(embed = embed)

        await asyncio.sleep(time*3600)

        em =  discord.Embed(title = "Reminder", description = f"`{reason}`", color = discord.Color.blue())
        await ctx.author.send(embed = em)

    elif msg == "m" or msg == "minutes":
        embed = discord.Embed(title = "Reminder set!", description = f"`I will remind you in {time} minutes!`", color = discord.Color.green())
        await ctx.send(embed = embed)

        await asyncio.sleep(time*60)

        em =  discord.Embed(title = "Reminder", description = f"`{reason}`", color = discord.Color.blue())
        await ctx.author.send(embed = em)

    elif msg == "s" or msg == "seconds":
       await ctx.send("I hope you can remember things in seconds, so why do you wanna set a reminder for that!")

@client.command()
@commands.has_permissions(manage_guild=True)
async def serverinfo(ctx):
    embed = discord.Embed(title=" Server Information ", color=discord.Colour.green())
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="Name", value=ctx.guild.name, inline=True)
    embed.add_field(name="ID", value=ctx.guild.id, inline=True)
    embed.add_field(name="Created at", value=ctx.guild.created_at.strftime("%#d/%m/%Y"), inline=True)
    embed.add_field(name="Members", value=int(ctx.guild.member_count), inline=True)
    embed.add_field(name="Region", value=ctx.guild.region, inline=True)
    embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
    embed.add_field(name="Text Channels", value=len(ctx.guild.text_channels), inline=True)
    embed.add_field(name="Voice Channels", value=len(ctx.guild.voice_channels), inline=True)
    await ctx.send(embed=embed)

@client.command()
async def post(ctx, channel: discord.TextChannel, *, msg = None):
    if msg == None:
        await ctx.send("<a:among_us_vibing:764449078612328458> Pls give me a message to post! <a:among_us_vibing:764449078612328458>")

    else:
        await channel.send(msg)

@client.command()
@commands.has_permissions(manage_messages = True, manage_guild = True)
async def gcreate(ctx):

    await ctx.send("Answer the following questions within 30 seconds.....")

    ques = ["What is the duration of the giveaway?(s|m|h|d)",
    "Which channel do you want it to be hosted in?",
    "What is the prize for the giveaway?"]

    ans = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in ques:
        em = discord.Embed(title = i, color = ctx.author.color)
        await ctx.send(embed = em)

        try:
            msg = await client.wait_for('message', timeout = 30.0, check = check)
        
        except asyncio.TimeoutError:
            await ctx.send("You didnt answer in time, be quicker next time")
            return

        else:
            ans.append(msg.content)

    try:
        c_id = int(ans[1][2:-1])
    except:
        await ctx.send(f"No such channel found.\nDo it like this : {ctx.channel.mention}")
        return

    channel = client.get_channel(c_id)

    time = convert(ans[0])

    if time == -1:
        await ctx.send("No such unit found. Please answer in (s|m|h|d)!")
        return

    elif time == -2:
        await ctx.send("Time should be in numbers/integers.")
        return

    prize = ans[2]

    await ctx.send(f"Giveaway has been hosted in {channel.mention} and will last {ans[0]}!")    

    embed = discord.Embed(title = f"{prize}",description = f"""
    React with :tada: to enter
    Time: {ans[0]}
    Hosted by : {ctx.author.mention}""",
    color = ctx.author.color)

    embed.set_footer(text = f"1 winner")

    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_msg = await channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()

    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")

@client.command(aliases = ['rm'])
@commands.has_permissions(manage_roles = True)
async def rolemembers(ctx, *, rolename):
    rolename = rolename.lower().replace("apac", "asia pacific")
    role = discord.utils.find(lambda r: r.name.lower() == rolename, ctx.guild.roles)
    if not role:
        return await ctx.send("That role does not exist!")
    if role.is_default():
        return await ctx.send("I think you know very well who has this role...")
    member_str = ""
    for n, member in enumerate(role.members):
        member_str += " " + member.mention
        if n % 2 == 0:
            member_str += "\n"
    await ctx.send(embed=discord.Embed(color=role.color, title=role.name, description=member_str))

@client.command()
@commands.is_owner()
async def premium(ctx, member: discord.Member):
    premium_users = await open_premium_account(member)
    await ctx.send(f"{member} has been added to premium users!")

    await member.send("Your premium access has been enabled B) !! Congrats")

async def open_premium_account(user):
    premium = await get_premium_data()

    if str(user.id) in premium:
        return False
    else :
        premium[str(user.id)] = "true"

    with open("premium.json","w") as f:
        json.dump(premium,f)
    return True

async def get_premium_data():
    with open("premium.json","r") as f:
        premium = json.load(f)

    return premium

@client.command(aliases = ["am-i-premium"])
async def am_i_premium(ctx):
    user = ctx.author
    premiums = await get_premium_data()

    with open("premium.json","r") as f:
        premium = json.load(f)

    if str(user.id) in premiums:
        await ctx.send("You are premium user..")

    else:
        await ctx.send("You are not a premium user.")

@client.command()
async def autofeed(ctx, time, limit: int, channel: discord.TextChannel, *, msg):
    user = ctx.author
    premiums = await get_premium_data()

    with open("premium.json","r") as f:
        premium = json.load(f)

    if str(user.id) in premiums:
        await ctx.send(f"```Autofeed enabled,\nTime: `{time}`\nLimit: `{limit}`\nMessage: `{msg}` ```")
        
        timer = convert(time)

        for i in range(limit):

            await asyncio.sleep(timer)

            await channel.send(msg)

    else:
        await ctx.send("Since you are not subscribed to our premium membership, you can't use this command. DM Rock Developer#3796 to subscribe to premium B)")

@client.command()
@commands.has_permissions(manage_messages = True)
async def embed(ctx, title, msg = "|", *, description):
    embed = discord.Embed(title = title, description = description, color = ctx.author.color)
    await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(manage_messages = True)
async def em(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Making an embed. Please answer the following questions in 60 seconds...")

    await asyncio.sleep(2)

    em1 = discord.Embed(title = "Which channel do you want to send the embed in?", description = "Please use the `Channel ID`!", color = ctx.author.color)

    await ctx.send(embed = em1)
    try:
        msg = await client.wait_for("message", check = check, timeout = 60.0)

        try:
            c_id = int(msg.content)
        
        except:
            await ctx.send(f"No such channel found.\nDo it like this : {ctx.channel.mention}")
            return

    except asyncio.TimeoutError:
        await ctx.send("You didnt answer in time!")
        return

    channel = client.get_channel(c_id)

    em = discord.Embed(title = "What do you want as the embed title?", color = ctx.author.color)

    await ctx.send(embed = em)
    try:
        msg = await client.wait_for("message", check = check, timeout = 60.0)

    except asyncio.TimeoutError:
        await ctx.send("You didnt answer in time!")
        return

    emb = discord.Embed(title = "What do you want as the description?", description = "Type `None` for no description.", color = ctx.author.color)
    await ctx.send(embed = emb)
    try:
        mesg = await client.wait_for("message", check = check, timeout = 60.0)

    except asyncio.TimeoutError:
        await ctx.send("You didnt answer in time!")
        return

    embe = discord.Embed(title = "What do you want as the image?(add link)", description = "Type `None` if you dont want any!", color = ctx.author.color)
    await ctx.send(embed = embe)
    try:
        message = await client.wait_for("message", check = check, timeout = 60.0)

    except asyncio.TimeoutError:
        await ctx.send("You didnt answer in time!")
        return

    if message.content.lower() == "none":
        embed = discord.Embed(title = msg.content, description = mesg.content, color = ctx.author.color)
        await channel.send(embed = embed)

    elif message.content.startswith("https://"):
        if message.content.startswith("https://discord.gg/"):
            await ctx.send("You can't have discord servers as image")
            return

        elif mesg.content.lower() == "none":
            embed = discord.Embed(title = msg.content, color = ctx.author.color)
            embed.set_image(url = message.content)
            await channel.send(embed = embed)

        else:
            embed = discord.Embed(title = msg.content, description = mesg.content, color = ctx.author.color)
            embed.set_image(url = message.content)
            await channel.send(embed = embed)

    else:
        await ctx.send("Please input a proper link.")
        return

    embed1 = discord.Embed(title = ":white_check_mark: Success", description = f"Embed sent in {channel.mention}!")
    await ctx.send(embed = embed1)

@client.command()
@commands.cooldown(1, 43200, commands.BucketType.user)
async def vote(ctx):

    em = discord.Embed(title = None, description = '''**[Vote in BFD](https://botsfordiscord.com/bot/743444065743405066/vote)
    
    [Vote in top.gg](https://top.gg/bot/743444065743405066/vote)**''', color = 0x1abc9c, timestamp = ctx.message.created_at)

    await ctx.send(embed = em)

@client.command()
async def report(ctx, *, message = None):

    if message == None:
        em = discord.Embed(title = "Please mention the content!", color = ctx.author.color, timestamp = ctx.message.created_at)
        await ctx.send(embed = em)

    elif "https://" in message:
        em = discord.Embed(title = "No links are allowed in reports!! If really needed to be given as report, join the support server and you can let us know!", color = ctx.author.color, timestamp = ctx.message.created_at)
        await ctx.send(embed = em)

    else:
        em = discord.Embed(title = "Report", description = f"Report: {message}", color = ctx.author.color, timestamp = ctx.message.created_at)
        em.set_footer(text = f"Reported by {ctx.author}")

        owner = client.get_user(639048582531383307)
        await owner.send(embed = em)

        em1 = discord.Embed(title = "Problem has been reported. We will get back to you soon. Thank you.", color = ctx.author.color)
        await ctx.author.send(embed = em1)

@client.command()
async def suggest(ctx, *, message = None):

    if message == None:
        em = discord.Embed(title = "Please mention the content!", color = ctx.author.color, timestamp = ctx.message.created_at)
        await ctx.send(embed = em)

    elif "https://" in message:
        em = discord.Embed(title = "No links are allowed in suggestions!!", color = ctx.author.color, timestamp = ctx.message.created_at)
        await ctx.send(embed = em)

    else:
        em = discord.Embed(title = "Suggestion", description = f"Suggestion: {message}", color = ctx.author.color, timestamp = ctx.message.created_at)
        em.set_footer(text = f"Suggestion by {ctx.author}")

        owner = client.get_user(639048582531383307)
        await owner.send(embed = em)

        em1 = discord.Embed(title = "Thank you for your suggestion.", color = ctx.author.color)
        await ctx.author.send(embed = em1)

@client.command()
async def dm(ctx, member: discord.Member, *,message):
    await member.send(message)

@client.command()
@commands.has_permissions(manage_messages = True, manage_guild = True)
async def reroll(ctx, id_ : int):
    channel = ctx.channel
    new_msg = await channel.fetch_message(id_)
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Congratulations! The new winner is {winner.mention}.!") 


@client.command()
@commands.has_permissions(manage_messages = True)
async def heist(ctx, amount: int, *,member: discord.Member):
    if member == None:
        await ctx.send("No sponsor name provided. Please mention the sponsor name next time.")

    elif amount == None:
        await ctx.send("Please mention the amount for the heist.")

    else:
        await ctx.send(f"""
    :tada: Get ready to rumble with this juicy Heist! :tada:

    <a:pointer:772736004222091305> Sponsor: {member.mention}

    <a:pointer:772736004222091305> Amount: {amount}

    <@&758174643814793276>
    """)

        embe = discord.Embed(title = "Join Heist", color = 0x1abc9c, timestamp = ctx.message.created_at)

        embe.add_field(name = "Be ready", value = "```diff\n+Make sure to have 1000 coins your wallet\n+We will wait for 'ONE MINUTE' before starting.```") 

        await ctx.send(embed = embe)

        embed = discord.Embed(title = "Timer", description = "60 seconds", color = 0x1abc9c, timestamp = ctx.message.created_at)

        msg = await ctx.send(embed = embed)

        await asyncio.sleep(30)

        embed2 = discord.Embed(title = "Timer", description = "30 seconds", color = 0x1abc9c, timestamp = ctx.message.created_at)

        await msg.edit(embed = embed2)

        await asyncio.sleep(30)

        await ctx.send(f"Heist time over {member.mention}! Start the heist within 10 seconds.")

        await asyncio.sleep(10)

        em = discord.Embed(title = "Heist starting..", color = ctx.author.color, timestamp = ctx.message.created_at)

        em.add_field(name = "Timer", value = ":red_car: ••••••••• :flag_black:", inline = False)

        em.add_field(name = "Sponsor", value = f"{member.mention}", inline = False)

        await ctx.send(embed = em)

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

        await ctx.channel.edit(slowmode_delay = 45)

        await asyncio.sleep(90)

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

        emb = discord.Embed(title = "Heist time ends...", color = 0x1abc9c, timestamp = ctx.message.created_at)

        emb.add_field(name = "Timer", value = "••••••••• :red_car: :flag_black:", inline = False)

        emb.add_field(name = "Sponsor", value = f"{member.mention}", inline = False)

        await ctx.send(embed = emb)

@client.command()
async def spank(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send("Please mention a member!")
        return

    else:
        spank = Image.open("./Images/spankinggrid.jpg")

        asset = member.avatar_url_as(size = 128)
        user = ctx.author.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        data2 = BytesIO(await user.read())
        pfp = Image.open(data)
        userp = Image.open(data2)

        pfp = pfp.resize((165,165))
        userp = userp.resize((200,200))

        spank.paste(pfp, (737,388))
        spank.paste(userp, (387,61))

        spank.save("./Images/spank.jpg")

        await ctx.send(file = discord.File("./Images/spank.jpg"))

@client.command()
async def slap(ctx, member:discord.Member = None):
    if member == None:
      await ctx.send("Tag someone whom you want to slap!")
      return

    slap = Image.open("./Images/slap.jpg")

    asset = member.avatar_url_as(size = 128)
    user = ctx.author.avatar_url_as(size = 128) 

    data = BytesIO(await asset.read())
    data2 = BytesIO(await user.read())

    pfp = Image.open(data)
    userp = Image.open(data2)

    pfp = pfp.resize((87,87))
    userp = userp.resize((75,75))

    slap.paste(pfp, (2,27))
    slap.paste(userp, (119,11))

    slap.save("./Images/slapped.jpg")

    await ctx.send(file = discord.File("./Images/slapped.jpg"))

@client.command()
async def delete(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author

    delete = Image.open("./Images/delete.jpg")

    asset = member.avatar_url_as(size = 128)

    data = BytesIO(await asset.read())

    pfp = Image.open(data)

    pfp = pfp.resize((198,198))

    delete.paste(pfp, (121,130))

    delete.save("./Images/deleted.jpg")

    await ctx.send(file = discord.File("./Images/deleted.jpg"))

@client.command(aliases = ["dead"])
async def rip(ctx, member:discord.Member):
    if member == None:
        member = ctx.author

    grave = Image.open("./Images/grave.jpg")

    asset = member.avatar_url_as(size = 128)

    data = BytesIO(await asset.read())

    pfp = Image.open(data)

    pfp = pfp.resize((137,137))

    grave.paste(pfp, (85,420))

    grave.save("./Images/rip.jpg")

    await ctx.send(file = discord.File("./Images/rip.jpg"))

@client.command(aliases = ["ac","achieved"])
async def achievement(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author

    achievement = Image.open("./Images/minecraft achievement.jpg")

    asset = member.avatar_url_as(size = 128)

    data = BytesIO(await asset.read())

    pfp = Image.open(data)

    pfp = pfp.resize((113,113))

    achievement.paste(pfp, (321,75))

    achievement.save("./Images/achievement.jpg")

    await ctx.send(file = discord.File("./Images/achievement.jpg"))

@client.command()
async def god(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author

    achievement = Image.open("./Images/mcgod.jpg")

    asset = member.avatar_url_as(size = 128)

    data = BytesIO(await asset.read())

    pfp = Image.open(data)

    pfp = pfp.resize((140,125))

    achievement.paste(pfp, (128,60))

    achievement.save("./Images/god.jpg")

    await ctx.send(file = discord.File("./Images/god.jpg"))

@client.command()
async def illuminati(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author

    illuminati = Image.open("./Images/illuminati.jpg")

    asset = member.avatar_url_as(size = 128)

    data = BytesIO(await asset.read())

    pfp = Image.open(data)

    pfp = pfp.resize((128,128))

    illuminati.paste(pfp, (290,350))

    illuminati.save("./Images/illuminated.jpg")

    await ctx.send(file = discord.File("./Images/illuminated.jpg"))

@client.command()
async def hbday(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author
        
    achievement = Image.open("./Images/Bdaysimp.jpg")

    asset = member.avatar_url_as(size = 128)

    data = BytesIO(await asset.read())

    pfp = Image.open(data)

    pfp = pfp.resize((84,84))

    achievement.paste(pfp, (473,334))

    achievement.save("./Images/Bdaysimpo.jpg")

    await ctx.send(file = discord.File("./Images/Bdaysimpo.jpg"))

@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"Cogs.{extension}")
    await ctx.send(f"Loaded {extension}.py")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"Unloaded {extension}.py")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    client.load_extension(f"Cogs.{extension}")
    await ctx.send(f"Reloaded {extension}.py")

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

keep_alive.keep_alive()

client.run(your_bots_token)