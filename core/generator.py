from typing import Dict, Any
from dataclasses import dataclass
import hashlib
import json

GameId = str
PayloadType = str

@dataclass
class Clicks:
    clicks: int

@dataclass
class ChallengeType:
    nonce: int
    hash: str
    id: str

@dataclass
class AmountType:
    amount: int

def generate_hash(input_data: str) -> str:
    """Generate a SHA-256 hash of the input data."""
    return hashlib.sha256(input_data.encode()).hexdigest()

class PayloadGenerator:
    def __init__(self, game_id: GameId, challenge: ChallengeType):
        self.game_id = game_id
        self.challenge = challenge

    def create_payload(self, clicks: Dict[str, Clicks], earned_points: Dict[str, AmountType]) -> Dict[str, Any]:
        """Create a payload based on the game data."""
        payload = {
            "gameId": self.game_id,
            "challenge": {
                "nonce": self.challenge.nonce,
                "hash": self.challenge.hash,
                "id": self.challenge.id
            },
            "assets": {key: {"clicks": value.clicks} for key, value in clicks.items()},
            "earnedPoints": {key: {"amount": value.amount} for key, value in earned_points.items()}
        }

        payload_string = json.dumps(payload, sort_keys=True)
        payload["payloadHash"] = generate_hash(payload_string)

        return payload


def main():
    game_id = "f0a60dd9-d0d1-4810-84d6-fc163dc740a0"
    challenge = ChallengeType(nonce=12345, hash="example_hash", id="challenge_001")

    clicks = {
        "asset_1": Clicks(clicks=10),
        "asset_2": Clicks(clicks=20)
    }

    earned_points = {
        "player_1": AmountType(amount=150),
        "player_2": AmountType(amount=200)
    }

    generator = PayloadGenerator(game_id, challenge)
    payload = generator.create_payload(clicks, earned_points)

    print(json.dumps(payload, indent=4))
    print(generator)

if __name__ == "__main__":
    main()
