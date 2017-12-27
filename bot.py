import re
import json

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


def calc_hypergeo(params):
    N, M, n, y = params[0], params[1], params[2], params[3]
    if M < n:
        print(something)
    hipergeom = stats.hypergeom(M, n, N)
    x = np.arange(0, n+1)
    fmp = hipergeom.pmf(x)
    sfmp = list()
    sfmpyn = 0
    for index, val in enumerate(fmp):
        if index == 0:
            sfmp.append(val)
        else:
            sfmp.append(val+sfmp[index-1])
        if index == y:
            sfmpyn = val
        elif index > y and index <= n:
            sfmpyn += val
        else:
            pass
    sfmp0y = sfmp[y]
    plt.plot(x, fmp, '--')
    plt.vlines(x, 0, fmp, colors='b', lw=5, alpha=0.5)
    plt.title('Distribución Hipergeométrica')
    plt.ylabel('Probabilidad')
    plt.xlabel('Valores')
    plt.save('plt.jpg')
    return sfmp0y, sfmpyn

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

    if message.content.startswith('!Hg'):
        clean_msg = message.content.replace('!Hg', '')
        params = clean_msg.split(" ")
        if len(params) != 4:
            text = """
                Error, se requieren estos parámetros:
                N: Tamaño del mazo
                M: Número de cartas deseadas en el mazo
                n: Cantiadd de robos/turnos
                x: Número de copias que se quiere
            """
            await client.send_message(message.channel, text)
        else:
            a, b = calc_hypergeo(params)
            text = """
                sum(0 -> X) = {a}
                sum(X -> n) = {b}
            """.format(a=a, b=b)
            await client.send_message(message.channel, text)
            await client.send_file(message.channel, "plt.jpg")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_TOKEN)
