from telethon import TelegramClient
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from telethon.tl.functions.channels import JoinChannelRequest

# Настройки клиента
API_ID = '11111111111'        # Замените на ваш API ID
API_HASH = '1111111111111111111111'    # Замените на ваш API Hash
PHONE_NUMBER = '111111111111'  # Замените на ваш номер телефона
SESSION_NAME = 'session_blum_autoplay'       # Имя файла сессии
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


async def subscribe_to_channel(client: TelegramClient, channel_username: str) -> str:
    """
    Подписывается на указанный канал Telegram, создавая сессию при необходимости.

    :param channel_username: Имя пользователя (или ссылка) канала, на который нужно подписаться.
    :return: Сообщение об успехе или ошибке.
    """
    try:
        print("Проверка или создание сессии...")
        await client.start(phone=PHONE_NUMBER)
        
        if await client.is_user_authorized() is False:
            print("Требуется двухфакторная аутентификация.")
            try:
                password = input("Введите пароль двухфакторной аутентификации: ")
                await client.sign_in(password=password)
            except SessionPasswordNeededError as e:
                return f"Ошибка двухфакторной аутентификации: {e}"
        
        await client(JoinChannelRequest(channel_username))
        return f"Успешно подписались на канал {channel_username}."
    except Exception as e:
        return f"Ошибка подписки на канал {channel_username}: {e}"
    finally:
        await client.disconnect()

async def main():
    channel_username = "@itpolice"
    result = await subscribe_to_channel(client, channel_username)
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
