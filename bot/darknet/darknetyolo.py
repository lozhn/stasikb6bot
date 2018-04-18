import sys, os

# put here path to darknet/python/ folder
sys.path.append(os.path.join(os.getcwd(), 'bot/darknet/python/'))
sys.path.append("../bot")

from darknet import *
import cv2
from random import randint

prefix = os.path.join(os.getcwd(), 'bot/darknet/')
_config = f"{prefix}/cfg/yolov3.cfg"
_weights = f"{prefix}/yolov3.weights"

net = load_net(_config), _weights, 0))
meta = load_meta(x(prefix + "cfg/coco.data"))


def detect_object_cmd(bot, update):

    file_id = update.message.photo[3].file_id
    photoFile = bot.get_file(file_id)
    file_name = f"{file_id}.jpg"
    image = bot.get_file(file_id).download(file_name)

    imagepath = os.path.join(os.getcwd(), image)

    bb = detect(net, meta, imagepath.encode('UTF-8'))
    
    img = cv2.cvtColor(cv2.imread(imagepath), cv2.COLOR_BGR2RGB)

    for count, value in enumerate(bb):
        name, confidence, bbox = value

        x, y, w, h  = map(int, bbox)

        pt1 = (int(x - w/2), int(y - h/2))
        pt2 = (int(x + w/2), int(y + h/2))
        cv2.rectangle(img, pt1, pt2, (randint(0, 255), randint(0, 255), randint(0, 255)), 2)
        cv2.putText(img, name.decode("UTF-8") , pt1, cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, '{:0.5f}'.format(confidence) , (int(x - w/2 + 20), int(y - h/2 + 20)) , cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)



    cv2.imwrite('/home/katerina/Documents/git/stasikb6bot/temp.png',  cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    update.message.reply_photo(open('/home/katerina/Documents/git/stasikb6bot/temp.png', 'rb'))
