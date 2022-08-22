import os
import time
import requests


def message(msg: str, channel_id: int, token: str):
    payload = {
        'content': f'{msg}'
    }

    requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload,
                  headers={'authorization': token})


# noinspection PyBroadException
def mention(persons_id, channel_id, token):
    payload = {
        "content": f"<@{persons_id}>"
    }
    try:
        requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers={'authorization': token})
        print('sent mention')
    except:
        print('failed to send mention')


# noinspection PyBroadException
def join(code, token):
    if 'discord.gg/' in code:
        code = code.replace('discord.gg/', '')
        code = code.replace('https://', '')

    payload = '{}'
    try:
        requests.post(f'https://discord.com/api/v9/invites/{code}', data=payload, headers={'authorization': token})
    except:
        pass


def spoiler_spam(channel_id, token):
    newspam = ''
    for _ in range(30):
        newspam += f'||e||'

    payload = {
        "content": f"{newspam}"
    }

    requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers={'authorization': token})


def account_info(token, types):
    e = requests.get('https://discord.com/api/v9/users/@me', headers={'authorization': token}).json()
    print(e)
    if types == 'whole':
        return e
    if types == 'discriminator':
        return e['discriminator']
    if types == 'username':
        return e['username']
    if types == 'avatar':
        return e['avatar']
    if types == 'id':
        return e['id']


def auto_discriminator(token, password, wanted_discriminator):
    # change name to #number to get a new one
    Token = {
        "authorization": f"{token}",
        "content-type": "application/json"
    }
    token = {
        "authorization": f"{token}",
    }
    discriminator = account_info(token, 'discriminator')
    while True:
        if discriminator != wanted_discriminator:
            payload = {
                "username": f"{discriminator}",
                "password": f"{password}"
            }
            print(payload)
            requests.patch('https://discord.com/api/v9/users/@me', json=payload, headers={'authorization': token})
        time.sleep(10)


def change_name(password, token):
    pass


def get_messages(channel_id, token, returns=False):
    d = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=100', headers={'authorization': token}).text
    with open(f'msgs\\{channel_id}.json', 'w') as e:
        e.write(d)
    if returns:
        return d


# noinspection PyGlobalUndefined
def self_reply(msg, channel, token, wait_time):
    global msg_id
    initial_msg = False
    msg = msg.split(' ')
    if not initial_msg:
        payload = {
            "content": f"{str(msg[0])}"
        }

        d = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", data=payload, headers={'authorization': token}).text
        d = d.split(',')
        msg_id = d[0].replace('{"id": "', '').replace('"', '')
        initial_msg = True
    msg_num = 0
    if initial_msg:
        for _ in msg:
            time.sleep(wait_time)
            if msg_num != 0:
                payload = {
                    "content": f"{_}",
                    "message_reference": {
                        "channel_id": f"{channel}",
                        "message_id": f"{msg_id}"
                    }
                }
                d = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", json=payload,
                                  headers={"authorization": f"{token}","content-type": "application/json"}).text
                d = d.split(',')
                msg_id = d[0].replace('{"id": "', '').replace('"', '')
            msg_num += 1


def reply(msg, channel, msgid, token):
    requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", json={"content": f"{msg}","message_reference": {"channel_id": f"{channel}","message_id": f"{msgid}"}}, headers={'authorization': token})


def ghost_ping(persons_id, channel, token):
    d = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", data={'content': f'<@{persons_id}>'}, headers={'authorization': token}).text
    d = d.split(',')
    msg__id = d[0].replace("'['{", '').replace('"id": "', '').replace('"', '').replace("'", '').replace('{', '')
    requests.delete(f'https://discord.com/api/v9/channels/{channel}/messages/{msg__id}', headers={'authorization': token})


