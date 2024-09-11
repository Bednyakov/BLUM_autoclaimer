from time import sleep
from random import randint


from .query_functions import get_headers, get_passes, get_game_id, claim_flowers
from .loggers import logger



def run():
    headers = get_headers()
    passes = get_passes(headers=headers)
    for _ in range(passes):

        try:
            game_id = get_game_id(headers=headers)
            sleep(31)
            claim_flowers(game_id=game_id, headers=headers)
            sleep(randint(1,4))
        except Exception as e:
            logger.error(e)


