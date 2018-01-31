import os
import logging


from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,  MessageHandler, Filters

from bot.tictactoe import tictactoe, button
from bot.calculator import calculator
from bot.xo import xo_game, xo_move, XOFilter

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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


def run(env):
    if not env:
        raise "No env"

    updater = Updater(env['TELEGRAM_TOKEN'])

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('help',  help))
    updater.dispatcher.add_handler(CommandHandler('tictactoe', tictactoe))
    updater.dispatcher.add_handler(CommandHandler('xo',  xo_game))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    #updater.dispatcher.add_handler(MessageHandler(Filters.text, calculator))

    updater.dispatcher.add_handler(MessageHandler(XOFilter(), xo_move))

    updater.start_polling()
    updater.idle()
