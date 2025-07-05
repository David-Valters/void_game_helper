from config import config
import telebot # type: ignore 
import pygame 
import pyautogui
import os

bot = telebot.TeleBot(config["TOKEN_BOT"])
pygame.mixer.init()

def wait_status():
    #музика  + зімна статусу + стікер + вставити таймер    
    print("Waiting...")
    bot.send_sticker(chat_id=config["chat_id"], sticker=config["wait_sticker_id"], message_thread_id=config.get("message_thread_id"))
    pygame.mixer.music.load("static/wait.mp3")
    pygame.mixer.music.play()

def starting_status():
    #музика + стікер
    print("Starting...")
    bot.send_sticker(chat_id=config["chat_id"], sticker=config["starting_sticker_id"], message_thread_id=config.get("message_thread_id"))
    pygame.mixer.music.load("static/starting.mp3")
    pygame.mixer.music.play()

def no_find_status():
    print("Не знайдено жовтий кружок.")
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("static/no_find.mp3")
        pygame.mixer.music.play()

def off_long_wait_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    print("Звук для long wait вимкнено.")
    config["play_long_wait_status"] = False  # Вимикаємо відтворення довгого очікування

def long_wait_status(playing: bool = True):
    if playing and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("static/long_time.mp3")
        pygame.mixer.music.play()

def start_round_status(img):
    bot.send_photo(chat_id=config["chat_id"], photo=img, message_thread_id=config.get("message_thread_id"))

def is_cursor_top_left() -> bool:
    x, y = pyautogui.position()
    if 'debug' in config:
        print(f"Координати курсора: ({x}, {y})")
    return x < 50 and y < 50

def create_screenshot_dir():
    os.makedirs("debug/no_find", exist_ok=True)