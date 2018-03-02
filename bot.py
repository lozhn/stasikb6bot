import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from bot.quit import quit_cmd_factory
from bot.start import start_cmd
from bot.help import help_cmd_factory
from bot.matches import matches_cmd, matches_cb
from bot.tictactoe import tictactoe_cmd, tictactoe_cb
from bot.xo import xo_cmd, xo_move
from bot.calculator import calculator_cmd_factory
from bot.tranlater import translate_cmd_factory
import locale
locale.setlocale(locale.LC_ALL, '')

logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def common_cb_handler(bot, update):
    path, val = update.callback_query.data.split('_')
    update.callback_query.data = val

    if path == 'tictactoe':
        tictactoe_cb(bot, update)

    if path == 'matches':
        matches_cb(bot, update)


def run(env):
    if not env:
        raise Exception("No env")

    updater = Updater(env['TELEGRAM_TOKEN'])

    helper_cmd = help_cmd_factory(env['HELP_TEXT'])
    calculator_cmd = calculator_cmd_factory(env['WOLFRAM_TOKEN'])
    quit_cmd = quit_cmd_factory(updater)
    translate = translate_cmd_factory(env['TRANSLATE_API'])

    # Defaults
    updater.dispatcher.add_handler(CommandHandler(
        'start', start_cmd, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler(
        'help', helper_cmd, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler(
        'quit', quit_cmd))

    # Tic-tac-toe
    updater.dispatcher.add_handler(CommandHandler(
        'tictactoe', tictactoe_cmd, pass_args=True))

    # Mathces
    updater.dispatcher.add_handler(CommandHandler(
        'matches', matches_cmd, pass_args=True))

    # Calculator
    updater.dispatcher.add_handler(CommandHandler(
        'calc', calculator_cmd, pass_args=True))

    # XO
    updater.dispatcher.add_handler(CommandHandler(
        'xo', xo_cmd, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler(
        'move', xo_move, pass_args=True))

    # Translator
    updater.dispatcher.add_handler(CommandHandler(
        'translate', translate, pass_args=True))

    # a.k.a. Callback Router
    updater.dispatcher.add_handler(CallbackQueryHandler(common_cb_handler))

    updater.start_polling()
    updater.idle()
