
from calendar import c
from config import config 
from detection import take_screenshot, circle_color, start_round, flush_input
from action import *
import time

def main():
    status = None
    last_trigger = 0
    while True:
        screenshot = take_screenshot()
        color = circle_color(screenshot)
        is_circle = color in ["Y", "G"]

        if not status: #не ініціалізовано (не було знайдено жовтйи кружок ні разу)
            print("Ініціалізація...")
            if is_circle:
                if color == "Y":
                    status = "Y"
                    start_wait_time = time.time()
                    if not config["settings"].get("play_long_wait", False):
                        config["settings"]["play_long_wait"] = True
                        print("Увімкнено відтворення звуку довгого очікування")
                    wait_status()
                continue
            # time.sleep(0.4)
        else:
            if not color:
                if time.time() - last_trigger > 2.5:
                    print("Не знайдено жовтий кружок, очікування...")
                    last_trigger = time.time()
                    time.sleep(0.4)
                    continue

                screenshot.save(f"debug/no_find/{time.strftime('%Y-%m-%d_%H-%M-%S')}_(wait).png")
                no_find_status()
                if status == "L":
                    status = None
                    continue
                
                status = "N"
                # time.sleep(1)

            elif color == "G":
                starting_status(screenshot)
                status = "G"
                break

            elif color == "Y":              
                #якщо пройшло більше 3 минут
                if start_wait_time is None:
                    start_wait_time = time.time()
                elif time.time() - start_wait_time > 180:
                    if config["settings"].get("play_long_wait", True):
                        config["settings"]["play_long_wait"] = False # Вимикаємо відтворення довгого очікування
                        long_wait_status()
                    status = "L"
        time.sleep(1)        
    while True:
        screenshot = take_screenshot()
        if start_round(screenshot):
            print("Раунд почався!")
            start_round_status(screenshot)
            break
        time.sleep(0.2)

if __name__ == "__main__":
    print("Запуск програми...")
    create_screenshot_dir()
    if 'debug' in config:
        print("Режим налагодження увімкнено.")
    if 'NO_SEND' in config:
        print("Відправка повідомлень вимкнена.")
    while True:
        #KeyboardInterrupt
        try:
            config["settings"] = {}  # Скидаємо налаштування перед кожним запуском
            main()
        except KeyboardInterrupt:
            config["play_long_wait_status"] = True  # type: ignore # Повертаємо відтворення довгого очікування
            print("\nПрограма зупинена користувачем.")
        flush_input()
        input("Натисніть Enter, щоб перезапустити...")  # Додано для зручності