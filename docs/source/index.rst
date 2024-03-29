.. polling-bot documentation master file, created by
   sphinx-quickstart on Sat Apr  1 18:06:03 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to polling-bot's documentation!
=======================================

.. role:: bash(code)
   :language: bash

polling-bot is a Discord bot to conduct basic polling functions in a Discord server.

Setup
======

To setup the Discord bot, follow the steps below:

1. Navigate to http://discordapp.com/developers/applications and create an account, or login if you already have a Discord account. 

2. Select "New Application" and give it a name ie. "polling-bot"

3. Navigate to the Bot tab on the left side menu, and click "Add Bot" and confirm. 

4. Under the TOKEN section, click "Copy" and copy the token.

5. To add the bot to your Discord server, select the OAuth2 tab from the left side menu. From the SCOPES section, select bot option and from the BOT PERMISSIONS section, select Administrator. Copy and navigate to the generated URL and select the server you want to add the bot to from the dropdown, then click "Authorize."

Next, install polling-bot with pip: :bash:`pip install polling-bot`

Finally, to run the bot, import and run it as follows:

.. code-block:: python

   import discord
   pollingbot = __import__("polling-bot")
   
   bot = pollingbot.PollingBot(intents=discord.Intents.all(), command_prefix="/")
   bot.run('TOKEN')

Where token is the token copied from the Developer Portal above.

The bot will now be responsive to commands in your Discord server. 


Available Commands
==================

:bash:`/poll` - Starts a poll in the server

   .. image:: demos/poll.png
      :width: 300
      :alt: Example usage of /poll command

:bash:`/add choice <content>` - Add choices to the poll

   .. image:: demos/add.png
      :width: 300
      :alt: Example usage of /add name command

:bash:`/edit <option> <content>` - Edit the content of the poll

   .. image:: demos/edit.png
      :width: 300
      :alt: Example usage of /edit name command

- Options are 'name', 'description', and 'choice'

:bash:`/vote <choice #>` - Vote for a choice in the poll
   
   .. image:: demos/vote.png
         :width: 300
         :alt: Example usage of /vote command

- Choice # is the # corresponding to the desired choice, viewable with :bash:`/view choices` or :bash:`/view poll`
   
:bash:`/view <option>` - View the contents and results of the poll

   .. image:: demos/results.png
      :width: 300
      :alt: Example usage of /view results command

- Options are 'name', 'description', 'choices', 'poll', and 'results'


Usage
=====

Start by executing :bash:`/poll` to create a poll. 
Edit the name and description of the poll using the :bash:`/edit` command. 
Next, add choices to the poll using the :bash:`/add` command. 
The poll name and description can be modified at any time using the :bash:`edit name/description` command followed by the new text.
The poll choices can be modified by using the :bash:`/edit choice #` followed by the new choice label, where # is the choice number in the poll.
Have users then vote on the choices by running :bash:`/view poll` to see the current state of the poll, and then voting on their desired selection using the :bash:`/vote` command. 
Once all users have voted and the poll has concluded, run :bash:`/view results` to view the results and winner of the poll. 
If there are multiple winners of the poll, then they all will be displayed. 

.. image:: demos/long-version.gif
   :width: 300
   :alt: Quick demo using polling-bot in a Discord server

.. rst-class:: page-break

Documentation
=============

.. automodule:: polling_bot
   :members:
   :undoc-members:
   :show-inheritance:

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
