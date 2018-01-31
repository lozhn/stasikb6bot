def start_cmd(bot, update, args):
    update.message.reply_text(f'Hi {update.message.from_user.first_name}')