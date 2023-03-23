# polling-bot

polling-bot is a Discord bot to conduct basic polling functions in a Discord server

[![Build Status](https://github.com/grnarayanan/polling-bot/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/grnarayanan/polling-bot/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/grnarayanan/polling-bot/branch/main/graph/badge.svg)](https://codecov.io/gh/grnarayanan/polling-bot)
![License](https://img.shields.io/github/license/grnarayanan/polling-bot.svg) ![GitHub issues](https://img.shields.io/github/issues/grnarayanan/polling-bot)

## Overview

Often times, reaching a consensus can be difficult without an organized method in place, and so this polling bot can be added to a Discord
server to solve that need in a simple and efficient manner. Use cases could include deciding with friends on a place to eat, what video game 
should be played, when to schedule a party, etc. 

The bot supports starting a poll and adding options for choices by the users. It will then keep track of responses made to the poll,
allow users to change their response, and surface the winner of the poll when called upon. 

## Details

This project is a pure python project using modern tooling. It uses a `Makefile` as a command registry, with the following commands:
- `make`: list available commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make lint`: perform static analysis of this library with `flake8` and `black`
- `make format`: autoformat this library using `black`
- `make annotate`: run type checking using `mypy`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information
- `make dist`: package library for distribution

## Setup

To setup the Discord bot, follow the steps below:
1. Navigate to http://discordapp.com/developers/applications and create an account, or login if you already have a Discord account. 
2. Select "New Application" and give it a name ie. "polling-bot"
3. Navigate to the Bot tab on the left side menu, and click "Add Bot" and confirm. 
4. Under the TOKEN section, click "Copy" and copy the token.
5. To add the bot to your Discord server, select the OAuth2 tab from the left side menu. From the SCOPES section, select bot option and from the BOT PERMISSIONS section, select Administrator. Copy and navigate to the generated URL and select the server you want to add the bot to from the dropdown, then click "Authorize."

Next, install polling-bot with pip: `pip install polling-bot`.

Navigate to the "polling-bot" directory and create a file called `.env` with the following content:

`DISCORD_TOKEN={token}`, where token is the token copied from the Developer Portal above. 

Finally, to run the bot, execute the command `python3 __main__.py`.

## Available Commands

`/poll` - Starts a poll in the server

`/add choice <content>` - Add choices to the poll

`/edit <option> <content>` - Edit the content of the poll

- Options are 'name', 'description', and 'choice'

`/vote <choice #>` - Vote for a choice in the poll

- Choice # is the # corresponding to the desired choice, viewable with `/view choices` or `/view poll`

`/view <option>` - View the contents and results of the poll

- Options are 'name', 'description', 'choices', 'poll', and 'results'

## Usage

Start by executing `/poll` to create a poll. Edit the name and description of the poll using the `/edit` command. Next, add choices to the poll using the `/add` command. Have users then vote on the choices by running `/view poll` to see the current state of the poll, and then voting on their desired selection using the `/vote` command. Once all users have voted and the poll has concluded, run `/view results` to view the results and winner of the poll.