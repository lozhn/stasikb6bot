import wolframalpha

def calculator_cmd_factory(wolfram_token):
    client = wolframalpha.Client(wolfram_token)

    def _calculator_cmd(bot, update, args):
        expr = " ".join(args)
        res = client.query(expr)
        # Using next loop, bot scratches all variants of solution, even writes out in words
        # for pod in res.pod:
        #     for sub in pod.subpod:
        #         answer = "{} : {}".format(sub["img"]["@src"], sub["img"]["@alt"])
        #         bot.send_message(chat_id=update.message.chat_id, text=answer)
        update.message.reply_text(f"{expr} \n > {next(res.results).text}")

    return _calculator_cmd

