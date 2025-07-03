import telebot # type: ignore
from config import config
from detection import take_screenshot, circle_color

#send screenshots
while True:
    img = take_screenshot()
    color = circle_color(img)