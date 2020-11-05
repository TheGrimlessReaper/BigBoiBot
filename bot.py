#import things
import discord
from discord.ext import commands
import asyncio
import time
import random

#start
print (time.ctime() + " Bot starting...")
starttime = time.time()

#read token
with open("A:\\Documents\\Discord Bottt\\token.txt", "r") as f:
    token = f.readlines()[0]

#read from config
with open("A:\\Documents\\Discord Bottt\\configu.txt", "r") as j:
    lines = j.readlines()
    ownerid = int(((lines[0])[9:]).strip())
    prefix = (str((lines[1])[7:])).strip()
    playing = (str(lines[2])[8:]).strip()

#initialize variables
bot = commands.Bot(command_prefix = prefix, help_command = None)
version = 1.4
embedcolor = 0x71368a
game = discord.Game(playing)

#runs on bot ready
@bot.event
async def on_ready():
    print(time.ctime() + " Bot live!")
    game = discord.Game(playing)
    await bot.change_presence(activity = game)

#decorator to check if message author is owner
def isOwner():
    def predicate(ctx):
        return ctx.message.author.id == ownerid
    return commands.check(predicate)

#help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(title = "Commands", description = "Must use prefix `" + prefix + "` before command", color = int(embedcolor))
    embed.add_field(name = "ping", value = "Pings the user.", inline = False)
    embed.add_field(name = "info", value = "Sends bot info.", inline = False)
    embed.add_field(name = "coinflip", value = "Flips a coin.", inline = False)
    embed.add_field(name = "remind", value = "Sends a reminder after a user-specified amount of time. For full usage type `" + prefix + "remind help`.", inline = False)
    embed.add_field(name = "weather", value = "Sends the weather. For full usage type `" + prefix + "weather help`.", inline = False)
    embed.add_field(name = "g `or` google", value = "Sends google search link.", inline = False)
    embed.add_field(name = "gay", value = "Because Chase is gay.", inline = False)
    await ctx.send(content = None, embed = embed)

