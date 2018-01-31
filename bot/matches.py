from telegram import InlineKeyboardButton, InlineKeyboardMarkup

games = {}

keyboard = [[InlineKeyboardButton(1, callback_data='matches_1'),
             InlineKeyboardButton(2, callback_data='matches_2'),
             InlineKeyboardButton(3, callback_data='matches_3'),
             InlineKeyboardButton(4, callback_data='matches_4')],

            [InlineKeyboardButton("Start new game", callback_data='matches_0')]]

reply_markup = InlineKeyboardMarkup(keyboard)


def matches_cmd(bot, update, args):
    player = update.message.chat.username
    games[player] = 21
    reply_text = f"Table: {'| ' * games[player]} \n Your turn: pick matches"
    update.message.reply_text(reply_text, reply_markup=reply_markup)


def matches_cb(bot, update):
    player = update.effective_message.chat.username
    state = games[player]
    move = int(update.callback_query.data)

    if move == 0:
        games[player] = 21
        response = f"Table: {'| ' * games[player]} \nYour turn: pick matches"
    else:
        response = _move(state, player, move)
    update.callback_query.message.edit_text(response, reply_markup=reply_markup)


def _move(state, player, move):
    state -= move
    ai = 5 - move
    state -= ai

    reply_text = f"Table [{state}]: {'| ' * state} \n"

    reply_text += f"You picked : {move}. AI picked : {ai} \n"


    if state == 1:
        reply_text += "You lose :("

    games[player] = state
    return reply_text
