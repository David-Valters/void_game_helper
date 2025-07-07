import time
from config import config
import telebot # type: ignore 
import pygame 
import pyautogui
import os

from detection import get_wait_time_window

if not 'NO_SEND' in config:
    bot = telebot.TeleBot(config["TOKEN_BOT"])
pygame.mixer.init()

def wait_status():
    #музика  + зімна статусу + стікер + вставити таймер    
    print("Waiting...")
    if not 'NO_SEND' in config:
        bot.send_sticker(chat_id=config["chat_id"], sticker=config["wait_sticker_id"], message_thread_id=config.get("message_thread_id"))
    pygame.mixer.music.load("static/wait.mp3")
    pygame.mixer.music.play()

def starting_status(img):
    #музика + стікер
    print("Starting...")
    pygame.mixer.music.load("static/starting.mp3")
    pygame.mixer.music.play()
    if not 'NO_SEND' in config:
        img = get_wait_time_window(img)
        if img:
            bot.send_photo(chat_id=config["chat_id"], photo=img, message_thread_id=config.get("message_thread_id"))
        else:
            bot.send_sticker(chat_id=config["chat_id"], sticker=config["starting_sticker_id"], message_thread_id=config.get("message_thread_id"))
            print("Не знайдено вікно очікування.")
            img.save(f"debug/no_find/{time.strftime('%Y-%m-%d_%H-%M-%S')}_(wait_time).png")

def no_find_status():
    print("Втрачено жовтий кружок.")
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("static/no_find.mp3")
        pygame.mixer.music.play()

def off_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def long_wait_status(playing: bool = True):
    if playing and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("static/long_time.mp3")
        pygame.mixer.music.play()

def start_round_status(img):
    if not 'NO_SEND' in config:
        bot.send_photo(chat_id=config["chat_id"], photo=img, message_thread_id=config.get("message_thread_id"))

def is_cursor_top_left() -> bool:
    x, y = pyautogui.position()
    if 'debug' in config:
        print(f"Координати курсора: ({x}, {y})")
    return x < 50 and y < 50

def create_screenshot_dir():
    os.makedirs("debug/no_find", exist_ok=True)
    os.makedirs("debug/f", exist_ok=True)
    os.makedirs("debug/s", exist_ok=True)