import hashlib
import time
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
import base64
import json


def generate_challenge(game_id: str, difficulty: int = 4) -> dict:
    """
    Generates a challenge by finding a hash that starts with a specified number of zeros.

    Args:
    game_id (str): The ID of the game.
    difficulty (int): The number of zeros the hash should start with. Defaults to 4.

    Returns:
    dict: A dictionary containing the nonce, hash, iterations, and time taken.
    """
    nonce = 0
    target = "0" * difficulty
    start_time = time.time()

    while True:
        data = game_id + str(nonce)

        hash_object = hashlib.sha256(data.encode())
        hash_hex = hash_object.hexdigest()

        if hash_hex.startswith(target):
            break

        nonce += 1

    time_taken = time.time() - start_time
    return {
        "nonce": nonce,
        "hash": hash_hex,
        "iterations": nonce + 1,  
        "time_taken": time_taken,
    }



def encrypt_payload(payload: str) -> str | None:
    """
    Encrypt a given payload using an RSA public key.
    :param payload: The payload to encrypt (as a string).
    :return: The encrypted payload as a base64 string, or None in case of an error.
    """
    try:
        load_public_key = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQ0lqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FnOEFNSUlDQ2dLQ0FnRUF6NXM0cnRzZkxiRmxoZnRoNFJ1OQpZZFdzaU45eVpJc2RtdUE4U2lOaTIrU1pSZlplQVRIMUh2ZVc5OUQyc3JxbkloOFVpUlR4dEpiWFdGSDFCTEQ2CkUvZ09RdjBMdy9Ld1VHZWhScjc3Zm5PT05QbkJBTnF3dEppOFRvWDZDL2hFeW9JMFlFaU5JUzdiY21JczVVNmkKRm9heTF0UFlmRzFkSEJXVGxxU2NidG5lSUthTTJxL3JtRXlQaHlRcDhTcHlTc0x5WTE1WGxERGM4SE5zNVhMNQpNU2hZTllQRWUrVG9hTTNsMDRMSDR6UmRxTEJLZ0ZJMFpqRWxVWlh0T24vTS81em1WamFwd1Q2Ymk0cldOTnZKCmM3TTdabkQ5RXJGWFFxemRLR0x0cHA4Q1hPdXZnUncxRGdPdFpITWwxRzVzY0p1TFZmYjJYRnBKaFNHUmYyQkkKMFFxbmhJc1VWNW03M1JWWE9Ma214dzZOcWpsbnI0TmNpR3F4MzMzWjFSa2o0U09odHJCbitiVXg3SzFIUVNveApDWVgycmlsRlFsdWdDNXd4NmxVU0lRRlQvU010anQ0S20remszYWFiQjlPQUQvWjgzOWVqVzM5MEpLbzA3MVg3CnVITkNhM2dIMjUvV2Rzc0Yra0NybDR3ZmhlUUhUcDhwck9qTjMrTXNNUTRBdzNBOFBvR1ZYdytMK3E1dmVuK0IKcndqanJyYmQzZ0pGMzdkYURydjRrWEFycGNFdHkxNVV4TTB0YzZZUXV5TzR3UDVwTG9BSmNOTFNtc1VGNzBOMwp4a3dqT05BYlByWURqc0x5c1dpUmRUWCsxaGx4NndqL2xWRVNmVjV2U0RvTytENmZUTjd2ZXRqZE5MSWRFeG9hClRmTzBkNzUrc2NGdGdtellvM2NxK1pNQ0F3RUFBUT09Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ=="
        public_key_bytes = base64.b64decode(load_public_key)
        public_key = serialization.load_pem_public_key(public_key_bytes)

        payload_bytes = payload.encode("utf-8")

        encrypted_payload = public_key.encrypt(
            payload_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=SHA256()),
                algorithm=SHA256(),
                label=None,
            ),
        )

        return base64.b64encode(encrypted_payload).decode("utf-8")

    except Exception as e:
        print(f"Error encrypting payload: {e}")
        return None
    

if __name__ == "__main__":
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

    game_id = "abcd-efghi-jklmno-292ddhdjh"
    points = 169

    challenge = generate_challenge(game_id=game_id)
    game_data["gameId"] = game_id
    game_data["challenge"]["nonce"] = challenge["nonce"]
    game_data["challenge"]["hash"] = challenge["hash"]
    game_data["earnedPoints"]["BP"]["amount"] = points
    game_data["assetClicks"]["CLOVER"]["clicks"] = points
    game_data["assetClicks"]["FREEZE"]["clicks"] = 2

    encrypted_payload = encrypt_payload(json.dumps(game_data, separators=(",", ":")))

    print(encrypted_payload)