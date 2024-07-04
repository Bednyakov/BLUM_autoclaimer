import time
import threading
from core.config import headers
from core.loggers import logger
from core.claimer import BlumClaimer

play = BlumClaimer(headers)
stop_event = threading.Event()

def now() -> None:
    while not stop_event.is_set():
        play.now_request()
        time.sleep(121)

def balance() -> None:
    while not stop_event.is_set():
        play.balance_request()
        time.sleep(31)

def game(count: int) -> None:
    passes = count
    while passes > 0:
        play.play()
        passes -= 1
    stop_all_threads()

def stop_all_threads():
    logger.info("Билеты кончились.")
    stop_event.set()

def run():
    play.me_request()
    play.now_request()
    count = play.balance_request()
    logger.info(f"Всего билетов: {count}")
    time.sleep(3)
    play.me_request()

    thread_one = threading.Thread(target=now)
    thread_two = threading.Thread(target=balance)
    thread_three = threading.Thread(target=game, args=(count,))

    thread_one.start()
    thread_two.start()
    thread_three.start()

    thread_one.join()
    thread_two.join()
    thread_three.join()