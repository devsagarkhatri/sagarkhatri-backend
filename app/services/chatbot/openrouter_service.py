
import os

import httpx
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")


class OpenRouterServiceError(Exception):
    """A safe, user-independent error from the AI provider service."""


async def create_chat_completion(
    messages: list[dict],
    tools: list[dict] | None = None,
) -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise OpenRouterServiceError(
            "OpenRouter API key is not configured."
        )

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.3,
    }

    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-OpenRouter-Title": "Sagar Khatri Portfolio",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload,
            )

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            raise OpenRouterServiceError(
                "The AI service returned an invalid response."
            )

        choices = data.get("choices")

        if not isinstance(choices, list) or not choices:
            raise OpenRouterServiceError(
                "The AI service returned no response."
            )

        first_choice = choices[0]

        if not isinstance(first_choice, dict):
            raise OpenRouterServiceError(
                "The AI service returned an invalid response."
            )

        message = first_choice.get("message")

        if not isinstance(message, dict):
            raise OpenRouterServiceError(
                "The AI service returned an invalid response."
            )

        content = message.get("content")
        tool_calls = message.get("tool_calls")

        if content is not None and not isinstance(content, str):
            raise OpenRouterServiceError(
                "The AI service returned an invalid response."
            )

        if tool_calls is not None and not isinstance(tool_calls, list):
            raise OpenRouterServiceError(
                "The AI service returned invalid tool requests."
            )

        if not content and not tool_calls:
            raise OpenRouterServiceError(
                "The AI service returned an empty response."
            )

        return message

    except OpenRouterServiceError:
        raise
    except (httpx.HTTPError, ValueError, TypeError, KeyError) as exc:
        # Do not expose provider errors, response bodies, or credentials.
        raise OpenRouterServiceError(
            "The AI service is temporarily unavailable."
        ) from exc
