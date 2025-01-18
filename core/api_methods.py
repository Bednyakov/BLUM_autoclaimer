from telethon.sync import TelegramClient, functions
from telethon.tl.functions.channels import JoinChannelRequest
from urllib.parse import unquote
import random
import json
import requests
import time

from core.gen import generate_challenge, encrypt_payload


def now(headers: dict) -> int:
    url = "https://game-domain.blum.codes/api/v1/time/now"
    response = requests.get(url=url, headers=headers)
    return response.status_code
    

def daily_reward(headers: dict) -> int | None:
    url = "https://game-domain.blum.codes/api/v2/daily-reward"

    for _ in range(5):
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            claim = data.get("claim")
            if claim == "available":
                for _ in range(5):
                    response = requests.post(url=url, headers=headers)
                    if response.status_code == 200:
                        print("Выполнено ежедневное задание.")
                        return int(time.time())
                    time.sleep(2)
            return int(time.time())
        time.sleep(2)
    return


def get_passes(headers: dict) -> int:
    url = "https://game-domain.blum.codes/api/v1/user/balance"
    
    for _ in range(5):
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            passes: int = data.get("playPasses", 0)
            print(f"Осталось {passes} билетов.")
            return passes
    return 0
        

def play(headers: dict) -> str:
    url = "https://game-domain.blum.codes/api/v2/game/play"

    for _ in range(5):
        response = requests.post(url=url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f'\nНачалась игра {result.get("gameId")}.')
            return result.get("gameId")
        

def get_payload(game_id: str):
        points = random.randint(200, 203)
        json_data = {"gameId": game_id, "points": points}
        asset_clicks = {
            "BOMB": {"clicks": 0},
            "CLOVER": {"clicks": points},
            "FREEZE": {"clicks": 0},
            "HARRIS": {"clicks": 0},
            "TRUMP": {"clicks": 0}
        }
        earned_points = {"BP": {"amount": points * 5}}
        pay={"gameId": game_id, "earnedPoints": earned_points, "assetClicks": asset_clicks}
        response = requests.post('http://62.60.246.140:9876/getPayload', json=pay)
        data = response.json()
        payload = data.get("payload")
        return {"payload": payload}
        

def claim(game_id: str, headers: dict) -> int:
    url = "https://game-domain.blum.codes/api/v2/game/claim"
    try:
        
        payload = get_payload(game_id)
        print(payload)

        for _ in range(5):
            response = requests.post(url=url, headers=headers, json=payload)
            if response.status_code == 200:
                print(f"{game_id}: {response.status_code}.")
                return 200
            return response.status_code
    except Exception as e:
        print(e)


def claim2(game_id: str, headers: dict) -> int:
    url = "https://game-domain.blum.codes/api/v2/game/claim"
    try:
        points = random.randint(200, 203)
        challenge = generate_challenge(game_id=game_id)

        game_data = {
        "version": 1.2,
        "gameId": "",
        "challenge": {
            "nonce": 0,
            "hash": "",
        },
        "earnedPoints": {"BP": {"amount": 100}},
        "assetClicks": {
            "BOMB": {"clicks": 0},
            "CLOVER": {"clicks": 100},
            "FREEZE": {
                "clicks": 2
            },
        },
        "isNode": False,
    }
        game_data["gameId"] = game_id
        game_data["challenge"]["nonce"] = challenge["nonce"]
        game_data["challenge"]["hash"] = challenge["hash"]
        game_data["earnedPoints"]["BP"]["amount"] = points
        game_data["assetClicks"]["CLOVER"]["clicks"] = points
        game_data["assetClicks"]["FREEZE"]["clicks"] = 0

        encrypted_payload = encrypt_payload(json.dumps(game_data, separators=(",", ":")))
        payload = {"payload": encrypted_payload}

        for _ in range(5):
            response = requests.post(url=url, headers=headers, json=payload)
            if response.status_code == 200:
                print(f"\n{game_id}. Status: {response.status_code}.")
                return 200
            print(f"\n{game_id}. Status: {response.status_code}.")
            return response.status_code
    except Exception as e:
        print(e)


def refresh_token(refresh: str, headers: dict) -> dict:
    new_headers = headers.copy()
    new_headers.pop("Authorization")
    url = "https://user-domain.blum.codes/api/v1/auth/refresh"
    payload = {"refresh": refresh}

    for _ in range(5):
        response = requests.post(url=url, headers=new_headers, json=payload)
        if response.status_code == 200:
            return response.json()
     

def hours_since(timestamp: int) -> int:
    current_time = time.time()
    time_difference = current_time - timestamp
    hours_passed = time_difference // 3600
    return int(hours_passed)


def get_token(client: TelegramClient, ref_token: str) -> dict:

    with client:

        telegram_object = client.get_entity("BlumCryptoBot")
        client(JoinChannelRequest("@itpolice"))
        webview = client(functions.messages.RequestWebViewRequest(telegram_object, telegram_object, platform="android", url="https://telegram.blum.codes/"))
        webview_url = webview.url

        data = unquote(webview_url.split('tgWebAppData=')[1].split('&')[0])

        json_data = {"query": data, "referralToken": ref_token}

        while True:
                response = requests.post("https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data)

                if response.status_code == 520:
                    time.sleep(5)
                    continue
                else:
                    break

        result = response.json()
        token = result.get("token")
        return token

