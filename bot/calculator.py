import wolframalpha

def calculator(bot, update):
    res = client.query(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=next(res.results).text)
    # for pod in res.pod:
    #     for sub in pod.subpod:
    #         answer = "{} : {}".format(sub["img"]["@src"], sub["img"]["@alt"])
    #         bot.send_message(chat_id=update.message.chat_id, text=answer)
