import json
import os

import requests
from dotenv import load_dotenv

load_dotenv("utils/config/.env")
GPT_ENDPOINT = os.getenv("GPT_ENDPOINT")
API_KEY = os.getenv("OPEN_AI_API_KEY")


class GptClient:
    def __init__(self, target: str = "main"):
        pass

    def request(self, message: str) -> str:
        return self._send(message)

    def request_json(self, message: str) -> dict | list:
        result = self._send(message, is_json=True)
        return json.loads(result)

    def _send(self, message, is_json: bool = False) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        data = {
            "model": "gpt-4-turbo",
            "messages": [{"role": "system", "content": message}],
            "temperature": 1,
            "max_tokens": 500,
        }
        if is_json:
            data["response_format"] = {"type": "json_object"}
        try:
            response = requests.post(GPT_ENDPOINT, headers=headers, json=data)
            return response.json()["choices"][0]["message"]["content"]
        except Exception as error:
            print(f"{error=}")
