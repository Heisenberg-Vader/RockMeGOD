import discord
import json
from discord.ext import commands
import random
import asyncio

colors = [0x1abc9c, 0xffff00, 0xe90000, 0x00e931, 0x0057e9, 0x00ffff, 0xf3f3f3, 0xff0091]

color = random.choice(colors)

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["bal"])
    @commands.is_owner()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def balance(self, ctx, member: discord.Member = None): 

        users = await self.get_bank_data()
        if member == None:
            member = ctx.author

        if member.bot:
            await ctx.send("Bots don't have access to economy, you dum!")
            return

        await self.open_account(member)
        user = member

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        max_amt = users[str(user.id)]["max"]

        em = discord.Embed(title = f"{user.name}'s balance", description = f"**Wallet**: <:rockcash:795902344934981652> {wallet_amt}\n**Bank**: <:rockcash:795902344934981652> {bank_amt}/{max_amt}\n**Total**: <:rockcash:795902344934981652> {bank_amt + wallet_amt}", colour = discord.Colour.green())

        if wallet_amt == 69 or wallet_amt == 6969:
            em.set_footer(text = "OMFGGG SEX NUMBER!!!!!!!")
        
        else:
            em.set_footer(text = "https://rockmegod.netlify,app 😉")

        await ctx.send(embed = em)

    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 15, commands.BucketType.user) 
    async def beg(self, ctx):
        await self.open_account(ctx.message.author)
        user = ctx.author
        users = await self.get_bank_data()

        earnings = random.randrange(100)

        await ctx.send(f"Someone Gave You {earnings} Coins!!")

        users[str(user.id)]["wallet"] += earnings

        with open("bank.json", "w") as f:
            json.dump(users,f) 

    @commands.command(aliases = ['with'])
    @commands.is_owner()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def withdraw(self, ctx, amount = None):
        await self.open_account(ctx.message.author)
        if amount == None:
            await ctx.send("Hey dumb, what are you withdrawing(mention it).")
            return

        bal = await self.update_bank(ctx.message.author)
        if amount == "all":
            amount = bal[1]

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("Stop trying to break me. You dont have that much money.")
            return

        if amount < 0:
            await ctx.send("So you have discovered a way to earn money in negative numbers. WOW!(FOOL)")
            return

        await self.update_bank(ctx.message.author,amount)
        await self.update_bank(ctx.message.author,-1*amount,"bank")
        await ctx.send(f"**{amount}** <:rockcash:795902344934981652> withdrawn.")


    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def give(self, ctx, member : discord.Member, amount = None):
        if member.bot:
            await ctx.send("Bots don't have access to economy, you dum!")
            return

        await self.open_account(ctx.message.author)
        await self.open_account(member)

        if amount == None:
            await ctx.send("Hey dumb, what are you sending.")
            return

        bal = await self.update_bank(ctx.message.author)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("Stop trying to break me. You dont have that much money.")
            return

        if amount<0:
            await ctx.send("So you have discovered a way to earn money in negative numbers. WOW!(FOOL)")
            return

        await self.update_bank(ctx.message.author,-1*amount,"wallet")
        await self.update_bank(member,amount,"wallet")
        await ctx.send(f"You gave **{amount}** <:rockcash:795902344934981652> to **{member.name}**.")

    @commands.command(aliases = ['steal'])
    @commands.is_owner()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rob(self, ctx, member : discord.Member):
        if member.bot:
            await ctx.send("Bots can't be robbed as they don't have access to economy, you dum!")
            return

        await self.open_account(ctx.message.author)
        await self.open_account(member)

        bal = await self.update_bank(member)
        bal1 = await self.update_bank(ctx.author)

        if bal1[0] < 300: 
            await ctx.send("You need minimum **300** <:rockcash:795902344934981652> to rob someone!")
            return

        if bal[0] < 500:
            await ctx.send("Victim doesnt have a **500** <:rockcash:795902344934981652>. Leave the poor guy alone!!")
            return

        earnings = random.randrange(0,bal[0])
        case = random.randint(1,2)

        if case == 1:
            await self.update_bank(ctx.message.author, earnings)
            await self.update_bank(member,-1*earnings)
            await ctx.send(f"You robbed and got **{earnings}** <:rockcash:795902344934981652>")
        
        else:
            await self.update_bank(ctx.author,-1*500)
            await self.update_bank(member,500)
            await ctx.send(f"You failed in the rob and had to pay **500** <:rockcash:795902344934981652> to **{member.name}**")

    @commands.command(aliases = ['dep'])
    @commands.is_owner()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def deposit(self, ctx, amount = None):
        await self.open_account(ctx.message.author)
        if amount == None:
            await ctx.send("Hey dumb, what are you depositing(mention it).")
            return

        bal = await self.update_bank(ctx.message.author)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("Stop trying to break me. You dont have that much money.")
            return

        if amount < 0:
            await ctx.send("So you have discovered a way to earn money in negative numbers. WOW!(FOOL)")
            return
          
        left_space = bal[2] - bal[1]

        if amount > left_space:
            amount = left_space

        if bal[1] == bal[2]:
            await ctx.send("Hey kiddo, your bank seems to be full!")

            users[str(user.id)]["wallet"] = bal[0]
            users[str(user.id)]["bank"] = bal[1]
            users[str(user.id)]["max"] = bal[2]

            with open("bank.json","w") as f:
                json.dump(users, f)

            return

        else:
            await self.update_bank(ctx.message.author,-1*amount)
            await self.update_bank(ctx.message.author,amount,"bank")
            await ctx.send(f"**{amount}** <:rockcash:795902344934981652> deposited.")
        
    async def open_account(self, user):
        users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else :
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 250
            users[str(user.id)]["bank"] = 0
            users[str(user.id)]["max"] = 500

        with open("bank.json","w") as f:
            json.dump(users,f)
        return True

    async def get_bank_data(self):
        with open("bank.json","r") as f:
            users = json.load(f)

        return users 

    async def update_bank(self, user, change = 0,mode = 'wallet'):
        users = await self.get_bank_data()

        users[str(user.id)][mode] = users[str(user.id)][mode] + change

        with open("bank.json","w") as f:
            json.dump(users,f)

        bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"],users[str(user.id)]["max"]]
        return bal

    @commands.command(aliases = ["am"])
    @commands.is_owner()
    async def addmoney(self, ctx, user: discord.Member, amount: int):
        if user.bot:
            return

        else:
            await self.open_account(user)
            await self.update_bank(user,amount)
            await ctx.send(f"Added **{amount}** <:rockcash:795902344934981652> to **{user.name}**!")


    @commands.command()
    @commands.is_owner()
    async def shop(self, ctx, index: int = None):
        if index == 1 or index == None:
            em = discord.Embed(title = ":shopping_cart: __***Shop Items***__ :shopping_cart:", description = "\n*** <:rockphone:796031719610122281> __ Cell Phone __ —— <:rockcash:795902344934981652> [500](https://www.youtube.com/watch?v=ub82Xb1C8os) ***\nYou would wanna use it for lots of stuff, check em urself :wink: !\n\n***<:rockpc:796036124106817576> __PC__ —— <:rockcash:795902344934981652> [10000](https://www.youtube.com/watch?v=ub82Xb1C8os) ***\nYou'd wanna do all kinda stuff using this like gaming and streaming.... or maybe be lame.... :joy:\n\n***<:rocklaptop:796038121690103869> __Laptop__ —— <:rockcash:795902344934981652> [2500](https://www.youtube.com/watch?v=ub82Xb1C8os)***\nYou would like to use this to post cool memes or maybe not........ lol\n\n***<:rockriffle:796304576021921792> __Huntin Riffle__ —— <:rockcash:795902344934981652> [10000](https://www.youtube.com/watch?v=ub82Xb1C8os)***\nGo hunting with the riffle and get some <:rockcash:795902344934981652> out of it :wink:\n\n***<:rockpole:796304876639748096> __Fishing Pole__ —— <:rockcash:795902344934981652> [7000](https://www.youtube.com/watch?v=ub82Xb1C8os)***\nGo on to a river side for some fishes and get some.....\n\n***<:bankpotion:796305218568060938>__Bank Potion__ —— <:rockcash:795902344934981652> [80000](https://www.youtube.com/watch?v=ub82Xb1C8os)***\nWill get you extra bank space, you might want it!\n\n", color = color)
            em.set_footer(text = "https://discord.gg/G5wPkDv")

            await ctx.send(embed = em)

        elif index == 2:
            await ctx.send("Worked")

    @commands.command()
    @commands.is_owner()
    async def use(self, ctx, *, item = None):
        with open("bank.json","r") as f:
            users = json.load(f)

        if item == None:
            await ctx.send("What do you want to use dum dum!")

        else:
            if item == "bank potion" or item == "bp" or item == "bank":
                amount = random.randrange(3000, 9000)
                old_max = users[str(ctx.author.id)]["max"]
                users[str(ctx.author.id)]["max"] += amount

                with open("bank.json","w") as f:
                    json.dump(users, f)

                await ctx.send(f"You used a **Bank Potion** and now bank has given you an allowance of **{amount}** more that can be deposited and **{old_max - amount}** being ")

            else:
                return

def setup(client):
    client.add_cog(Economy(client))