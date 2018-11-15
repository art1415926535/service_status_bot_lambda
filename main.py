from datetime import datetime
import os

import telebot

from checker import multi_fetch


urls = [u.strip() for u in os.environ.get('urls').split(',')]

token = os.environ.get('token')
bot = telebot.TeleBot(token, threaded=False)

message_id = os.environ.get('message_id')
chat_id = os.environ.get('chat_id')

emoji_status = {
    200: '✅',
    404: '🙈',
    500: '❗',
    502: '💀',
    504: '🕚',
    998: '⚫️‍',
}


def handler(event, context):
    if not all((urls, token, message_id, chat_id)):
        return {
            'error': 'config error',
            'token': token,
            'message_id': message_id,
            'chat_id': chat_id,
            'urls': urls,
        }

    statuses, errors = list(zip(*multi_fetch(urls)))
    lines = []
    first_line = ''
    for url, status in zip(urls, statuses):
        s = '`' if status != 200 else '*'
        e_status = emoji_status.get(status, "❓")
        first_line += e_status
        lines.append(f'{s}{status}{s}    {url}')

    statistics = "\n".join(lines)
    errors = filter(lambda x: x[1] is not None, zip(urls, errors))
    errors_text = "\n\n".join(
        f'{url}\n`{error}`' for url, error in errors
    )
    text = (
        f'{first_line}\n'
        f'{datetime.now().strftime("`%H:%M:%S` %d.%m.%y")}\n\n'
        f'{statistics}\n\n'
        f'{errors_text}'
    )
    bot.edit_message_text(
        message_id=os.environ.get('message_id'),
        chat_id=os.environ.get('chat_id'),
        text=text,
        disable_web_page_preview=True,
        parse_mode='Markdown'
    )

    return {
        'result': 'ok',
    }
