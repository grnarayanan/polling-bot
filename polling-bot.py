# -*- coding: utf-8 -*-
"""
polling-bot for Discord

Conduct basic polling functions in a Discord server

@author: Ganesan Narayanan
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

#client = discord.Client(intents=discord.Intents.all())
token = os.getenv('TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="/")


poll_data = dict()


'''
@client.event
async def on_ready():
    print("{} has connected to Discord.".format(client.user))
    
@client.event
async def on_message(message):

    #TODO ignore DMs

    if message.author == client.user:
        return

    print("{}".format(message.author))
    print("{}".format(message.content))
    print("{}".format(message.channel))
    print()

    await message.channel.send(str(message.content).upper())
'''

#TODO modify permissions
#TODO add user input verification

@bot.command(name='poll', help='Starts a poll in the server')
async def poll(ctx):

    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

    await ctx.send("Welcome to the polling-bot!")
    await ctx.send("To add to the poll, type \"add OPTION XXX\" with the text you want to add.")


@bot.command(name='add', help='Add content to the poll')
async def add(ctx, *args):

    if len(args) > 1:
        
        if args[0] == "name":

            if "name" in poll_data:

                await ctx.send("A name already exists for this poll. To modify it, use the \"/edit\" command.")
                
                return

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("Name: " + " ".join(args[1:]))

            poll_data["name"] = " ".join(args[1:])

        elif args[0] == "description":

            if "description" in poll_data:

                await ctx.send("A description already exists for this poll. To modify it, use the \"/edit\" command.")
                
                return

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("Description: " + " ".join(args[1:]))

            poll_data["description"] = " ".join(args[1:])
        
        elif args[0] == "choice":
            
            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("Choice: " + " ".join(args[1:]))

    else:

        await ctx.send("To add contents to the poll, type \"add OPTION XXX\" with the text you want to add.")


@bot.command(name='edit', help='Edit the content of the poll')
async def edit(ctx, *args):

    if len(args) > 1:

        if args[0] == "name":

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("New name: " + " ".join(args[1:]))
       
            poll_data["name"] = " ".join(args[1:])
        
        elif args[0] == "description":

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("New description: " + " ".join(args[1:]))
       
            poll_data["description"] = " ".join(args[1:])

        elif args[0] == "choice":

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("New choice: " + " ".join(args[1:]))

    else:

        await ctx.send("To edit the poll, type \"edit OPTION XXX\" with the new text.")


@bot.command(name='vote', help='Vote for a choice in the poll')
async def vote(ctx, *args):

    if len(args) > 0:

        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

        print("Vote: " + str(int(args[0])))

    else:

        await ctx.send("To vote for a choice, type \"/vote X\" with the number of the choice you want to vote for.")


@bot.command(name='view', help='View the contents and results of the poll')
async def view(ctx, *args):

    if len(args) > 0:

        if args[0] == "name":

            if "name" not in poll_data:

                await ctx.send("No name for this poll. To add one, use the \"/add\" command.")
                
                return

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("View name")
            await ctx.send("Name: " + poll_data["name"])

        elif args[0] == "description":

            if "description" not in poll_data:

                await ctx.send("No description for this poll. To add one, use the \"/add\" command.")
                
                return

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("View description")
            await ctx.send("Description: " + poll_data["description"])

        elif args[0] == "choices":

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("View choices")
            await ctx.send("Choices: ")

        elif args[0] == "results":

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            print("View results")
            await ctx.send("The winner of the poll is: ")

    else:

        await ctx.send("To view information about the poll, type \"/view description/choices/results\".")


#client.run(token)
bot.run(token)
