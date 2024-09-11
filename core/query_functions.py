import requests
from random import randint
from sys import exit as exit_the_program

from .loggers import logger



def balance_request(headers: dict) -> int:
        url = "https://game-domain.blum.codes/api/v1/user/balance"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                return data["playPasses"]
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")
        logger.error(f"Ошибка balance_request: {response.status_code}")
        exit_the_program()


def get_game_id(headers: dict) -> str:
    url = "https://game-domain.blum.codes/api/v1/game/play"
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
            try:
                data = response.json()
                return data["gameId"]
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")
    logger.error(f"Ошибка play_request: {response.status_code}")
    exit_the_program()


def claim_flowers(game_id: str, headers: dict) -> None:
    url = "https://game-domain.blum.codes/api/v1/game/claim"
    points = randint(189, 207)
    payload = {"gameId": game_id, "points": points}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        logger.info(f"За игру получено {points} очков.")
        return None
    logger.error(f"Ошибка claim_request: {response.status_code}")
    exit_the_program()


def get_passes(headers: dict) -> int:
    amount = input("\nВведите количество билетов или 'all' если играем на все: ")
    if amount == 'all':
        return balance_request(headers)

    return int(amount)

def get_token() -> str:
     token = input("\nВведите токен авторизации (без Bearer): ")
     return token

def get_headers() -> dict:
     token = get_token()
     headers: dict = {
    "Origin": "https://telegram.blum.codes",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-G975F Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.133 Mobile Safari/537.36',
    'Content-Type': 'application/json',
    "Authorization": f"Bearer {token}",
    "X-Requested-With": "org.telegram.messenger",
}
     return headers