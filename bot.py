import os
import logging
from telegram.ext import Updater, CommandHandler
import tictactoe

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, \
            text=f'Hi {update.message.from_user.first_name}')


def hello(bot, update):
    update.message.reply_text(f'{update.message.from_user.first_name}')

updater = Updater(os.environ.get('TELEGRAM_TOKEN'))

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('tictactoe', tictactoe))

updater.start_polling()
updater.idle()
