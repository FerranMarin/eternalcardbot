import re
import json

import discord
from config import DISCORD_TOKEN

card_dict = dict()
with open('eternal-cards.json') as data_file:
    data = json.load(data_file)
    for row in data:
        card_dict[row['Name']] = row['ImageUrl']


def sanitize(inp):
    output = inp.replace("'", "").replace(' ', '')
    return output


def logic(card):
    options = []
    for option in card_dict.keys():
        if re.search(card.lower(), option.lower()):
            options.append(option)
    if len(options) == 1:
        return card_dict[options[0]]
    elif len(options) > 1:
        for option in options:
            if card.lower() == option.lower():
                return card_dict[option]
        return 'Multiple options: {options}'.format(options=options)


client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!carta'):
        clean_msg = message.content.replace('!carta ', '')
        if len(clean_msg) < 3:
            return
        card = logic(clean_msg)
        print(card)
        if card:
            await client.send_message(message.channel, card)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_TOKEN)
