import os
from time import time
import logging

from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async

from bot import config

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bot.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"
)


class StackPoint:
    def __init__(self):
        self.is_lock = False
        self._value = None
        with open(config.sp_data_filepath, 'r') as file:
            data = file.read()
            self._set_next_sp(data, True)

    def _set_next_sp(self, data, is_init=False):
        data = data.strip()
        if not data.isdecimal():
            logging.error(f"SP file contain wrong data: {data}. Current SP value: {self._value}")
            raise Exception()
        self._value = (int(data) + int(not is_init)) % len(config.students)

    def next(self):
        logging.info(f"Start getting next student. Current SP value: {self._value}")
        stime = time()
        while self.is_lock:
            if (time() - stime) < config.timeout:
                logging.error(f"SP timeout. SP={self._value}")
                raise TimeoutError()

        self.is_lock = True
        with open(config.sp_data_filepath, 'r') as file:
            data = file.read()
            self._set_next_sp(data)
        with open(config.sp_data_filepath, 'w') as file:
            # TODO: fix it
            file.write(f"{self._value}")
        self.is_lock = False
        logging.info(f"Finish getting next student. Current SP value: {self._value}")
        return config.students[self._value]

    def get_value(self) -> int:
        assert self._value is not None
        return self._value


@run_async
def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text='Страдания с удобством\n/next - перейти к следующему по очереди студенту\n/get - посмотреть очередь',
        parse_mode="MARKDOWN"
    )


@run_async
def next(bot, update):
    """Returns next student name and moves SP"""
    logging.info(f"Start procc request(next) from {update.message.chat_id} - {update.message.from_user.name}")
    from_id = update.message.chat_id
    if from_id not in config.teacher_ids:
        bot.sendMessage(chat_id=update.message.chat_id, text="**Forbidden**", parse_mode="MARKDOWN")
        return None
    next_student = sp.next()
    bot.sendMessage(chat_id=update.message.chat_id, text=f"**{next_student}**", parse_mode="MARKDOWN")
    logging.info(f"Finish procc request(next) from {update.message.chat_id} - {update.message.from_user.name}")


@run_async
def get(bot, update):
    """Returns student list with SP"""
    logging.info(f"Start procc request(get) from {update.message.chat_id} - {update.message.from_user.name}")
    queue = config.students[:]
    queue[sp.get_value()] = f"**{queue[sp.get_value()]}** ` <=`"
    bot.sendMessage(chat_id=update.message.chat_id, text="\n".join(queue), parse_mode="MARKDOWN")
    logging.info(f"Finish procc request(get) from {update.message.chat_id} - {update.message.from_user.name}")


sp = StackPoint()

try:
    assert config.bot_token
    assert config.students
    assert config.teacher_ids
    assert 0 <= sp.get_value() < len(config.students)
except AssertionError as e:
    logging.error("Wrong config")
    exit(-1)

updater = Updater(config.bot_token, **({'request_kwargs': {'proxy_url': config.proxy}} if config.proxy is not None else {}))

start_handler = CommandHandler('start', start)
next_handler = CommandHandler('next', next)
get_handler = CommandHandler('get', get)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(next_handler)
updater.dispatcher.add_handler(get_handler)
updater.start_polling()
updater.idle()
