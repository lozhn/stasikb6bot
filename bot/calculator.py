import wolframalpha

def calculator_cmd_factory(wolfram_token):
    client = wolframalpha.Client(wolfram_token)

    def _calculator_cmd(bot, update, args):
        expr = " ".join(args)
        res = client.query(expr)
        update.message.reply_text(next(res.results).text)
        # for pod in res.pod:
        #     for sub in pod.subpod:
        #         answer = "{} : {}".format(sub["img"]["@src"], sub["img"]["@alt"])
        #         bot.send_message(chat_id=update.message.chat_id, text=answer)

    return _calculator_cmd
