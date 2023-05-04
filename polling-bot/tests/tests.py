import sys
import os
import time
import discord
import coverage
import unittest
from unittest.mock import Mock
from collections import defaultdict
from faker import Faker
from random import randint

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from polling_bot import PollingBot


class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = PollingBot(intents=discord.Intents.all(), command_prefix="/")
        self.faker = Faker()

    # UNIT TESTS
    def test_init(self):
        intents_test = discord.Intents.all()
        command_prefix_test = "/"

        bot_test = PollingBot(intents=intents_test, command_prefix=command_prefix_test)

        self.assertEqual(bot_test.intents, intents_test)
        self.assertEqual(bot_test.command_prefix, command_prefix_test)

    def test_create_poll(self):
        self.bot.create_poll()

        self.assertIsInstance(self.bot.poll_data, type(defaultdict()))
        self.assertIsInstance(self.bot.poll_data["Choices"], type(defaultdict()))
        self.assertIsInstance(self.bot.poll_data["Votes"], type(defaultdict()))
        self.assertEqual(self.bot.num_choices, 0)

    def test_add_choice(self):
        num_choices = randint(1, 100)
        self.bot.num_choices = num_choices
        self.bot.poll_data = defaultdict()
        self.bot.poll_data["Choices"] = defaultdict()
        self.bot.poll_data["Votes"] = defaultdict()

        test_choice = self.faker.text()

        self.bot.add_choice(test_choice)

        self.assertEqual(self.bot.num_choices, num_choices + 1)
        self.assertEqual(self.bot.poll_data["Choices"][self.bot.num_choices], test_choice)

    def test_add_vote(self):
        self.bot.poll_data = defaultdict()
        self.bot.poll_data["Choices"] = defaultdict()
        self.bot.poll_data["Votes"] = defaultdict()
        self.bot.voters = defaultdict()
        num_choice = randint(1, 100)
        user = self.faker.name()

        self.assertEqual(False, self.bot.add_vote(num_choice, user))

        self.bot.poll_data["Choices"][num_choice] = self.faker.text()
        old_votes = randint(1, 100)
        self.bot.poll_data["Votes"][num_choice] = old_votes

        self.bot.add_vote(num_choice, user)

        self.assertEqual(self.bot.poll_data["Votes"][num_choice], old_votes + 1)
        self.assertEqual(False, self.bot.add_vote(num_choice, user))

    def test_edit_name(self):
        self.bot.poll_data = defaultdict()
        new_name = self.faker.text()

        self.bot.edit_name(new_name)

        self.assertEqual(self.bot.poll_data["Name"], new_name)

    def test_edit_description(self):
        self.bot.poll_data = defaultdict()
        new_description = self.faker.text()

        self.bot.edit_description(new_description)

        self.assertEqual(self.bot.poll_data["Description"], new_description)

    def test_edit_choice(self):
        self.bot.poll_data = defaultdict()
        self.bot.poll_data["Choices"] = defaultdict()
        new_choice = self.faker.text()
        num_choice = randint(1, 100)
        self.bot.poll_data["Choices"][num_choice] = self.faker.text()

        self.assertEqual(self.bot.edit_choice(new_choice, num_choice), True)
        self.assertEqual(self.bot.poll_data["Choices"][num_choice], new_choice)

    def test_edit_duration(self):
        self.bot.duration = randint(1, 100)
        new_duration = randint(1, 100)

        self.bot.edit_duration(new_duration)

        self.assertEqual(new_duration * 60, self.bot.duration)

    def test_get_poll(self):
        self.bot.poll_data = defaultdict()
        name = self.faker.text()
        self.bot.poll_data["Name"] = name
        description = self.faker.text()
        self.bot.poll_data["Description"] = description
        self.bot.poll_data["Choices"] = defaultdict()
        self.bot.poll_data["Votes"] = defaultdict()
        self.bot.voters = defaultdict()
        num_choices = randint(1, 10)
        for i in range(num_choices):
            choice = self.faker.name()
            self.bot.poll_data["Choices"][i] = choice
            self.bot.voters[self.faker.name()] = choice
            self.bot.poll_data["Votes"][i] = randint(1, 100)

        expected_msg = "**" + name + "**" + "\n" + "*" + description + "*" + "\n\n"
        expected_msg += "__Choices:__\n"
        for num_choice, choice in self.bot.poll_data["Choices"].items():
            voters = ""
            for key, value in self.bot.voters.items():
                if value == choice:
                    voters += key + ", "
            expected_msg += (
                str(num_choice)
                + ") "
                + choice
                + "\t\t"
                + "Votes: "
                + str(self.bot.poll_data["Votes"][num_choice])
                + "\t"
                + " (*"
                + voters[: len(voters) - 2]
                + "*)"
                + "\n"
            )

        expected_msg += "\n" + "*Voters: "

        for voter in self.bot.voters.keys():
            expected_msg += voter + ", "

        expected_msg = expected_msg[: len(expected_msg) - 2] + "*"

        self.assertEqual(self.bot.get_poll(), expected_msg)

    def test_get_name(self):
        self.bot.poll_data = defaultdict()
        name = self.faker.text()
        self.bot.poll_data["Name"] = name

        self.assertEqual(self.bot.get_name(), name)

    def test_get_description(self):
        self.bot.poll_data = defaultdict()
        description = self.faker.text()
        self.bot.poll_data["Description"] = description

        self.assertEqual(self.bot.get_description(), description)

    def test_get_choices(self):
        self.bot.poll_data = defaultdict()
        choices = self.faker.profile()
        self.bot.poll_data["Choices"] = defaultdict()
        self.bot.poll_data["Votes"] = defaultdict()
        self.bot.voters = defaultdict()
        num_choices = randint(1, 10)
        for i in range(num_choices):
            choice = self.faker.name()
            self.bot.poll_data["Choices"][i] = choice
            self.bot.voters[self.faker.name()] = choice
            self.bot.poll_data["Votes"][i] = randint(1, 100)

        expected_msg = ""
        expected_msg += "__Choices:__\n"
        for num_choice, choice in self.bot.poll_data["Choices"].items():
            voters = ""
            for key, value in self.bot.voters.items():
                if value == choice:
                    voters += key + ", "
            expected_msg += (
                str(num_choice)
                + ") "
                + choice
                + "\t\t"
                + "Votes: "
                + str(self.bot.poll_data["Votes"][num_choice])
                + "\t"
                + " (*"
                + voters[: len(voters) - 2]
                + "*)"
                + "\n"
            )

        self.assertEqual(self.bot.get_choices_with_voters(), expected_msg[: len(expected_msg) - 1])

    def test_get_choices_with_voters(self):
        self.bot.poll_data = defaultdict()
        choices = self.faker.profile()
        self.bot.poll_data["Choices"] = defaultdict()
        self.bot.poll_data["Votes"] = defaultdict()
        num_choices = randint(1, 10)
        for i in range(num_choices):
            self.bot.poll_data["Choices"][i] = self.faker.name()
            self.bot.poll_data["Votes"][i] = randint(1, 100)

        expected_msg = "__Choices:__\n"
        for num_choice, choice in self.bot.poll_data["Choices"].items():
            expected_msg += str(num_choice) + ") " + choice + "\n"

        self.assertEqual(self.bot.get_choices(), expected_msg[: len(expected_msg) - 1])

    def test_get_voters(self):
        self.bot.voters = defaultdict()
        for i in range(randint(1, 10)):
            self.bot.voters[self.faker.name()] = self.faker.text()

        expected_msg = "*Voters: "

        for voter in self.bot.voters.keys():
            expected_msg += voter + ", "

        expected_msg = expected_msg[: len(expected_msg) - 2] + "*"

        self.assertEqual(expected_msg, self.bot.get_voters())

    def test_get_results(self):
        self.bot.poll_data = defaultdict()
        self.bot.poll_data["Name"] = self.faker.text()
        self.bot.poll_data["Choices"] = defaultdict()
        self.bot.poll_data["Votes"] = defaultdict()
        num = randint(1, 10)
        self.bot.num_choices = num
        for i in range(0, num):
            self.bot.poll_data["Choices"][i] = self.faker.name()
            self.bot.poll_data["Votes"][i] = i + 1

        expected_msg = (
            "The winner of " + self.bot.get_name() + " is:\n" + "**" + self.bot.poll_data["Choices"][num - 1] + ",**"
        )
        expected_msg += " *with " + str(num) + " votes!*"

        self.assertNotEqual(self.bot.get_results(), (None, None))
        self.assertEqual(self.bot.get_results(), expected_msg)

    def test_check_time(self):
        self.bot.start_time = time.time()
        self.bot.duration = 60

        self.assertEqual(self.bot.check_time(), True)

        self.bot.duration = 0
        self.assertEqual(self.bot.check_time(), False)

    # INTEGRATION TEST
    def test_conduct_poll(self):
        self.bot.create_poll()
        name = self.faker.text()
        description = self.faker.text()
        self.bot.edit_name(name)
        self.bot.edit_description(description)

        num = randint(1, 20)
        for i in range(0, num):
            self.bot.add_choice(self.faker.name())
            for _ in range(0, i):
                user = self.faker.name()
                self.bot.add_vote(i, user)

        expected_msg = (
            "The winner of " + self.bot.get_name() + " is:\n" + "**" + self.bot.poll_data["Choices"][num - 1] + ",**"
        )
        expected_msg += " *with " + str(num - 1) + " votes!*"

        self.assertEqual(self.bot.get_name(), name)
        self.assertEqual(self.bot.get_description(), description)
        self.assertEqual(self.bot.get_results(), expected_msg)


if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()

    unittest.main()

    cov.stop()
    cov.report()
