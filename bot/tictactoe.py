from telegram import InlineKeyboardButton, InlineKeyboardMarkup

games = {}

def tictactoe_cmd(bot, update, args):
    player = update.message.chat.username
    print("tictactoe command " + player)
    games[player] = _newboard()

    keyboard = [[InlineKeyboardButton(games[player][0], callback_data='tictactoe_0'),
                 InlineKeyboardButton(games[player][1], callback_data='tictactoe_1'),
                 InlineKeyboardButton(games[player][2], callback_data='tictactoe_2')],
                [InlineKeyboardButton(games[player][3], callback_data='tictactoe_3'),
                 InlineKeyboardButton(games[player][4], callback_data='tictactoe_4'),
                 InlineKeyboardButton(games[player][5], callback_data='tictactoe_5')],
                [InlineKeyboardButton(games[player][6], callback_data='tictactoe_6'),
                 InlineKeyboardButton(games[player][7], callback_data='tictactoe_7'),
                 InlineKeyboardButton(games[player][8], callback_data='tictactoe_8')],
                [InlineKeyboardButton("Start new game", callback_data='tictactoe_9')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Your turn, ' + update.message.chat.username + ':', reply_markup=reply_markup)


def _newboard():
    return [".", ".", ".", ".", ".", ".", ".", ".", "."]


def tictactoe_cb(bot, update):
    query = update.callback_query
    move = int(query.data)
    player = update.effective_message.chat.username
    print("tictactoe turn " + player)
    new_message = 'Your turn, ' + player + ':'
    current_text = update.callback_query.message.text

    if (move == 9):
        games[player] = _newboard()
        print("tictactoe newgame " + player)
    elif (current_text == "You win" or current_text == "I win"):
        new_message = current_text
        print("tictactoe still_win/lose " + player)
    elif (0 <= move < 9):
        board = games[player]

        if board[move] == ".":
            board[move] = "X"

            if _i_won("X", board):
                new_message = "You win"
                print("tictactoe win " + player)
            elif (len([i for i in board if i == "."]) > 0):
                board[_getmove(board)] = "O"
                if _i_won("O", board):
                    new_message = "I win"
                    print("tictactoe lose " + player)
            else:
                new_message = "Game ended"
                print("tictactoe endgame " + player)
        else:
            new_message = "Incorrect move"
            print("tictactoe incor_move " + player)

    keyboard = [[InlineKeyboardButton(games[player][0], callback_data='tictactoe_0'),
                 InlineKeyboardButton(games[player][1], callback_data='tictactoe_1'),
                 InlineKeyboardButton(games[player][2], callback_data='tictactoe_2')],
                [InlineKeyboardButton(games[player][3], callback_data='tictactoe_3'),
                 InlineKeyboardButton(games[player][4], callback_data='tictactoe_4'),
                 InlineKeyboardButton(games[player][5], callback_data='tictactoe_5')],
                [InlineKeyboardButton(games[player][6], callback_data='tictactoe_6'),
                 InlineKeyboardButton(games[player][7], callback_data='tictactoe_7'),
                 InlineKeyboardButton(games[player][8], callback_data='tictactoe_8')],
                [InlineKeyboardButton("Start new game", callback_data='tictactoe_9')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # update.message.edit_reply_markup(reply_markup=reply_markup) #обновление только кнопок
    update.callback_query.message.edit_text(new_message, reply_markup=reply_markup)


def _getmove(board):
    # сначала проверяем есть ли возможность сразу выйграть
    i = 0
    while (i < len(board)):
        if board[i] == '.':
            new_board = board[:]
            new_board[i] = "O"
            if (_i_won("O", new_board)):
                return i
        i += 1

    # теперь надо ли блокировать победу врага
    i = 0
    while (i < len(board)):
        if board[i] == '.':
            new_board = board[:]
            new_board[i] = "X"
            if (_i_won("X", new_board)):
                return i
        i += 1

    # теперь хардкод
    if board[4] == ".":
        return 4
    if board[2] == ".":
        return 2
    if board[6] == ".":
        return 6
    if board[8] == ".":
        return 8

    i = 0
    while (i < len(board)):
        if board[i] == '.':
            return i
        i += 1


def _i_won(mark, board):
    wins = [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6]
    for win in wins:
        if (board[win[0]] == mark and board[win[1]] == mark and board[win[2]] == mark):
            return True
    return False
