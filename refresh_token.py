import requests

url = 'https://user-domain.blum.codes/api/v1/auth/refresh'

refresh_token = "NjleHAiOjE3MjYxNzGFC0quGFGPRiyv..."


headers = {
            'Content-Type': 'application/json',
            'Sec-Ch-Ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Origin': 'https://telegram.blum.codes',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://telegram.blum.codes/',
            'Accept-Language': 'en-US,en;q=0.9',
            'Priority': 'u=1, i'
        }

payload = {"refresh":refresh_token}

def get_tokens(url: str, headers: dict, data: dict) -> dict | int:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result
    return response.status_code

if __name__ == "__main__":
    print(get_tokens(url, headers, payload))
    