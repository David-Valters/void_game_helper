
from config import config 
from detection import take_screenshot, circle_color, start_round, flush_input
from action import *
import time

def main():
    status = None

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
                    wait_status()
                continue
            # time.sleep(0.4)
        else:
            if not color:
                if status == "L":
                    status = None
                    continue
                if status == "N":

                    no_find_status()
                status = "N"
                # time.sleep(1)

            elif color == "G":
                starting_status()
                status = "G"
                break

            elif color == "Y":                
                #якщо пройшло більше 3 минут
                if start_wait_time is None:
                    start_wait_time = time.time()
                elif time.time() - start_wait_time > 180:
                    if is_cursor_top_left():
                        off_long_wait_music()
                    long_wait_status(config.get("play_long_wait_status", True))
                    screenshot.save(f"debug/no_find/{time.strftime('%Y%m%d%H%M%S')}_({color}).png")
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
    while True:
        #KeyboardInterrupt
        try:
            main()
        except KeyboardInterrupt:
            config["play_long_wait_status"] = True  # type: ignore # Повертаємо відтворення довгого очікування
            print("\nПрограма зупинена користувачем.")
        flush_input()
        input("Натисніть Enter, щоб перезапустити...")  # Додано для зручності