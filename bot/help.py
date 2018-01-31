
def help_cmd_factory(help_text):
    def _help_cmd(bot, update, args):
        update.message.reply_text(help_text)

    return _help_cmd
