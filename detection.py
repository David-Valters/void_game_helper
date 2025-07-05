import subprocess
import os
import sys
import time
import pyautogui
import cv2
import numpy as np
from PIL import Image

from config import config

def take_screenshot()-> Image.Image:
    if sys.platform == 'linux':
        filepath="/tmp/screenshot.png"
        # Запускаємо spectacle
        subprocess.run(["spectacle", "-n", "-b", "-o", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)        
        # Чекаємо поки файл з'явиться
        for _ in range(10):
            if os.path.exists(filepath):
                return Image.open(filepath)
            time.sleep(0.2)
        raise FileNotFoundError("Не вдалося зробити скріншот.")
    else:
        return pyautogui.screenshot()

yellow_circle_template = cv2.imread('static/yellow_circle.png', cv2.IMREAD_COLOR)
green_circle_template = cv2.imread('static/green_circle.png', cv2.IMREAD_COLOR)
start_round_template = cv2.imread('static/start_round_v3.png', cv2.IMREAD_COLOR)

def img_show(img_path):
    Image.open(img_path).show()

def match_template(img, template:list, min_val=0.8)-> list[float]:
    screenshot = np.array(img)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    results = []
    for tmpl in template:
        res = cv2.matchTemplate(screenshot, tmpl, cv2.TM_CCOEFF_NORMED)
        _, val, _, max_loc = cv2.minMaxLoc(res)
        results.append(val)
        if 'debug' in config:
            if val > min_val:
                print(f"Знайдено шаблон з ймовірністю {val:.2f}")
                template_h, template_w = tmpl.shape[:2]
                top_left = max_loc
                bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
                cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
                # cv2.imshow("Matched Result", screenshot)
                fn=f'static/f/{time.strftime('%Y-%m-%d_%H-%M-%S')}_({val:.3f}).png'
                cv2.imwrite(fn, screenshot)
                # img_show(fn)

                

    if 'debug' in config:
        print(f"Результати збігу шаблонів: {results}")
    return results
        

def circle_color(img):
    w, h = img.size
    cropped = img.crop((0, 0, w // 1.8, h // 2))
    yellow, green = match_template(cropped, [yellow_circle_template, green_circle_template])
    if yellow > 0.8:
        return "Y"
    elif green > 0.8:
        return "G"
    else:
        return None

def start_round(img):
    start_round = match_template(img, [start_round_template], min_val=0.6)
    if start_round[0] > 0.8:
        return True
    if 'debug' in config:
        #save image
        fn = f'static/s/{time.strftime('%Y-%m-%d_%H-%M-%S')}_({start_round[0]:.3f})_start_round.png'
        img.save(fn)
    return False

def flush_input():
    if os.name == 'nt':  # Windows
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:  # Unix/Linux/Mac
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)