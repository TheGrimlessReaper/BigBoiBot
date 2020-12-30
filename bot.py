#import things
import discord
from discord.ext import commands, tasks
import asyncio
import time
import datetime
import random
import json
from os import path
import googlemaps
from noaa_sdk import noaa

#starting bot
print(time.ctime() + " Bot starting...")
starttime = time.time()

#file paths
jsonPath = "/root/bot/reminders.json"
tokenPath = "/root/bot/token.txt"
configPath = "/root/bot/configu.txt"
mapsKeyPath = "/root/bot/mapskey.txt"
hornyPath = "/root/bot/horny.jpg"

#read bot token
with open(tokenPath, "r") as f:
    token = f.readlines()[0]

#read Google Maps key
with open(mapsKeyPath, "r") as j:
    mapsKey = j.readlines()[0]

#read from config file
with open(configPath, "r") as j:
    lines = j.readlines()
    ownerID = int(((lines[0])[9:]).strip())
    prefix = (str((lines[1])[7:])).strip()
    playing = (str(lines[2])[8:]).strip()

#initialize variables
bot = commands.Bot(command_prefix = prefix, help_command = None)
version = 1.61
embedColor = 0x71368a
game = discord.Game(playing)

#create objects for the api clients
n = noaa.NOAA()
m = googlemaps.Client(key = mapsKey)

#runs on bot ready
@bot.event
async def on_ready():
    starttime = time.time()
    game = discord.Game(playing)
    await bot.change_presence(activity = game)
    print(time.ctime() + " Bot live!")
    #checking JSON for unsent reminders
    print("Loading JSON data...")
    #checks if the JSON is greater than 2 bytes (has data other than an empty list)
    if path.getsize(jsonPath) > 2:
        with open(jsonPath) as j:
            waitBool = False
            reminderData = []
            reminderData = list(json.load(j))
            print(reminderData)
            waitForList = []
            for x in reminderData:
                #if the JSON element's time is before or at the current time send the reminder now with a message at the beginning
                if int(x['time']) <= int(time.time()):
                    channel = bot.get_channel(int(x["channel"]))
                    await channel.send("This reminder was sent late because of the bot being offline at the time of the original requested reminder time.\n" + str(x["author"]) + " " + str(x["reminder"]))
                    delete_JSON_Element(x)
                #if the JSON element's time is after the current time add it to a list to be run in the background task later
                elif int(x["time"]) > int(time.time()):
                    waitBool = True
                    waitForList.append(x)
        #if there are any elements of the JSON whose time is after the current time
        if(waitBool):
            #sorts the list of elements by time
            waitForList.sort(key = sortKey)
            #start background task that sends reminders later
            wait.start(waitForList)    
        print("JSON data successfully loaded")
    #otherwise don't try to open the file because it'll throw an error
    else:
        print("No JSON data to load")

#helper function to delete a given JSON element
def delete_JSON_Element(element):
    with open(jsonPath, "r") as j:
        reminderData = list(json.load(j))
        newReminderData = []
        for x in reminderData:
            if x != element:
                newReminderData.append(x)
    with open(jsonPath, "w") as k:
        json.dump(list(newReminderData), k)
    print("Element successfully deleted")

#background task that is only run once for the reminders that are backed up in the JSON but have not happened yet
@tasks.loop(count = 1)
async def wait(remindList):
    for x in remindList:
        await asyncio.sleep(x["time"] - int(time.time()))
        channel = bot.get_channel(int(x["channel"]))
        await channel.send(str(x["author"]) + " " + str(x["reminder"]))
        delete_JSON_Element(x)

#function for sorting reminders list
def sortKey(x):
    return x["time"]

#decorator to check if message author is owner
def isOwner():
    def predicate(ctx):
        return ctx.message.author.id == ownerID
    return commands.check(predicate)

#help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(title = "Commands", description = "Must use prefix `" + prefix + "` before command", color = embedColor)
    embed.add_field(name = "info", value = "Sends bot info.", inline = False)
    embed.add_field(name = "ping", value = "Pings the user.", inline = False)
    embed.add_field(name = "coinflip", value = "Flips a coin.", inline = False)
    embed.add_field(name = "remind or r", value = "Sends a reminder after a user-specified amount of time.\nUsage: `" + prefix + "remind <time><units>; <reminder>`\nSupported units: seconds, minutes, hours, days", inline = False)
    embed.add_field(name = "weather", value = "Sends the weather. For full usage type `" + prefix + "weather help`.", inline = False)
    embed.add_field(name = "google or g", value = "Sends Google search link.", inline = False)
    embed.add_field(name = "duckduckgo or ddg", value = "Sends DuckDuckGo search link.", inline = False)
    embed.add_field(name = "gay", value = "Because Chase is gay.", inline = False)
    embed.add_field(name = "horny", value = "Because y'all are horny.", inline = False)
    await ctx.send(content = None, embed = embed)

