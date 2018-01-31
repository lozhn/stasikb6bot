import wolframalpha

def calculator(env):
    client = wolframalpha.Client(env['WOLFRAM_TOKEN'])

    def _calculator(bot, update):
        res = client.query(update.message.text)
        bot.send_message(chat_id=update.message.chat_id, text=next(res.results).text)
		
		# Using next loop, bot scratches all variants of solution, even writes out in words
        # for pod in res.pod:
        #     for sub in pod.subpod:
        #         answer = "{} : {}".format(sub["img"]["@src"], sub["img"]["@alt"])
        #         bot.send_message(chat_id=update.message.chat_id, text=answer)

    return calculator
