import re
import json
import random

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
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


def dice(to_roll, to_save):
    dice_list = []
    ten_list = []
    result = 0
    for i in range(0, to_roll):
        dice_list.append(random.randint(1, 10))
    dice_list = sorted(dice_list, key=int)
    for item in dice_list[-to_save:]:
        if item == 10:
            x = ten()
            ten_list.append(x)
            result += x
        result += item
    return dice_list, ten_list, result


def ten():
    cont = True
    tmp_result = 0
    while cont:
        cont = False
        tmp = random.randint(1, 10)
        tmp_result += tmp
        if tmp == 10:
            cont = True
    return tmp_result


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

    if message.content.startswith('!roll'):
        clean_msg = message.content.replace('!roll', '')
        params = clean_msg.split("g")
        if len(params) != 2:
            text = """
                Error, el input ha de ser XgY:
                - X es el numero de dados a tirar
                - Y es el numero de dados a guardar
            """
            await client.send_message(message.channel, text)
        else:
            a, b, c = dice(int(params[0]), int(params[1]))
            text = """
                Todas las Tiradas: {a}
                Resultados del 10: {b}
                Resultado: {c}
            """.format(a=a, b=b, c=c)
            await client.send_message(message.channel, text)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_TOKEN)
