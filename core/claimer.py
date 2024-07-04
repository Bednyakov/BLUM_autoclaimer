import time
import requests
from random import randint
from core.loggers import logger


class BlumClaimer():

    def __init__(self, headers: dict):
        self.headers = headers

    def me_request(self) -> None:
        url = "https://gateway.blum.codes/v1/user/me"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:
                data = response.json()
                id = data["id"]["id"]
                username = data["username"]
                logger.info(f"Id: {id}, username: {username}")
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")
        else:
            logger.error(f"Ошибка me_request: {response.text}")

    def now_request(self) -> None:
        url = "https://game-domain.blum.codes/api/v1/time/now"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return None
        logger.error(f"Ошибка now_request: {response.status_code}")

    def balance_request(self) -> int:
        url = "https://game-domain.blum.codes/api/v1/user/balance"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:
                data = response.json()
                # balance = data["availableBalance"]
                # passes = data["playPasses"]
                # logger.info(f"Balance: {balance}, Play passes: {passes}")
                return data["playPasses"]
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")
        logger.error(f"Ошибка balance_request: {response.status_code}")

    def play_request(self) -> str:
        url = "https://game-domain.blum.codes/api/v1/game/play"

        response = requests.post(url, headers=self.headers)
        self.balance_request()

        if response.status_code == 200:
            try:
                data = response.json()
                return data["gameId"]
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")
        logger.error(f"Ошибка play_request: {response.status_code}")

    def claim_request(self, id: str) -> None:
        url = "https://game-domain.blum.codes/api/v1/game/claim"
        game_id = id
        points = randint(189, 207)
        payload = {"gameId": game_id, "points": points}

        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 200:
            logger.info(f"За игру получено {points} очков.")
            return None
        logger.error(f"Ошибка claim_request: {response.status_code}")

    def play(self):
        id = self.play_request()
        logger.info(f"Началась игра {id}")
        time.sleep(34)
        self.claim_request(id)

        
        
        






