import os
from dotenv import load_dotenv


load_dotenv()


token: str = os.getenv('TOKEN', 'default_token_if_not_set')

headers: dict = {
    "Origin": "https://telegram.blum.codes",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-G975F Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.133 Mobile Safari/537.36',
    'Content-Type': 'application/json',
    "Authorization": f"Bearer {token}",
    "X-Requested-With": "org.telegram.messenger",
}