# Bot made by Cameron
# Add me on Discord! Cameron#5842

import discord
from discord.ext import commands
import asyncio
import csv
from bs4 import BeautifulSoup
import urllib.request
from html.parser import HTMLParser
from datetime import datetime
from pytz import timezone
import requests
import json

bot = commands.Bot(command_prefix="!", case_insensitive=True)

bot.remove_command('help')

myGuild = bot.get_guild(315554696460894209)


# Makes the commands case insensitive
@bot.group(case_insensitive=True)

# Prints to the console when the bot is up and ready
@bot.event
async def on_ready():
    print('We have logged in')

#--------------------------------------------------------Commands------------------------------------------------------------------

# Custom help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="AvBot", description="A multipurpose bot with a central theme of Aviation and ease-of-use.", color=0x26ABD4)

    embed.add_field(name="!help", value="Shows this message.", inline=False)
    embed.add_field(name="!ts", value="Gives a information about Transport Canada and a link to their website.", inline=False)
    embed.add_field(name="!icao [CODE]", value="This command is for getting information on different aerodromes/airports by inputting the ICAO code of that airport.", inline=False)
    embed.add_field(name="!zulu", value="This command displays the current zulu (Greenwich Mean Time) time.", inline=False)
    embed.add_field(name="!BoA (Aliases Include: 'BoeingOrAirbus').", value="This command is just a joke about Airbus and Boeing", inline=False)
    embed.add_field(name="!info", value="This command gives a short description of the bot along with the Author (me), how many servers the bot is currently on, and an invite link if you wish to use this bot on your server!", inline=False)
    embed.add_field(name="!hello", value="This command is just for saying hello to the bot and it will respond likewise.", inline=False)
    embed.add_field(name="!purge", value="This command can remove between 1 and 500 of the most recent messages in the channel where the command is executed.")
    embed.add_field(name="!create_channel [channel name]", value="This command creates a custom voice channel for you and your friends to play games or have a private chat.")
    embed.add_field(name="!delete_channel [channel name]", value="This command deletes a voice channel.")


    await ctx.send(embed=embed)

# Command for Bot Info
@bot.command()
async def info(ctx):
    embed = discord.Embed(title=bot.user.name, description="Waltzy sucks and stop making fun of my bot's function.", color=0x26ABD4)
    
    # give info about you here
    embed.add_field(name="Author", value="Cameron")
    
    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=len(bot.guilds))

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite My Bot To Your Server!](https://discordapp.com/api/oauth2/authorize?client_id=438785767049789441&permissions=0&scope=bot)")

    await ctx.send(embed=embed)

# Command for creating channels
@bot.command()
async def create_channel(ctx, channelName: str = None):
    categoryID = 438280527401713667
    channelCategory = bot.get_channel(categoryID)
    await ctx.send('Hey, I have created **' + channelName + '** for you. It is under the **' + channelCategory.name + '** category')
    await ctx.guild.create_voice_channel(channelName, category=channelCategory)

# Command for deleting channels.
@bot.command()
async def delete_channel(ctx, channel : discord.VoiceChannel):
    await ctx.send('Hey, I have deleted **{}** for you.'.format(channel))
    await channel.delete()

# Command for changing the bot's name
@bot.command()
async def bot_name(ctx, newBotName: str):
    await bot.user.edit(username = newBotName)

# Command for saying hello to the bot. It replies!
@bot.command(aliases=["hi", "yousuck", "howdy", "sup", "yo", "whats up", "what's up"])
async def hello(ctx):
    await ctx.send("Ayyyyy, was guuud boyos!!")

# Command for getting information on an airport/aerodrome when ICAO code is provided
@bot.command()
async def icao(ctx, airportCode: str):
    airportData = open('airports.csv', encoding="utf8")

    csv_airportData = csv.reader(airportData)
    for row in csv_airportData:
        if row[1] == airportCode:
            titleElement = "{0}".format(row [3])
            descElement1 = "({0})".format(row [1])
            descElement2 = "{0}".format(row [10])
            descElement3 = "{0}".format(row [9])
            e = discord.Embed(title=titleElement, description=descElement1, color=0x26ABD4)
            e.add_field(name='Country-Region', value=descElement3)
            e.add_field(name='City', value=descElement2)
            await ctx.send(embed=e)
            break
    else:
            await ctx.send('Invalid ICAO Airport Code!')

# (Not Yet Working) Command to retrieve METAR and TAF data from an airport given the ICAO code
@bot.command()
async def metar(ctx):
    headers = {
        'X-API-Key': 'e529ae2f9f39e5554ab34e952f',
        'Accept': 'application/json',
    }

    requests.get('https://api.checkwx.com/station/kpie', headers=headers)

# Command to get Transport Canada information and website
@bot.command()
async def ts(ctx):
    e = discord.Embed(title="Transport Canada", description="Transport Canada is the department within the government of Canada which is responsible for developing regulations, policies and services of transportation in Canada. It is part of the Transportation, Infrastructure and Communities portfolio.", color=0x26ABD4)
    e.add_field(name='Website', value='https://www.tc.gc.ca/')
    e.set_image(url='https://assets.skiesmag.com/wp-content/uploads/2017/09/Transport-Canada-logo.png')
    await ctx.send(embed=e)

# Funny Boeing joke
@bot.command(aliases=["boa"])
async def BoeingOrAirbus(ctx):
    e = discord.Embed(title="If it's not Boeing, I'm not going!", description="Courtesy of Cameron :blush:", color=0x26ABD4)
    await ctx.send(embed=e)

# Command to get Zulu (Greenwich Mean Time) time
@bot.command()
async def zulu(ctx):
    zuluTime = datetime.utcnow()
    await ctx.send(zuluTime.strftime("```The current Zulu time is: %H:%M:%S```"))

# Command to change the bot's status.
@bot.command()
async def status(ctx, *, currentStatus: str):
    game = discord.Game(currentStatus)
    await bot.change_presence(status=discord.Status.idle, activity=game)
    await ctx.send(":thumbsup: Status has been set to " + currentStatus)

# Command that purges messages
@bot.command(aliases=["purge"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount:int):
      amount = min(amount, 500)
      await ctx.channel.purge(limit=amount)
      await ctx.send("**{}** messages have been removed!".format(amount))

#--------------------------------------------------------------------------Bot Token----------------------------------------------------------------------------------------




bot.run("NDM4Nzg1NzY3MDQ5Nzg5NDQx.DcLJHg.njZfe1ifmbULvucpeaH_-fU5pXA")



