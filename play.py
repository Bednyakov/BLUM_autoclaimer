import time
from telethon import TelegramClient
from fake_useragent import UserAgent
from core import get_token, daily_reward, refresh_token, hours_since, get_passes, play, claim, now, claim2


def autoplay() -> None:
    """
    Эмулирует работу с Telegram App BLUM.
    """

    API_ID = input("\nAPI ID: ")
    API_HASH = input("\nAPI Hash: ")
    if not (API_HASH or API_ID):
        return "Введены некорректные данные."
    SESSION_NAME = 'session_blum_autoplay'
    headers = {'User-Agent': UserAgent(os='android').random}

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH, lang_code="ru")
    try:

        token: dict = get_token(client=client, ref_token="dVebIvzKmr")
        access: str = token.get("access")
        refresh: str = token.get("refresh")
        headers.update({"Authorization": f"Bearer {access}"})
        headers.update({"Content-Type": "application/json"})
        timestamp = 0

        while True:

            if hours_since(timestamp=timestamp) > 3:
                timestamp = daily_reward(headers=headers)
                if not timestamp:
                    token = refresh_token(refresh=refresh, headers=headers)
                    access: str = token.get("access")
                    refresh: str = token.get("refresh")
                    headers.update({"Authorization": f"Bearer {access}"})
                    timestamp = daily_reward(headers=headers)

            passes = get_passes(headers=headers)
            if passes > 0:
                for _ in range(passes):
                    game_id = play(headers=headers)
                    time.sleep(31)
                    game_result = claim2(game_id=game_id, headers=headers)
                    if game_result != 200:
                        break

            time.sleep(3600 * 3)
            token = refresh_token(refresh=refresh, headers=headers)
            access: str = token.get("access")
            refresh: str = token.get("refresh")
            headers.update({"Authorization": f"Bearer {access}"})
            timestamp = daily_reward(headers=headers)
            game_result = claim2(game_id=game_id, headers=headers)

    except Exception as e:
        return {"error": f"Ошибка выполнения: {e}"}
    finally:
        client.disconnect()


if __name__ == "__main__":
    print(autoplay())
