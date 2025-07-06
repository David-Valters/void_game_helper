from math import e
import telebot # type: ignore
from config import config
from detection import *
from action import *
#send screenshots
# while True:

# img = Image.open("/home/duck/Desktop/image.webp")
img = Image.open("/home/duck/Desktop/i2.png")
# img.show()
i = get_wait_time_window(img)
if i:
    i.show()
else:
    print("No start round window found")