def send_code(code, channel, token):
    payload = {
        'content': f'```py\n{code}```'
    }
    print(payload)
    print(requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", data=payload, headers=token))


def upload_code(code):
    banner = 'this was sent by a request\n\n'
    real_bytes_code = banner.encode('utf-8') + code.encode('utf-8')
    e = requests.post('https://paste.pythondiscord.com/documents', data=real_bytes_code).text
    print(f'https://paste.pythondiscord.com/' + str(e).replace('{"key":"', '').replace('"}', '') + '.py')


def server_nick(guild_id, new_nickname, token):
    print(requests.patch(f'https://discord.com/api/v9/guilds/{guild_id}/members/@me', json={"nick": f"{new_nickname}"}, headers={'authorization': token}).text)


def profile_color(rgb, token):
    # noinspection PyGlobalUndefined
    def get_accent(rgb_value):
        global final_number, number
        rgb2 = []
        amount = 0
        amount2 = -1
        final_number = 0
        for item in rgb_value:
            rgb2.append(item)
        for _ in rgb2:
            amount += 1
        for _ in rgb2:
            amount = amount - 1
            amount2 += 1
            if rgb2[amount] == 'f' or rgb2[amount] == 'F':
                number = 15
            elif rgb2[amount] == 'e' or rgb2[amount] == 'E':
                number = 14
            elif rgb2[amount] == 'd' or rgb2[amount] == 'D':
                number = 13
            elif rgb2[amount] == 'c' or rgb2[amount] == 'C':
                number = 12
            elif rgb2[amount] == 'b' or rgb2[amount] == 'B':
                number = 11
            elif rgb2[amount] == 'a' or rgb2[amount] == 'A':
                number = 10
            else:
                number = rgb[amount]
            final_number += int(number) * 16 ** int(amount2)
        return final_number

    requests.patch('https://discord.com/api/v9/users/@me', json={"accent_color": get_accent(rgb_value=rgb)}, headers={'authorization': token})


def emoji_message(messages, channel_id, token):
    msg = messages.replace('a', "🇦").replace('A', '🇦').replace('b', '🇧').replace('B', '🇧').replace('c',
                                                                                                       '🇨').replace(
        'C',
        '🇨').replace(
        'd', '🇩').replace('D', '🇩').replace('e', '🇪').replace('E', '🇪').replace('f', '🇫').replace('F',
                                                                                                       '🇫').replace(
        'g', '🇬').replace('G', '🇬').replace('h', '🇭').replace('H', '🇭').replace('i', '🇮').replace('I',
                                                                                                       '🇮').replace(
        'j', '🇯').replace('J', '🇯').replace('k', '🇰').replace('K', '🇰').replace('l', '🇱').replace('L',
                                                                                                       '🇱').replace(
        'm', '🇲').replace('M', '🇲').replace('n', '🇳').replace('N', '🇳').replace('o', '🇴').replace('O',
                                                                                                       '🇴').replace(
        'p', '🇵').replace('P', '🇵').replace('q', '🇶').replace('Q', '🇶').replace('r', '🇷').replace('R',
                                                                                                       '🇷').replace(
        's', '🇸').replace('S', '🇸').replace('t', '🇹').replace('T', '🇹').replace('u', '🇺').replace('U',
                                                                                                       '🇺').replace(
        'v', '🇻').replace('V', '🇻').replace('w', '🇼').replace('W', '🇼').replace('x', '🇽').replace('X',
                                                                                                       '🇽').replace(
        'y', '🇾').replace('Y', '🇾').replace('z', '🇿').replace('Z', '🇿')
    new_msg = ''
    for item in msg:
        new_msg += item + ' '

    requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data={'content': f'{new_msg}'}, headers=token)


def download_pfp(token, size):
    avatar = account_info(token=token, types='avatar')
    id = account_info(token={'authorization': token}, types='id')
    r = requests.get(f'https://cdn.discordapp.com/avatars/{id}/{avatar}.webp?size={size}')
    if r.status_code == 200:
        with open(f'pfps\\{avatar}.png', 'wb') as f:
            f.write(r.content)

def emoji_exploit(token, guild_id):
    res = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/emojis', headers={'authorization': token})
    print(res.json())
    for item in res.json():
        if item['animated']:
            print(item['name'], 'animated '+f'https://cdn.discordapp.com/emojis/{item["id"]}.gif?size=128&quality=lossless')
        if not item['animated']:
            print(item['name'], 'not animated '+f'https://cdn.discordapp.com/emojis/{item["id"]}.webp?size=128&quality=lossless')
