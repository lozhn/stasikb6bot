import os
import logging

import wolframalpha

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,  MessageHandler, Filters

from bot.tictactoe import tictactoe, button
from bot.calculator import calculator

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
client = wolframalpha.Client("YKQ89L-69QK5EG99L")
updater = Updater('487928890:AAGU3UCFlUt5_fmg-uNNl-TlXYLgGMEJUUg')

def run():
    updater.start_polling()
    updater.idle()

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, \
                        text=f'Hi {update.message.from_user.first_name}')

def hello(bot, update):
    update.message.reply_text(f'Hi {update.message.from_user.first_name}')

def help(bot, update):
    update.message.reply_text(f'Enter /tictactoe to play in tic-tac-toe')

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('help',  help))
updater.dispatcher.add_handler(CommandHandler('tictactoe', tictactoe))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(MessageHandler(Filters.text, calculator))

if __name__ == '__main__':
    run()