#info command
@bot.command()
async def info(ctx):
    uptimesecs = round(time.time() - starttime)
    m, s = divmod(uptimesecs, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    uptime = "%0d:%02d:%02d:%02d" % (d, h, m, s)
    embed = discord.Embed(title = "Bot info", color = embedColor)
    embed.add_field(name = "Ping", value = str(int(bot.latency * 1000)) + " ms", inline = False)
    embed.add_field(name = "Uptime", value = str(uptime), inline = False)
    embed.add_field(name = "Version", value = "Bot version: " + str(version) + "\nDiscord.py version: " + str(discord.__version__) + " " + str(discord.version_info.releaselevel), inline = False)
    embed.add_field(name = "View source code:", value = "https://github.com/TheGrimlessReaper/BigBoiBot", inline = False)
    await ctx.send(content = None, embed = embed)

#command that pings the user
@bot.command()
async def ping(ctx):
    await ctx.send(str(ctx.author.mention) + " Pong!")

#command that flips a coin
@bot.command()
async def coinflip(ctx):
    result = ["Heads", "Tails"]
    await ctx.send(random.choice(result) + "!")

#command that searches google
@bot.command(aliases = ["g"])
async def google(ctx, *args):
    search = "{}".format("+".join(args))
    await ctx.send("https://google.com/search?q=" + search)

#command that searches DuckDuckGo
@bot.command(aliases = ["ddg"])
async def duckduckgo(ctx, *args):
    search = "{}".format("+".join(args))
    await ctx.send("https://duckduckgo.com/?q=" + search)

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
@bot.command(aliases = ["r"])
async def remind(ctx, *args):
    if (args[0] == "help"):
        embed = discord.Embed(title = "Remind", description = "Reminds users.", color = embedColor)
        embed.add_field(name = "Usage:", value = "`" + prefix + "remind <time><units>; <reminder>`\nSupported units: seconds, minutes, hours, days", inline = False)
        await ctx.send(content = None, embed = embed)
    else: 
        reminder = "{}".format(" ".join(args))
        print(reminder)
        ctime = int(time.time())
        sep = ";"
        remindtime = str(reminder.split(sep, 2)[0])
        remindtimestr = ''.join([i for i in remindtime if not i.isdigit()])
        remindtimenum = ''.join([i for i in remindtime if i.isdigit()])
        remindtimestr = str(remindtimestr.strip())
        remindtimenum = int(remindtimenum)
        remindauthor = str(ctx.message.author.mention)
        remindchannel = ctx.message.channel.id
        reminder = str((reminder.split(sep, 2)[1]).strip())
        print(remindauthor, ":", reminder, remindtime, str(remindtimenum), remindtimestr)
        if (remindtimestr == "d" or remindtimestr == "day" or remindtimestr == "days" or remindtimestr == " d" or remindtimestr == " day" or remindtimestr == " days"):
            finalremindtime = (remindtimenum * 86400) + ctime
            remindtimelongstr = "day"
        elif (remindtimestr == "h" or remindtimestr == "hour" or remindtimestr == "hours" or remindtimestr == " h" or remindtimestr == " hour" or remindtimestr == " hours"):
            finalremindtime = (remindtimenum * 3600) + ctime
            remindtimelongstr = "hour"
        elif (remindtimestr == "m" or remindtimestr == "minute" or remindtimestr == "minutes" or remindtimestr == " m" or remindtimestr == " minute" or remindtimestr == " minutes"):
            finalremindtime = (remindtimenum * 60) + ctime
            remindtimelongstr = "minute"
        elif (remindtimestr == "s" or remindtimestr == "second" or remindtimestr == "seconds" or remindtimestr == " s" or remindtimestr == " second" or remindtimestr == " seconds"):
            finalremindtime = remindtimenum + ctime
            remindtimelongstr = "second"
        else:
            await ctx.send("Invalid time.")
            return
        if remindtimenum == 1:
            await ctx.send("Okay " + remindauthor + ", I'll remind you in " + str(remindtimenum) + " " + remindtimelongstr + ".")
        elif remindtimenum > 1:
            await ctx.send("Okay " + remindauthor + ", I'll remind you in " + str(remindtimenum) + " " + remindtimelongstr + "s.")
        else:
            await ctx.send("Invalid time.")
            return
        #add reminder info to JSON
        reminderList = []
        #checks if the JSON is greater than 2 bytes (has data other than an empty list)
        if path.getsize(jsonPath) > 2:
            with open(jsonPath, "r") as j:
                reminderList = list(json.load(j))
        reminderDict = {"reminder": reminder, "author": remindauthor, "time": finalremindtime, "channel": remindchannel}
        reminderList.append(reminderDict)
        with open(jsonPath, "w") as j:
            json.dump(reminderList, j)
        print("Added to JSON")
        await asyncio.sleep(finalremindtime - ctime)
        await ctx.send(remindauthor + " " + str(reminder))
        delete_JSON_Element(reminderDict)

#echoes what is said
@isOwner()
@bot.command()
async def echo(ctx, *, args):
    await ctx.send(args)

#because chase is gay
@bot.command()
async def gay(ctx):
    chase = await bot.fetch_user(231600702819008512)
    KappaPride = bot.get_emoji(449082148415078401)
    await ctx.send(str(chase.mention) + " Chase is gay " + str(KappaPride))

#prints that the bot has been disconnected
@bot.event
async def on_disconnect():
    while(bot.is_closed()):
        print(time.ctime() + " Client disconnected")
        await asyncio.sleep(5)

#prints when bot has been reconnected
@bot.event 
async def on_resumed():
    starttime = time.time()
    print(time.ctime() + " Client reconnected!")
 
#command that plays hangman
#doesn't work yet, only owner can play
@isOwner()
@bot.command()
async def hangman(ctx):
    user = ctx.message.author
    dm = await user.create_dm()
    await user.send("Hi! You're recieving this DM because you used the " + prefix + "hangman command. What would word would you like your opponent to guess? Reply STOP now to stop.")
    await ctx.send(str(ctx.message.author.mention) + " Welcome to Hangman! Please respond to the DM that has been sent to you within 60 seconds to play.")
    cont = True
    playing = True
    while(playing):
        while(cont):
            def check(m):
                return m.channel == dm
            try:
                message = await bot.wait_for('message', timeout = 60, check = check)
            except asyncio.TimeoutError:
                await ctx.send("User did not respond to DM in time. Use the " + prefix + "hangman command if you would like to play again.")
            else:
                if(message.content == "STOP"):
                    await ctx.send("User stopped DMs. Use the " + prefix + "hangman command if you would like to play again.")
                    cont, playing = False
                else:
                    word = message.content
                    message = await user.send("Okay, your word is " + word + ". Is that right? React with :thumbsup: to confirm or :thumbsdown: to input another word.")
                    await message.add_reaction('\N{THUMBS UP SIGN}')
                    await message.add_reaction('\N{THUMBS DOWN SIGN}')
                    await asyncio.sleep(1)
                    # def check(reaction):
                    #     return str(reaction.emoji == '\N{THUMBS UP SIGN}')
                    try:
                        react = await bot.wait_for('reaction_add', timeout = 60)
                    except asyncio.TimeoutError:
                        await ctx.send("User stopped DMs. Use the " + prefix + "hangman command if you would like to play again.")
                        cont, playing = False
                    else:
                        print(react[0])
                        #doesn't work
                        if(react[0] == '👎 '):
                            await user.send("Okay, what word would you like your opponent to guess? Reply STOP now to stop.")
                        else:
                            await user.send("Okay, getting the game ready for you.")
                            cont, playing = False

#because y'all are horny
@bot.command()
async def horny(ctx):
    await ctx.send(file = discord.File(hornyPath))

#command that gives the weather
@bot.command()
async def weather(ctx, *args):
    if args:
        async with ctx.channel.typing():
            search = ""
            for x in args:
                search += str(x) + " "
            #searches for the location's coordinates using the google maps api
            geo = m.geocode(search)
            lat = float(round(geo[0]['geometry']['location']['lat'], 4))
            lon = float(round(geo[0]['geometry']['location']['lng'], 4))
            embed = discord.Embed(title = "Weather for " + search + ":", description = "Weather provided by [the National Weather Service](https://www.weather.gov/).", color = 0x3498db)
            ##hourly forecast
            hourlyForecasts = n.points_forecast(lat, lon, hourly = True)
            #datetime object of the current time in GMT
            currentTimeGMT = datetime.datetime.now(datetime.timezone.utc)
            i = 0
            for f in hourlyForecasts['properties']['periods']:
                #datetime object of the time of the spot being iterated in hourlyForecasts
                weatherTime = datetime.datetime.strptime(f['startTime'], "%Y-%m-%dT%H:%M:%S%z")
                #checks if the string of current hour in gmt is equal to the string of the hour of the place in the forecast converted to gmt (so it will work with any time zone)
                if currentTimeGMT.strftime("%I %p") == (datetime.datetime.utcfromtimestamp(weatherTime.timestamp()).strftime("%I %p")):
                    #if it is then break the for loop
                    break
                #if it is not then add 1 to the index of hourly forecasts to use
                else:
                    i+=1
            hourlyForecasts = hourlyForecasts['properties']['periods'][i:i+6]
            embedString = ""
            #adding the modified forecast array to the embed
            for f in hourlyForecasts:
                #start time of forecast in the format hour:min am/pm
                t = datetime.datetime.strptime((f['startTime']), "%Y-%m-%dT%H:%M:%S%z").strftime("%I:%M %p")
                embedString += (t + " - " + str(f['temperature']) + "°" + f['temperatureUnit'] + ", " + f['shortForecast'] + "\n")
            #embed string needs to be less than 1024 characters because of a limitation with the Discord API
            embedString = embedString[:1023]
            embed.add_field(name = "Next 6 hours:", value = embedString, inline = False)
            ##daily forecast
            embedString = ""
            dailyForecasts = n.points_forecast(lat, lon, hourly = False)
            for f in dailyForecasts['properties']['periods']:
                #converting the datetime object we are iterating at to seconds since epoch
                endT = datetime.datetime.strptime(f['endTime'], "%Y-%m-%dT%H:%M:%S%z").timestamp()
                #seconds since epoch of current time
                currentT = datetime.datetime.now().timestamp()
                #if the current time is after the end time of f in dailyForecasts
                if endT <= currentT:
                    #add 1 to the starting index of dailyForecasts
                    i+=1
                #else stop checking
                else:
                    break
            dailyForecasts = dailyForecasts['properties']['periods'][i:i+6]
            #adding the modified forecast array to the embed
            for f in dailyForecasts:
                embedString += (f['name'] + " - " + f['detailedForecast'] + "\n")
            #embed string needs to be less than 1024 characters because of a limitation with the Discord API
            embedString = embedString[:1023]
            embed.add_field(name = "Next 3 days:", value  = embedString, inline = False)
            ##alerts
            embedString = ""
            pointStr = str(lat) + "," + str(lon)
            paramsDict = {'point': pointStr}
            alerts = n.alerts(active = 1, **paramsDict)
            activeAlerts = False
            for f in alerts['features']:
                #datetime object of the end time of the alert
                endTObj = datetime.datetime.strptime(f['properties']['expires'], "%Y-%m-%dT%H:%M:%S%z")
                #these are ints of time since epoch
                startT = datetime.datetime.strptime(f['properties']['effective'], "%Y-%m-%dT%H:%M:%S%z").timestamp()
                endT = endTObj.timestamp()
                currentT = datetime.datetime.now().timestamp()
                #if the current time is before the end time and after the start time of the alert
                if(endT >= currentT and startT <= currentT):
                    activeAlerts = True
                    #add the alert to the embed
                    embedString += (f['properties']['event'] + " until " + endTObj.strftime("%B %d, %Y at %I:%M %p") + "\n")
            if(not activeAlerts):
                embedString = "No active alerts."
            if(activeAlerts):
                embedString += ("Check your NWS website or local media for more information on these alerts.")
            #embed string needs to be less than 1024 characters because of a limitation with the Discord API
            embedString = embedString[:1023]
            embed.add_field(name = "Alerts:", value = embedString, inline = False)
            embed.add_field(name = "More weather information:", value = "Visit [weather.gov](https://forecast.weather.gov/MapClick.php?lat=" + str(lat) + "&lon=" + str(lon) + ").", inline = False)
            await ctx.send(content = None, embed = embed)

#run bot
bot.run(token)