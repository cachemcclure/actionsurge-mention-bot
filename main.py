# main.py
import os
from dotenv import load_dotenv
#from keep_alive import keep_alive
from pickle import dump as pdump
from pickle import load as pload
import discord
from discord.ext import commands

## Load Environmental Variables
#load_dotenv()
creds = pload(open('creds.pkl','rb'))
TOKEN = creds['token']
channel_list = ['general','twsnbn-thursday-afternoon','announcements']

## Check if User Message List Exists
def load_users():
    if os.path.exists('user_list.pkl'):
        user_list = list(set(pload(open('user_list.pkl','rb'))))
    else:
        user_list = []
        pdump(user_list,open('user_list.pkl','wb'))
    return user_list

## Define Bot
bot = commands.Bot(command_prefix="!", case_insensitive=True)

## Bot Login
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

## Check Message for User on User Message List
@bot.event
async def on_message(message):
    user_list = load_users()
#    print(user_list)
    channel = str(message.channel)
    if (not str(message.content).startswith('!')) and (channel in channel_list):
        list_users = [user_mentioned for user_mentioned in message.mentions]
        it_no = len(list_users)
#        print(it_no)
        xyz = 0
        for user_mentioned in list_users:
#        for user_mentioned in message.mentions:
            if (str(user_mentioned.id) in user_list) and (xyz < it_no):
#                print('Found user!')
                await user_mentioned.send(content=str(message.content))
    await bot.process_commands(message)

## Add User to User Message List
@bot.command(name="add_user",description="Add user to DM list")
async def add_user(ctx,*args):
    user_list = load_users()
    list_users = [str(user_mentioned.id) for user_mentioned in ctx.message.mentions]
    for xx in list_users:
#        print(xx)
        if xx not in user_list:
#            print(xx)
            user_list = user_list + [xx]
    pdump(user_list,open('user_list.pkl','wb'))
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## List Users
@bot.command(name="list_users",description="List All DM Users")
async def list_users(ctx,*args):
    user_list = load_users()
    for xx in user_list:
        await ctx.author.send(xx)

## Run bot
#keep_alive()
bot.run(TOKEN)
