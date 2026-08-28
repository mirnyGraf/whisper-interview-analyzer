from __future__ import annotations

import os

import httpx


class GroqClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        timeout: float = 120,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        self.client.close()

    def chat(self, system: str, user: str) -> str:
        response = self.client.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": system,
                    },
                    {
                        "role": "user",
                        "content": user,
                    },
                ],
                "temperature": 0,
            },
        )

        # Комментарии: если Groq вернёт 401, 429, 5xx и т.д.,
        # Комментарии: здесь получим понятное HTTP-исключение.
        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]


def create_groq_client_from_env() -> GroqClient:
    api_key = os.environ["GROQ_API_KEY"]
    base_url = os.environ.get(
        "GROQ_BASE_URL",
        "https://api.groq.com/openai/v1",
    )
    model = os.environ.get(
        "GROQ_MODEL",
        "openai/gpt-oss-120b",
    )

    return GroqClient(
        api_key=api_key,
        base_url=base_url,
        model=model,
    )
