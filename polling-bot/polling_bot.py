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

    def add_choice(self, choice):
        self.num_choices += 1
        self.poll_data["Choices"][self.num_choices] = choice

    def add_vote(self, num_choice):
        if num_choice not in self.poll_data["Choices"]:
            return False

        if num_choice not in self.poll_data["Votes"]:
            self.poll_data["Votes"][num_choice] = 1

        else:
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

    def get_name(self):
        if "Name" not in self.poll_data:
            return False

        return self.poll_data["Name"]

    def get_description(self):
        if "Description" not in self.poll_data:
            return False

        return self.poll_data["Description"]

    def get_choices(self):
        return self.poll_data["Choices"]

    def get_results(self):
        if self.num_choices == 0:
            return None, None

        max_votes = 0
        winning_choices = list()

        for num_choice in self.poll_data["Votes"]:
            if self.poll_data["Votes"][num_choice] > max_votes:
                winning_choices = list()
                winning_choices.append(self.poll_data["Choices"][num_choice])
                max_votes = self.poll_data["Votes"][num_choice]

            elif self.poll_data["Votes"][num_choice] == max_votes:
                winning_choices.append(self.poll_data["Choices"][num_choice])

        return winning_choices, max_votes

    def __init__(self, intents, command_prefix):
        commands.Bot.__init__(self, intents=intents, command_prefix=command_prefix)

        @self.command(name='poll', help='Starts a poll in the server')
        async def poll(ctx):
            self.create_poll()

            print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            await ctx.send("Welcome to the polling-bot!")
            await ctx.send("To add to the poll, type \"add OPTION XXX\" with the text you want to add.")

        @self.command(name='add', help='Add content to the poll')
        async def add(ctx, *args):
            if len(args) > 1:
                if args[0] == "name":
                    if self.get_name() is not False:
                        await ctx.send("A name already exists for this poll. To modify it, use the \"/edit\" command.")

                        return

                    self.edit_name(" ".join(args[1:]))

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                elif args[0] == "description":
                    if self.get_description() is not False:
                        await ctx.send(
                            "A description already exists for this poll. To modify it, use the \"/edit\" command."
                        )

                        return

                    self.edit_description(" ".join(args[1:]))

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                elif args[0] == "choice":
                    self.add_choice(" ".join(args[1:]))

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            else:
                await ctx.send("To add contents to the poll, type \"add OPTION XXX\" with the text you want to add.")

        @self.command(name='edit', help='Edit the content of the poll')
        async def edit(ctx, *args):
            if len(args) > 1:
                if args[0] == "name":
                    self.edit_name(" ".join(args[1:]))

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                elif args[0] == "description":
                    self.edit_description(" ".join(args[1:]))

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                elif args[0] == "choice":
                    self.edit_choice(" ".join(args[2:]), int(args[1]))

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            else:
                await ctx.send("To edit the poll, type \"edit OPTION XXX\" with the new text.")

        @self.command(name='vote', help='Vote for a choice in the poll')
        async def vote(ctx, *args):
            if len(args) > 0:
                self.add_vote(int(args[0]))

                print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

            else:
                await ctx.send(
                    "To vote for a choice, type \"/vote X\" with the number of the choice you want to vote for."
                )

        @self.command(name='view', help='View the contents and results of the poll')
        async def view(ctx, *args):
            if len(args) > 0:
                if args[0] == "name":
                    if self.get_name() is False:
                        await ctx.send("No name for this poll. To add one, use the \"/add\" command.")

                        return

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                    await ctx.send("Name: " + str(self.get_name()))

                elif args[0] == "description":
                    if self.get_description() is False:
                        await ctx.send("No description for this poll. To add one, use the \"/add\" command.")

                        return

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                    await ctx.send("Description: " + str(self.get_description()))

                elif args[0] == "choices":
                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                    await ctx.send("Choices: " + str(self.get_choices()))

                elif args[0] == "results":
                    if self.get_results() == (None, None):
                        await ctx.send("No votes yet for this poll.")

                        return

                    print("{} invoked {} command in {}".format(ctx.author, ctx.message.content, ctx.guild.name))

                    await ctx.send("The winner of the poll is: " + str(self.get_results()))

            else:
                await ctx.send("To view information about the poll, type \"/view description/choices/results\".")
