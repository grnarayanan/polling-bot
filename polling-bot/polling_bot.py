# -*- coding: utf-8 -*-
"""
polling-bot for Discord

Conduct basic polling functions in a Discord server

@author: Ganesan Narayanan
"""

from collections import defaultdict
from discord.ext import commands


class PollingBot(commands.Bot):
    def create_poll(self):
        self.poll_data = defaultdict()
        self.poll_data["Choices"] = defaultdict()
        self.poll_data["Votes"] = defaultdict()
        self.num_choices = 0
        self.poll_data["Name"] = "MyPoll"
        self.poll_data["Description"] = ""
        self.poll_active = True

    def add_choice(self, choice):
        self.num_choices += 1
        self.poll_data["Choices"][self.num_choices] = choice
        self.poll_data["Votes"][self.num_choices] = 0

    def add_vote(self, num_choice):
        if num_choice not in self.poll_data["Choices"]:
            return False

        self.poll_data["Votes"][num_choice] += 1

    def edit_name(self, new_name):
        self.poll_data["Name"] = new_name

        return True

    def edit_description(self, new_description):
        self.poll_data["Description"] = new_description

        return True

    def edit_choice(self, new_choice, num_choice):
        if num_choice not in self.poll_data["Choices"]:
            return False

        self.poll_data["Choices"][num_choice] = new_choice

        return True

    def get_poll(self):
        return self.poll_data["Name"] + "\n" + self.poll_data["Description"] + "\n" + self.get_choices()

    def get_name(self):
        return self.poll_data["Name"]

    def get_description(self):
        if "Description" not in self.poll_data:
            return False

        return self.poll_data["Description"]

    def get_choices(self):
        msg = "Choices:\n"

        for num_choice, choice in self.poll_data["Choices"].items():
            msg += str(num_choice) + ") " + choice + "\t" + "Votes: " + str(self.poll_data["Votes"][num_choice]) + "\n"

        return msg[: len(msg) - 1]

    def get_results(self):
        if self.num_choices == 0:
            return None, None

        max_votes = 0
        winning_choices = list()
        msg = ""

        for num_choice in self.poll_data["Votes"]:
            if self.poll_data["Votes"][num_choice] > max_votes:
                winning_choices = list()
                winning_choices.append(self.poll_data["Choices"][num_choice])
                max_votes = self.poll_data["Votes"][num_choice]

            elif self.poll_data["Votes"][num_choice] == max_votes:
                winning_choices.append(self.poll_data["Choices"][num_choice])

        if max_votes == 0:
            return "No votes yet for this poll."

        if len(winning_choices) == 1:
            msg += "The winner of " + self.get_name() + " is:\n" + winning_choices[0]

        else:
            msg += "The winners of " + self.get_name() + " are:\n" + ", ".join(winning_choices)

        if max_votes == 1:
            msg += ", with " + str(max_votes) + " vote!"
        else:
            msg += ", with " + str(max_votes) + " votes!"

        return msg

    def __init__(self, intents, command_prefix):
        commands.Bot.__init__(self, intents=intents, command_prefix=command_prefix)
        self.poll_active = False

        @self.command(name='poll', help='Starts a poll in the server')
        async def poll(ctx):
            self.create_poll()

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            await ctx.send("Welcome to the polling-bot!")
            await ctx.send("Type \"edit\" or \"add\" to get started.")

        @self.command(name='add', help='Add choices to the poll')
        async def add(ctx, *args):
            if self.poll_active:
                if len(args) > 1:
                    if args[0] == "choice":
                        self.add_choice(" ".join(args[1:]))

                        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                else:
                    await ctx.send(
                        "To add choices to the poll, type \"/add choice XXX\" with the text you want to add."
                    )
            else:
                await ctx.send("Type \"/poll\" to start a poll.")

        @self.command(name='edit', help='Edit the content of the poll')
        async def edit(ctx, *args):
            if self.poll_active:
                if len(args) > 1:
                    if args[0] == "name":
                        self.edit_name(" ".join(args[1:]))

                        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                    elif args[0] == "description":
                        self.edit_description(" ".join(args[1:]))

                        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                    elif args[0] == "choice":
                        if self.edit_choice(" ".join(args[2:]), int(args[1])) is False:
                            await ctx.send("Not a valid choice.")

                        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                else:
                    await ctx.send("To edit the poll, type \"edit name/description/choice XXX\" with the new text.")
            else:
                await ctx.send("Type \"/poll\" to start a poll.")

        @self.command(name='vote', help='Vote for a choice in the poll')
        async def vote(ctx, *args):
            if self.poll_active:
                if len(args) > 0:
                    if self.add_vote(int(args[0])) is False:
                        await ctx.send("Not a valid option.")

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                else:
                    await ctx.send(
                        "To vote for a choice, type \"/vote #\" with the # of the choice you want to vote for."
                    )
            else:
                await ctx.send("Type \"/poll\" to start a poll.")

        @self.command(name='view', help='View the contents and results of the poll')
        async def view(ctx, *args):
            if self.poll_active:
                if len(args) > 0:
                    if args[0] == "name":
                        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                        await ctx.send("Name: " + str(self.get_name()))

                    elif args[0] == "description":
                        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                        await ctx.send("Description: " + str(self.get_description()))

                    elif args[0] == "choices":
                        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                        await ctx.send(self.get_choices())

                    elif args[0] == "results":
                        if self.get_results() == (None, None):
                            await ctx.send("No votes yet for this poll.")

                            return

                        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                        await ctx.send(self.get_results())

                    elif args[0] == "poll":
                        print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                        await ctx.send(self.get_poll())

                else:
                    await ctx.send("To view information about the poll, type \"/view poll/results\".")
            else:
                await ctx.send("Type \"/poll\" to start a poll.")
