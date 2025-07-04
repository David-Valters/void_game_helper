
from operator import is_
from config import config 
from detection import take_screenshot, circle_color, start_round
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
                
                elif color == "G":
                    status = "G"
                    starting_status()
                    break
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
                    status = "L"
        time.sleep(1)        
    while True:
        screenshot = take_screenshot()
        if start_round(screenshot):
            print("Раунд почався!")
            start_round_status(screenshot)
            break
        time.sleep(0.3)

if __name__ == "__main__":
    print("Запуск програми...")
    if 'debug' in config:
        print("Режим налагодження увімкнено.")
    while True:
        #KeyboardInterrupt
        try:
            main()
        except KeyboardInterrupt:
            print("\nПрограма зупинена користувачем.")

        input("Натисніть Enter, щоб перезапустити...")  # Додано для зручності