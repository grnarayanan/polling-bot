# -*- coding: utf-8 -*-
"""
polling-bot for Discord

Conduct basic polling functions in a Discord server

@author: Ganesan Narayanan
"""

import os
import discord
from dotenv import load_dotenv
from polling_bot import PollingBot

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('TOKEN')

    bot = PollingBot(intents=discord.Intents.all(), command_prefix="/")
    bot.run(token)
