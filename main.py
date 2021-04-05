import os
import json
import random
import discord
from keep_alive import keep_alive
from discord.ext import commands

#gobal variabels

mag = [
    0x0037ff, 0xff0008, 0x00ffe5, 0xff1100, 0x03c2fc, 0xdffc03, 0xfc0373,
    0x03fc62, 0xfc6b03, 0xbd03fc, 0xfc0303
]
client = commands.Bot(command_prefix=("m ", "M ", "M", "m", ".m ", ".M ", ".M", ".m"))
client.remove_command("help")

#ready


@client.event
async def on_ready():
    print(f"I am ready to go - {client.user.name}")


#spamm prof/stufff


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


#commands for help

# find accout shit
async def open_account(user):

    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Wallet"] = 0
        users[str(user.id)]["Bank"] = 0
        users[str(user.id)]["level"] = 0
        users[str(user.id)]["exp"] = 0
        users[str(user.id)]["exp_multi"] = 1
        users[str(user.id)]["Bank_max"] = 100
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True

# data is data
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

#shose shit
async def update_bank(user, change=0, mode="Wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["Wallet"], users[str(user.id)]["Bank"]]
    return bal


#open acc for gamble
async def open_account_gamble(user):
  gamble = await get_gamble_data()
  if str(user.id) in gamble:
    return False
  else:
    gamble[str(user.id)] = {}
    gamble[str(user.id)]["multi"] = 0
    gamble[str(user.id)]["special multi"] = 0
    with open("gamble_stat.json", "w") as f:
      json.dump(gamble, f)
    return True


# get gamble delattr
async def get_gamble_data():
  with open("gamble_stat.json", "r") as f:
    gamble = json.load(f)
  return gamble

# change og exp
async def exp_give(user, change):
  users = await get_bank_data()
  xp_multi_work = change * users[str(user.id)]["exp_multi"]
  xp_multi = users[str(user.id)]["exp_multi"]
  users[str(user.id)]["exp"] += xp_multi_work
  xp = users[str(user.id)]["exp"]
  random_en = random.randint(0, 1)
  users[str(user.id)]["level"] = xp//100
  if random_en == 1:
    if xp_multi == 1:
     users[str(user.id)]["Bank_max"] += xp//0.125
    elif xp_multi == 2:
      users[str(user.id)]["Bank_max"] += xp//0.1
    elif xp_multi == 3:
       users[str(user.id)]["Bank_max"] += xp//0.08333333333333
    elif xp_multi == 4:
       users[str(user.id)]["Bank_max"] += xp//0.0714285714285
    elif xp_multi == 5:
       users[str(user.id)]["Bank_max"] += xp//0.0625
  with open("mainbank.json", "w") as f:
      json.dump(users, f)



#commands for bot


#bal cmd
@client.command(aliases=["shiy", "balance", "Balance"])
@commands.cooldown(1, 5, commands.BucketType.user) 
async def bal(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    await exp_give(ctx.author, random.randint(0, 1))
    wallet_amt = users[str(user.id)]["Wallet"]
    bank_amt = users[str(user.id)]["Bank"]
    bank_max_amt = users[str(user.id)]["Bank_max"]
    real = f"{bank_amt}/{bank_max_amt}"
    balem = discord.Embed(title=f"{ctx.author.name}'s balance",
    colour=random.choice(mag))
    balem.add_field(name="Wallet balance", value=wallet_amt)
    balem.add_field(name="Bank balance", value=real, inline=False)
    balem.set_footer(text="thanks for supportering me")
    await ctx.send(embed=balem)
    


#beg command
@client.command(aliases=["Beg"])
@commands.cooldown(1, 30, commands.BucketType.user) 
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    await exp_give(ctx.author, random.randint(0, 1))
    eraning = random.randint(0, 150)
    shame = [
        "I don't have any money bish", "My credit card loans need to be payed",
        "I don't have cash", "Poor begger owo", "I got family to take care of",
        "I need to feed my family",
        'Kid:"Mom see how unclean is he drinking and shit not money for you bish" Mom:*Scoffs*',
        "Go find work", "I only have card"
    ]
    if eraning == 0:
        await ctx.send(random.choice(shame))
        return
    await ctx.send(f"Some one gave you {eraning} coins!!!!!!!!!!!!!!")
    users[str(user.id)]["Wallet"] += eraning
    users[str(user.id)]["exp"] += 1
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@client.command(aliases=["with", "withdraw", "Withdraw"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def _with(ctx, amt=None):
    await open_account(ctx.author)
    if amt == None:
        await ctx.send("Please enter a valid amount")
        return
    amt = int(amt)
    bal = await update_bank(ctx.author)
    if amt > bal[1]:
        await ctx.send("you don't have that much!")
        return
    if amt < 0:
        await ctx.send("amount must be positive!")
        return
    bank_deatial_pro = await get_bank_data()
    user = ctx.author
    await update_bank(ctx.author, amt)
    await update_bank(ctx.author, -1 * amt, "Bank")
    bank_deatial_pro = await get_bank_data()
    user = ctx.author
    wallet = bank_deatial_pro[str(user.id)]["Wallet"]
    bank = bank_deatial_pro[str(user.id)]["Bank"]
    await ctx.send(f"<@{user.id}> You withdrew **{amt}** coins. Now you have **{wallet}** in your wallet, and have **{bank}** in your bank!")


# dep 
@client.command(aliases=["dep", "Deposit", "deposit"])
@commands.cooldown(1, 5, commands.BucketType.user) 
async def _dep(ctx, amt=None):
    await open_account(ctx.author)
    users =  await get_bank_data()
    user = ctx.author
    if amt == None:
        await ctx.send("Please enter a valid amount")
        return
    amt = int(amt)
    bal = await update_bank(ctx.author)
    idk_wtf = users[str(user.id)]["Bank_max"]
    if amt + bal[1] > idk_wtf :
      await ctx.send(f"<@{ctx.author.id}> you dont have any more bank space!")
      return
    if amt > bal[0]:
        await ctx.send(f"<@{ctx.author.id}> you don't have that much!")
        return
    if amt < 0:
        await ctx.send(f"<@{ctx.author.id}> amount must be positive!")
        return
    user = ctx.author
    await update_bank(ctx.author, -1* amt)
    await update_bank(ctx.author, amt, "Bank")
    user = ctx.author
    wallet = users[str(user.id)]["Wallet"]
    bank = users[str(user.id)]["Bank"]
    await ctx.send(f"<@{user.id}> You deposited **{amt}** coins. Now you have **{wallet}** in your wallet, and have **{bank}** in your bank!")


# send cmd

@client.command(aliases=["send", "Give", "Send"])
@commands.cooldown(1, 5, commands.BucketType.user) 
async def give(ctx, member: discord.Member, amt=None):
    await open_account(ctx.author)
    await open_account(member)
    users =  await get_bank_data()
    user = ctx.author
    if amt == None:
        await ctx.send("Please enter a valid amount")
        return
    amt = int(amt)
    bal = await update_bank(ctx.author)
    idk_wtf = users[str(user.id)]["Bank_max"]
    if amt + bal[1] > idk_wtf :
      await ctx.send(f"<@{ctx.author.id}> you dont have any more bank space!")
      return
    if amt > bal[0]:
        await ctx.send(f"<@{ctx.author.id}> you don't have that much!")
        return
    if amt < 0:
        await ctx.send(f"<@{ctx.author.id}> amount must be positive!")
        return
    user = ctx.author
    await update_bank(ctx.author, -1* amt)
    await update_bank(member, amt, "Wallet")
    user = ctx.author
    wallet = users[str(user.id)]["Wallet"]
    bank = users[str(member.id)]["Wallet"]
    await ctx.send(f"<@{user.id}> You sent **{amt}** coins to <@{member.id}> Now you have **{wallet}** in your wallet, and they have **{bank}** in their wallet!")




@client.command(aliases=["Slots"])
@commands.cooldown(1, 5, commands.BucketType.user) 
async def slots(ctx, amt):
    await open_account(ctx.author)

    await open_account_gamble(ctx.author)
    user = ctx.author

    gamble = await get_gamble_data()

    if amt == None:
        await ctx.send("Please enter a valid amount")

        return
    amt = int(amt)

    bal = await update_bank(ctx.author)

    if amt > bal[0]:
        await ctx.send(f"<@{ctx.author.id}> you don't have that much!")

        return

    if amt < 0:
        await ctx.send(f"<@{ctx.author.id}> amount must be positive!")

        return

    emoji_set_1 = random.choice([":middle_finger:",":flushed:"])

    emoji_set_2 = random.choice([":eggplant:",":peach:",":eyes:"])

    emoji_set_3 = random.choice([":star2:",":alien:"])

    final = []

    for i in range(3):
      a = random.choice([emoji_set_1, emoji_set_2, emoji_set_3])

      final.append(a)

    multi = gamble[str(user.id)]["multi"]

    if final[0]  == final[1] or final[1]  == final[2]:

      if multi >= 0 and multi <= 21:

        answer1 = random.uniform(0.1, 0.9)

        roudning = round(answer1 * amt)

        await update_bank(ctx.author, + roudning)

        msg = " ".join(final)

        await ctx.send(f"you won~!!!!!!! {msg}")

    else:
      await update_bank(ctx.author, -amt)














#help cmd
@client.group(name="help", invoke_without_command=True)
async def help(ctx):
    dcem = discord.Embed(title="Maeker commands lists and type", description= "See every single command and and many more!", colour = random.choice(mag))
    dcem.set_thumbnail(url = "https://cdn.discordapp.com/avatars/805391676922920975/ef3c042031ea8bf59d7ff8fa81b152cb.jpg?size=1024")
    dcem.add_field(name = "economics", value= "`m help economics`", inline = False)
    dcem.add_field(name = "type", value = "`m help type`", inline = False)
    dcem.add_field(name = "Cooldowns", value= "`m help cooldown`", inline = False)
    dcem.add_field(name = "category", value = "`m help category {category name}`")
    dcem.add_field(name = "about", value = "`m help about {command name}`", inline = False)
    await ctx.send(embed = dcem)


@help.command(aliases = ['Econo', 'econo', 'Economics'])
async def economics(ctx):
    eem = discord.Embed(title = "Economics", description = "use `m help about {command name}` to see how to use them!", color = random.choice(mag))
    eem.add_field(name = "All economics commnds!", value = "`balance`, `withdraw`, `deposit`, `beg`, `slots`")
    await ctx.send(embed = eem)


@help.command(aliases = ['Type', 'version', 'Version'])
async def type(ctx, typeing = None):
    if typeing == None:
        tem = discord.Embed(title = "Types", colour = random.choice(mag))
        tem.add_field(name = "balance", value = "`bal`, `Balance`")
        tem.add_field(name = "withdraw", value = "`with`, `_with`, `Withdraw`")
        tem.add_field(name = "deposit", value = "`dep`, `Deposit`, `deposit`")
        tem.add_field(name = "beg", value = "`Beg`")
        tem.add_field(name = "slots", value = "`Slots`")
        await ctx.send(embed = tem)


        


@help.command(aliases=['Cooldowns', 'cooldowns', 'Cooldown'])
async def cooldown(ctx, item = None):
    cem = discord.Embed(title = "Cooldowns", colour = random.choice(mag))
    await ctx.send(embed = cem) 






#list and event
money_left = [
  "I am not made of money...",
  "I need power to run...",
  'Hold up will you host me?,then yes.....',
  'No way...',
  "Take a breather....",
  "I need some one to host me.....",
  "I will not a be FUQKER....",
  "I am gonna be done....",
  "Cpu: 99.9% Gpu: 69% Memory: 99.99999% disk usage: 100%, help...."
]

@client.event
async def on_command_error(ctx, error):
  print(error)
  if isinstance(error, commands.CommandOnCooldown):
    cmd_try = round(error.retry_after)
    errorem = discord.Embed(title="Chill chilll...", description=random.choice(money_left), color= random.choice(mag))
    errorem.add_field(name="Your on cooldown. Try again in", value=f"{cmd_try}s")
    errorem.set_footer(text="More of cool down in 'm cooldown {command}' ")
    await ctx.send(embed=errorem)

keep_alive()
client.run(os.getenv("yes"))