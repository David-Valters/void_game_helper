import telebot # type: ignore
from config import config
from detection import *
from action import *
#send screenshots
# while True:

img = Image.open("static/s/20250703_23-47-49_start_round.png")
# img.show()
st = match_template(img, [start_round_template])
print(st)