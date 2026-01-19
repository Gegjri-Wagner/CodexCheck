#!/usr/bin/env python3
import os
import time
import requests

API_BASE = "https://api.telegram.org/bot{token}/{method}"
MESSAGE = "Угроза БПЛА для города Чебоксар."


def api_call(token: str, method: str, payload: dict | None = None) -> dict:
    url = API_BASE.format(token=token, method=method)
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def send_message(token: str, chat_id: int) -> None:
    api_call(
        token,
        "sendMessage",
        {"chat_id": chat_id, "text": MESSAGE},
    )


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set")

    offset = None
    while True:
        payload = {"timeout": 30}
        if offset is not None:
            payload["offset"] = offset

        result = api_call(token, "getUpdates", payload)
        for update in result.get("result", []):
            offset = update["update_id"] + 1
            message = update.get("message") or {}
            chat = message.get("chat") or {}
            chat_id = chat.get("id")
            if chat_id is not None:
                send_message(token, chat_id)

        time.sleep(1)


if __name__ == "__main__":
    main()
