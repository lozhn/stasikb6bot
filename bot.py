import os
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,  MessageHandler, Filters
import wolframalpha


# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
client = wolframalpha.Client("YKQ89L-69QK5EG99L")


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,text="Hi" + ' ' + update.message.from_user.first_name)


def hello(bot, update):
    update.message.reply_text("Hi" + ' ' + update.message.from_user.first_name)


def help(bot, update):
    update.message.reply_text('Enter /tictactoe to play in tic-tac-toe')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def callb_text(bot, update):
    res = client.query(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=next(res.results).text)
    # for pod in res.pod:
    #     for sub in pod.subpod:
    #         answer = "{} : {}".format(sub["img"]["@src"], sub["img"]["@alt"])
    #         bot.send_message(chat_id=update.message.chat_id, text=answer)


updater = Updater('487915411:AAGHGqvVl0s_MQIuS8LYmLPDwmVgWQydQ0g')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.dispatcher.add_handler(MessageHandler(Filters.text, callb_text))

updater.start_polling()
updater.idle()
