from yandex import Translater


def translate_cmd_factory(translate_api_key):
    translator = Translater()
    api_key = translate_api_key

    def translate(bot, update, args):
        query = " ".join(args)
        translator.set_key(api_key)
        translator.set_from_lang('ru')
        translator.set_to_lang('en')
        translator.set_text(query)
        result = translator.translate()
        update.message.reply_text(result)

    return translate
