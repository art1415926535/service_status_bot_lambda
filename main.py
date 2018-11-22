from datetime import datetime
import os

import telebot
import dateutil.tz

from checker import get_status_codes


urls = [u.strip() for u in os.environ.get('urls').split(',')]

token = os.environ.get('token')
bot = telebot.TeleBot(token, threaded=False)

message_id = os.environ.get('message_id')
chat_id = os.environ.get('chat_id')

tz = dateutil.tz.gettz(os.environ.get('tz'))


status_code_to_emoji = {
    200: '✅',
    404: '🙈',
    500: '❗',
    502: '💀',
    504: '🕚',
    None: '❓'
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
        emoji = status_code_to_emoji.get(status, status_code_to_emoji[None])
        first_line += emoji
        message_lines.append(f'{tag}{status}{tag}    {url}')

    # fix for very large lines
    if len(first_line) > 10:
        new_first_line_data = []
        for emoji in status_code_to_emoji.values():
            if emoji in first_line:
                new_first_line_data.append(f'{emoji}×'
                                           f'{first_line.count(emoji)}')

        first_line = f'`{"  ".join(new_first_line_data)}    `'

    statistics = "\n".join(message_lines)
    errors = filter(lambda x: x[1] is not None, zip(urls, errors))
    errors_text = "\n\n".join(
        f'{url}\n`{error}`' for url, error in errors
    )
    text = (
        f'{first_line}\n'
        f'{datetime.now(tz=tz).strftime("`%H:%M:%S` %d.%m.%y")}\n\n'
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
