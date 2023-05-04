# -*- coding: utf-8 -*-
"""
polling-bot for Discord

Conduct basic polling functions in a Discord server

@author: Ganesan Narayanan
"""

import time
from collections import defaultdict
from discord.ext import commands


class PollingBot(commands.Bot):
    def create_poll(self):
        """Creates a new poll structure poll_data with default parameters."""
        self.poll_data = defaultdict()
        self.poll_data["Choices"] = defaultdict()
        self.poll_data["Votes"] = defaultdict()
        self.num_choices = 0
        self.poll_data["Name"] = "MyPoll"
        self.poll_data["Description"] = ""
        self.poll_active = True
        self.start_time = time.time()
        self.duration = 60
        self.voters = defaultdict()

    def add_choice(self, choice):
        """Adds a choice to the poll and initializes # of votes to 0. Modifies poll_data in place.

        Args:
            choice (str): Text for the new choice to add.

        """
        self.num_choices += 1
        self.poll_data["Choices"][self.num_choices] = choice
        self.poll_data["Votes"][self.num_choices] = 0

    def add_vote(self, num_choice, user):
        """Adds a vote to the specified choice in the poll. Modifies poll_data in place.

        Args:
            num_choice (int): Number corresponding to intended choice.
                Number is visible by running /view poll command.

        Returns:
            bool: True if choice exists and voter has not voted yet, false otherwise.

        """
        if num_choice not in self.poll_data["Choices"]:
            return False

        if user in self.voters:
            return False

        self.poll_data["Votes"][num_choice] += 1
        self.voters[user] = self.poll_data["Choices"][num_choice]

        return True

    def edit_name(self, new_name):
        """Edits the name of the poll. Modifies poll_data in place.

        Args:
            new_name (str): Text for the new name.

        """
        self.poll_data["Name"] = new_name

    def edit_description(self, new_description):
        """Edits the description of the poll. Modifies poll_data in place.

        Args:
            new_description (str): Text for the new description.

        """
        self.poll_data["Description"] = new_description

    def edit_choice(self, new_choice, num_choice):
        """Edits the specified choice in the poll. Modifies poll_data in place.

        Args:
            new_choice (str): Text for the new description.
            num_choice (int): Number for choice to modify, view with /view poll.

        Returns:
            bool: True if specified choice exists, false otherwise.

        """
        if num_choice not in self.poll_data["Choices"]:
            return False

        self.poll_data["Choices"][num_choice] = new_choice

        return True

    def edit_duration(self, new_duration):
        """Edits the duration of the poll.

        Args:
            new_duration (int): Time for new duration in minutes.

        """

        self.duration = new_duration * 60

    def get_poll(self):
        """Gets the contents of the poll in a printable format.

        Returns:
            str: Formatted string of all poll contents.

        """

        if self.poll_data["Description"] == "":
            return (
                "**"
                + self.poll_data["Name"]
                + "**"
                + "\n"
                + self.poll_data["Description"]
                + "\n\n"
                + self.get_choices_with_voters()
                + "\n\n"
                + self.get_voters()
            )

        return (
            "**"
            + self.poll_data["Name"]
            + "**"
            + "\n"
            + "*"
            + self.poll_data["Description"]
            + "*"
            + "\n\n"
            + self.get_choices_with_voters()
            + "\n\n"
            + self.get_voters()
        )

    def get_name(self):
        """Gets the name of the poll in a printable format.

        Returns:
            str: Formatted string of poll name.

        """
        return self.poll_data["Name"]

    def get_description(self):
        """Gets the description of the poll in a printable format.

        Returns:
            str: Formatted string of poll description.

        """

        return self.poll_data["Description"]

    def get_choices(self):
        """Gets the choices in the poll in a printable format.

        Returns:
            str: Formatted string of poll choices and choice number.

        """
        msg = "__Choices:__\n"

        for num_choice, choice in self.poll_data["Choices"].items():
            msg += str(num_choice) + ") " + choice + "\n"

        return msg[: len(msg) - 1]

    def get_choices_with_voters(self):
        """Gets the choices, votes, and voters in the poll in a printable format.

        Returns:
            str: Formatted string of poll choices, choice number, and votes and voters per choice.

        """

        msg = "__Choices:__\n"

        for num_choice, choice in self.poll_data["Choices"].items():
            voters = ""

            for key, value in self.voters.items():
                if value == choice:
                    voters += key + ", "

            if self.poll_data["Votes"][num_choice] == 0:
                msg += (
                    str(num_choice)
                    + ") "
                    + choice
                    + "\t\t"
                    + "Votes: "
                    + str(self.poll_data["Votes"][num_choice])
                    + "\n"
                )

            else:
                msg += (
                    str(num_choice)
                    + ") "
                    + choice
                    + "\t\t"
                    + "Votes: "
                    + str(self.poll_data["Votes"][num_choice])
                    + "\t"
                    + " (*"
                    + voters[: len(voters) - 2]
                    + "*)"
                    + "\n"
                )

        return msg[: len(msg) - 1]

    def get_voters(self):
        """Gets who has voted in the poll in a printable format.

        Returns:
            str: Formatted string with list of voters.

        """
        msg = "*Voters: "

        for voter in self.voters.keys():
            msg += voter + ", "

        if len(msg) == 9:
            msg = msg[: len(msg) - 1] + "*"

        else:
            msg = msg[: len(msg) - 2] + "*"

        return msg

    def get_results(self):
        """Gets the results of the poll in a printable format.

        Returns:
            str: Formatted string with winner of poll and number of votes.

        """
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
            msg += "The winner of " + self.get_name() + " is:\n" + "**" + winning_choices[0] + ",**"

        else:
            msg += "The winners of " + self.get_name() + " are:\n" + "**" + ", ".join(winning_choices) + ",**"

        if max_votes == 1:
            msg += " *with " + str(max_votes) + " vote!*"
        else:
            msg += " *with " + str(max_votes) + " votes!*"

        return msg

    def check_time(self):
        """Checks if the poll is past its expiry time.

        Returns:
            bool: True if poll has not expired, false otherwise.

        """

        if time.time() - self.start_time < self.duration:
            return True

        return False

    def __init__(self, intents, command_prefix):
        commands.Bot.__init__(self, intents=intents, command_prefix=command_prefix)
        self.poll_active = False

        @self.command(name='poll', help='Starts a poll in the server')
        async def poll(ctx):
            self.create_poll()

            print("{} invoked {} command in {}".format(ctx.author.display_name, ctx.message.content, ctx.guild.name))

            await ctx.send("Welcome to the polling-bot!")
            await ctx.send("Type \"edit\" or \"add\" to get started.")

        @self.command(name='add', help='Add choices to the poll')
        async def add(ctx, *args):
            if self.poll_active and self.check_time() is True:
                if len(args) > 1:
                    if args[0] == "choice":
                        self.add_choice(" ".join(args[1:]))

                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                else:
                    await ctx.send(
                        "To add choices to the poll, type \"/add choice XXX\" with the text you want to add."
                    )
            else:
                await ctx.send(
                    "No poll started or existing poll has expired, type \"/poll\" to start a new poll \
                    or \"/view results\" to view the results of the previous poll."
                )

        @self.command(name='edit', help='Edit the content of the poll')
        async def edit(ctx, *args):
            if self.poll_active and self.check_time() is True:
                if len(args) > 1:
                    if args[0] == "name":
                        self.edit_name(" ".join(args[1:]))

                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                    elif args[0] == "description":
                        self.edit_description(" ".join(args[1:]))

                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                    elif args[0] == "choice":
                        if self.edit_choice(" ".join(args[2:]), int(args[1])) is False:
                            await ctx.send("Not a valid choice.")

                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                    elif args[0] == "duration":
                        self.edit_duration(int(args[1]))

                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                else:
                    await ctx.send("To edit the poll, type \"edit name/description/choice XXX\" with the new text.")
            else:
                await ctx.send(
                    "No poll started or existing poll has expired, type \"/poll\" to start a new poll \
                    or \"/view results\" to view the results of the previous poll."
                )

        @self.command(name='vote', help='Vote for a choice in the poll')
        async def vote(ctx, *args):
            if self.poll_active and self.check_time() is True:
                if len(args) > 0:
                    if self.add_vote(int(args[0]), ctx.author.display_name) is False:
                        await ctx.send("Not a valid option or user has already voted.")

                    print(
                        "{} invoked {} command in {}".format(
                            ctx.author.display_name, ctx.message.content, ctx.guild.name
                        )
                    )

                else:
                    await ctx.send(
                        "To vote for a choice, type \"/vote #\" with the # of the choice you want to vote for."
                    )
            else:
                await ctx.send(
                    "No poll started or existing poll has expired, type \"/poll\" to start a new poll \
                    or \"/view results\" to view the results of the previous poll."
                )

        @self.command(name='view', help='View the contents and results of the poll')
        async def view(ctx, *args):
            if self.poll_active:
                if len(args) > 0:
                    if args[0] == "name":
                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                        await ctx.send("Name: " + str(self.get_name()))

                    elif args[0] == "description":
                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                        await ctx.send("Description: " + str(self.get_description()))

                    elif args[0] == "choices":
                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                        await ctx.send(self.get_choices())

                    elif args[0] == "results":
                        if self.get_results() == (None, None):
                            await ctx.send("No votes yet for this poll.")

                            return

                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                        await ctx.send(self.get_results())

                    elif args[0] == "poll":
                        print(
                            "{} invoked {} command in {}".format(
                                ctx.author.display_name, ctx.message.content, ctx.guild.name
                            )
                        )

                        await ctx.send(self.get_poll())

                else:
                    await ctx.send("To view information about the poll, type \"/view poll/results\".")
            else:
                await ctx.send("No poll started, type \"/poll\" to start a poll.")
