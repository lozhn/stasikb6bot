def quit_cmd_factory(updater):
    def _quit(bot, update):
        update.message.reply_text("Shutting down")
        updater.stop()
        updater.running = False
        exit_msg = f"Shutting down because of {update.message.from_user.name}"
        print(exit_msg)
    return _quit