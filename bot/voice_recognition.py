import os
import uuid
import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment

API_KEY = '89665de6-d76c-40ba-ac6b-a13b52bf32f1'
UUID = str(uuid.uuid4()).replace("-", "")


def voice_cmd(bot, update):
    file_id = update.message.voice.file_id
    file_name = f"{file_id}.oga"
    export_file_name = f"{file_id}.wav"
    bot.get_file(file_id).download(file_name)
    voice = AudioSegment.from_ogg(file_name)
    voice.export(export_file_name, format="wav")
    result = recognize(export_file_name, UUID)
    update.message.reply_text(result)
    os.remove(file_name)
    os.remove(export_file_name)


def recognize(voice, uid):
    languages = ['ru-RU', 'en-US']
    result = dict()
    data = open(voice, "rb").read()
    for lang in languages:
        url = f"https://asr.yandex.net/asr_xml?uuid={uid}&key={API_KEY}&topic=queries&lang={lang}&disableAntimat=true"
        headers = {'Content-Type': 'audio/x-wav',
                   'Content-Length': str(len(data))}
        resp = requests.post(url, data=data, headers=headers)
        dom = BeautifulSoup(resp.text, 'lxml')
        res = dict((var.string, float(var['confidence']))
                   for var
                   in dom.html.body.recognitionresults.findAll("variant"))
        result.update(res)

    phrase = max(result, key=(lambda key: result[key]))
    return phrase
