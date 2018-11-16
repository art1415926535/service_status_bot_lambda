from datetime import datetime
import os

import telebot

from checker import get_status_codes


urls = [u.strip() for u in os.environ.get('urls').split(',')]

token = os.environ.get('token')
bot = telebot.TeleBot(token, threaded=False)

message_id = os.environ.get('message_id')
chat_id = os.environ.get('chat_id')

status_code_to_emoji = {
    200: '✅',
    404: '🙈',
    500: '❗',
    502: '💀',
    504: '🕚',
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

    codes, errors = list(zip(*get_status_codes(urls)))
    message_lines = []
    first_line = ''
    for url, status in zip(urls, codes):
        tag = '*' if status == 200 else '`'
        emoji = status_code_to_emoji.get(status, "❓")
        first_line += emoji
        message_lines.append(f'{tag}{status}{tag}    {url}')

    statistics = "\n".join(message_lines)
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
        message_id=message_id,
        chat_id=chat_id,
        text=text,
        disable_web_page_preview=True,
        parse_mode='Markdown'
    )

    return {'result': 'ok'}
