import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from bot.start import start_cmd
from bot.help import help_cmd_factory
from bot.matches import matches_cmd, matches_cb
from bot.tictactoe import tictactoe_cmd, tictactoe_cb
import wolframalpha

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

<<<<<<< HEAD
def common_cb_handler(bot, update):
    path, val = update.callback_query.data.split('_')
    update.callback_query.data = val

    if path == 'tictactoe':
        tictactoe_cb(bot, update)
=======
from bot.tictactoe import tictactoe, button
from bot.calculator import calculator
from bot.xo import xo_game, xo_move, XOFilter

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
>>>>>>> xo 5 in row

    if path == 'matches':
        matches_cb(bot, update)

    if path == 'xo':
        pass


def run(env):
    if not env:
        raise Exception("No env")

    updater = Updater(env['TELEGRAM_TOKEN'])

<<<<<<< HEAD
    help = help_cmd_factory(env['HELP_TEXT'])
    start = start_cmd
    client = wolframalpha.Client(env['WOLFRAM_TOKEN'])

    def _calculator_cmd(bot, update):
        res = client.query(update.message.text)
        update.message.reply_text(next(res.results).text)

    updater.dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('help', help, pass_args=True))

    updater.dispatcher.add_handler(CommandHandler('tictactoe', tictactoe_cmd, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('matches', matches_cmd, pass_args=True))


    updater.dispatcher.add_handler(MessageHandler(Filters.text, _calculator_cmd))
    updater.dispatcher.add_handler(CallbackQueryHandler(common_cb_handler))
=======
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('help',  help))
    updater.dispatcher.add_handler(CommandHandler('tictactoe', tictactoe))
    updater.dispatcher.add_handler(CommandHandler('xo',  xo_game))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    #updater.dispatcher.add_handler(MessageHandler(Filters.text, calculator))

    updater.dispatcher.add_handler(MessageHandler(XOFilter(), xo_move))
>>>>>>> xo 5 in row

    updater.start_polling()
    updater.idle()
