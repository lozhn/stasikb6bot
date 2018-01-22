import os
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from tictactoe import tictactoe, button

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, \
            text=f'Hi {update.message.from_user.first_name}')


def hello(bot, update):
    update.message.reply_text(f'{update.message.from_user.first_name}')

def help(bot, update):
    update.message.reply_text(f'Enter /tictactoe to play in tic-tac-toe')

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

updater = Updater('487928890:AAGU3UCFlUt5_fmg-uNNl-TlXYLgGMEJUUg')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('tictactoe', tictactoe))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
updater.idle()
