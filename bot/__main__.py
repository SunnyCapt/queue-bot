from time import time
from logging import getLogger

import locker
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

from bot import config


logger = getLogger("general")


class StackPoint:
    def __init__(self, students):
        self.students = students
        self.is_lock = False
        self.value = None

    def next(self):
        stime = time()

        while self.is_lock:
            if (time() - stime) < config.timeout:
                logger.error(f"SP timeout. SP={self.value}")
                raise TimeoutError()

        self.is_lock = True
        with open(config.sp_data_filepath, 'w') as file:
            data = file.read()
        if not data.isdecimal():
            logger.error(f"SP file contain wrong data: {data}. Current SP value: {self.value}")
            raise Exception()
        self.value = int(data)
        self.is_lock = False




@run_async
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Страдания с удобством<br><br>/next - перейти к следующему по очереди студенту.<br>/get - посмотреть очередь', parse_mode="HTML")


@run_async
def next(bot, update):
    """Returns next student name and moves SP"""
    from_id = update.message.chat_id
    if not from_id in config.teachers:
        bot.sendMessage(chat_id=update.message.chat_id, text="<strong>Forbidden</strong>", parse_mode="HTML")


@run_async
def get(bot, update):
    """Returns student list with SP"""
    pass


try:
    assert config.bot_token
    assert config.students
    assert config.teachers
except AssertionError as e:
    logger.error("Wrong config")
    exit(-1)

updater = Updater(token=config.bot_token)  # , request_kwargs={'proxy_url':"protocol://host:port"} )
start_handler = CommandHandler('start', start)
text_handler = MessageHandler(Filters.text, text)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(text_handler)
updater.start_polling()
updater.idle()
