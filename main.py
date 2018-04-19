import logging
import re
import time
import traceback
from datetime import datetime
from threading import Thread

import telebot

import settings
from checker import multi_fetch


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger()
if settings.DEBUG:
    logger.setLevel(logging.DEBUG)

urls = []

async_bot = telebot.AsyncTeleBot(settings.TOKEN)
bot = telebot.TeleBot(settings.TOKEN, threaded=False)

message_id = None
chat_id = None

emoji_status = {
    200: '✅',
    404: '🙈',
    500: '❗',
    502: '💀',
    504: '🕚',
    998: '⚫️‍',
}


def generate_message_id():
    global message_id
    try:
        with open('old_message_id.txt') as f:
            message_id = int(f.read())
    except:
        message = bot.send_message(
            chat_id=settings.CHAT_ID,
            text='Получение данных от сервисов.'
        )
        message_id = message.message_id
        try:
            with open('old_message_id.txt', 'w') as f:
                f.write(str(message_id))
        except:
            print('Невозможно создать old_message_id.txt')


def check():
    while True:
        if message_id is None or not urls:
            time.sleep(5)
            continue

        urls_copy = urls.copy()
        statuses, errors = multi_fetch(urls_copy)
        lines = []
        first_line = ''
        for url, status in zip(urls, statuses):
            s = '`' if status != 200 else '*'
            e_status = emoji_status.get(status, "❓")
            first_line += e_status
            lines.append(f'{s}{status}{s}    {url}')

        statistics = "\n".join(lines)
        errors = filter(lambda x: x[1] is not None, zip(urls_copy, errors))
        errors_text = "\n\n".join(
            f'{url}\n`{error}`' for url, error in errors
        )
        text = (
            f'{first_line}\n'
            f'{datetime.now().strftime("`%H:%M:%S` %d.%m.%y")}\n\n'
            f'{statistics}\n\n'
            f'{errors_text}'
        )
        async_bot.edit_message_text(
            message_id=message_id,
            chat_id=settings.CHAT_ID,
            text=text,
            disable_web_page_preview=True,
            parse_mode='Markdown'
        )

        if any([s != 200 for s in statuses]):
            time.sleep(60)
        else:
            time.sleep(60*5)


def urls_updater():
    global urls
    while True:
        with open('urls.txt') as f:
            new_urls = re.findall(
                'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
                f.read()
            )
            if new_urls:
                urls = new_urls
        time.sleep(60*5)


def start_bot():
    enabled = False
    while True:
        try:
            time.sleep(10)
            if not enabled:
                bot.polling(none_stop=True, interval=0, timeout=20)
                enabled = True
        except KeyboardInterrupt:
            break
        except:
            try:
                enabled = False
                bot.send_message(
                    chat_id=167767298,
                    text='```' + traceback.format_exc() + '```',
                    parse_mode='Markdown'
                )
            except:
                logging.warning(traceback.format_exc())

            time.sleep(10)


if __name__ == '__main__':
    generate_message_id()
    Thread(target=urls_updater).start()
    Thread(target=check).start()