#info command
@bot.command()
async def info(ctx):
    uptimesecs = round(time.time() - starttime)
    m, s = divmod(uptimesecs, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    time2 = "%0d:%02d:%02d:%02d" % (d, h, m, s)
    embed = discord.Embed(title = "Bot info", color = embedcolor)
    embed.add_field(name = "Ping", value = str(int(bot.latency * 1000)) + " ms", inline = False)
    embed.add_field(name = "Version", value = "Discord.py version: " + str(discord.__version__) + " " + str(discord.version_info.releaselevel) + " \nBot version: " + str(version), inline = False)
    embed.add_field(name = "Uptime", value = str(time2), inline = False)
    embed.add_field(name = "View source:", value = "https://github.com/TheGrimlessReaper/BigBoiBot", inline = False)
    await ctx.send(content = None, embed = embed)

#command that pings the user and sends Pong
@bot.command()
async def ping(ctx):
    await ctx.send(str(ctx.author.mention) + " Pong!")

#command that flips a coin
@bot.command()
async def coinflip(ctx):
    result = ["Heads", "Tails"]
    await ctx.send(random.choice(result) + "!")

#command that searches google
@bot.command()
async def google(ctx, *args):
    search = "{}".format("+".join(args))
    await ctx.send("https://google.com/search?q=" + search)

#another command that searches google
@bot.command()
async def g(ctx, *args):
    search = "{}".format("+".join(args))
    await ctx.send("https://google.com/search?q=" + search)

#command that changes playing status of bot
@isOwner()
@bot.command()
async def changeplaying(ctx, arg):
    if (arg == "default"):
        await bot.change_presence(activity = game)
        await ctx.send("Playing status changed to default")
    else:
        await bot.change_presence(activity = arg)
        await ctx.send("Playing status changed to " + str(arg))

#command that changes online status of bot
@isOwner()
@bot.command()
async def changestatus(ctx, arg):
    print(arg)
    if (arg == "online" or arg == "default"):
        await bot.change_presence(activity = game, status = discord.Status.online)
        await ctx.send("Online status changed to `online`.")
    elif (arg == "away" or arg == "idle"):
        await bot.change_presence(activity = game, status = discord.Status.idle)
        await ctx.send("Online status changed to `away`.")
    elif (arg == "dnd"):
        await bot.change_presence(activity = game, status = discord.Status.dnd)
        await ctx.send("Online status changed to `do not disturb`.")
    elif (arg == "invis" or arg == "offline" or arg == "invisible"):
        await bot.change_presence(activity = game, status = discord.Status.invisible)
        await ctx.send("Online status changed to `invisible`.")

#remind command
@bot.command()
async def remind(ctx, *args):
    if (args[0] == "help"):
        embed = discord.Embed(title = "Remind", description = "Reminds users.", color = embedcolor)
        embed.add_field(name = "How to use:", value = prefix + "remind <time>; <reminder>\nSupported units: seconds, minutes, hours, days", inline = False)
        await ctx.send(content = None, embed = embed)
    else: 
        reminder = "{}".format(" ".join(args))
        print(reminder)
        ctime = int(time.time())
        sep = ";"
        remindtime = (str(reminder.split(sep, 2)[0]))
        remindtimestr = ''.join([i for i in remindtime if not i.isdigit()])
        remindtimenum = ''.join([i for i in remindtime if i.isdigit()])
        remindtimestr = str(remindtimestr.strip())
        remindtimenum = int(remindtimenum)
        reminder = (reminder.split(sep, 2)[1]).strip()
        print(str(remindtimenum),remindtimestr,reminder,remindtime)
        if (remindtimestr == "d" or remindtimestr == "day" or remindtimestr == "days" or remindtimestr == " d" or remindtimestr == " day" or remindtimestr == " days"):
            finalremindtime = (remindtimenum * 86400) + ctime
            remindtimelongstr="day"
        elif (remindtimestr == "h" or remindtimestr == "hour" or remindtimestr == "hours" or remindtimestr == " h" or remindtimestr == " hour" or remindtimestr == " hours"):
            finalremindtime = (remindtimenum * 3600) + ctime
            remindtimelongstr="hour"
        elif (remindtimestr == "m" or remindtimestr == "minute" or remindtimestr == "minutes" or remindtimestr == " m" or remindtimestr == " minute" or remindtimestr == " minutes"):
            finalremindtime = (remindtimenum * 60) + ctime
            remindtimelongstr="minute"
        elif (remindtimestr == "s" or remindtimestr == "second" or remindtimestr == "seconds" or remindtimestr == " s" or remindtimestr == " second" or remindtimestr == " seconds"):
            finalremindtime = remindtimenum + ctime
            remindtimelongstr="second"
        else:
            await ctx.send("Invalid time.")
        if remindtimenum == 1:
            await ctx.send("Okay, " + str(ctx.message.author.mention) + ", I'll remind you in " + str(remindtimenum) + " " + str(remindtimelongstr) + ".")
        elif remindtimenum > 1:
            await ctx.send("Okay, " + str(ctx.message.author.mention) + ", I'll remind you in " + str(remindtimenum) + " " + str(remindtimelongstr) + "s.")
        await asyncio.sleep(finalremindtime-ctime)
        await ctx.send(str(ctx.message.author.mention) + " " + str(reminder))

#echoes what is said
@isOwner()
@bot.command()
async def echo(ctx, *, args):
    await ctx.send(args)

#because chase is gay
@bot.command()
async def gay(ctx):
    chase = bot.get_user(231600702819008512)
    await ctx.send(str(chase.mention) + " Chase is gay :KappaPride:")

#prints that the bot has been disconnected
@bot.event
async def on_disconnect():
    while(True):
        print(time.ctime() + " Client disconnected")
        await asyncio.sleep(5)

#prints when bot has been reconnected
@bot.event 
async def on_resumed():
    print(time.ctime() + " Client reconnected!")

#run bot
bot.run(token)
