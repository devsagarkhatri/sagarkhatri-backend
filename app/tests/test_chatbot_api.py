
import unittest
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException

from app.api.v1.chatbot import chat
from app.schemas.chatbot.chat import ChatRequest
from app.services.chatbot.chatbot_cache import (
    clear_chatbot_cache,
    get_cached_answer,
)
from app.services.chatbot.openrouter_service import OpenRouterServiceError
from app.services.chatbot.agent_service import answer_portfolio_question


class ChatbotApiTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        clear_chatbot_cache()

    def tearDown(self):
        clear_chatbot_cache()

    async def test_successful_answer_is_returned_and_cached(self):
        with patch(
            "app.api.v1.chatbot.answer_portfolio_question",
            new_callable=AsyncMock,
            return_value="Sagar has built several projects.",
        ) as mock_answer:
            response = await chat(
                ChatRequest(message="What projects has Sagar built?"),
                db=None,
            )

        self.assertEqual(
            response.answer,
            "Sagar has built several projects.",
        )
        self.assertEqual(
            get_cached_answer("What projects has Sagar built?"),
            "Sagar has built several projects.",
        )
        mock_answer.assert_awaited_once()

    async def test_cached_answer_skips_ai_call(self):
        from app.services.chatbot.chatbot_cache import cache_answer

        cache_answer("Tell me about Sagar", "Cached response")

        with patch(
            "app.api.v1.chatbot.answer_portfolio_question",
            new_callable=AsyncMock,
        ) as mock_answer:
            response = await chat(
                ChatRequest(message="Tell me about Sagar"),
                db=None,
            )

        self.assertEqual(response.answer, "Cached response")
        mock_answer.assert_not_awaited()

    async def test_provider_failure_returns_safe_503_and_is_not_cached(self):
        question = "What projects has Sagar built?"

        with patch(
            "app.api.v1.chatbot.answer_portfolio_question",
            new_callable=AsyncMock,
            side_effect=OpenRouterServiceError(
                "Internal provider error with sensitive details"
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                await chat(ChatRequest(message=question), db=None)

        self.assertEqual(context.exception.status_code, 503)
        self.assertNotIn(
            "sensitive details",
            str(context.exception.detail),
        )
        self.assertIsNone(get_cached_answer(question))

    async def test_whitespace_only_message_returns_422(self):
        with self.assertRaises(HTTPException) as context:
            await chat(ChatRequest(message="   "), db=None)

        self.assertEqual(context.exception.status_code, 422)


class ChatbotAgentSafetyTests(unittest.IsolatedAsyncioTestCase):
    async def test_invalid_provider_response_is_rejected(self):
        with patch(
            "app.services.chatbot.agent_service.create_chat_completion",
            new_callable=AsyncMock,
            return_value=None,
        ):
            with self.assertRaises(OpenRouterServiceError):
                await answer_portfolio_question(
                    db=None,
                    question="Tell me about Sagar",
                )

    async def test_too_many_tool_calls_are_rejected(self):
        tool_calls = [
            {
                "id": f"call-{index}",
                "type": "function",
                "function": {
                    "name": "get_profile",
                    "arguments": "{}",
                },
            }
            for index in range(5)
        ]

        with patch(
            "app.services.chatbot.agent_service.create_chat_completion",
            new_callable=AsyncMock,
            return_value={
                "role": "assistant",
                "content": None,
                "tool_calls": tool_calls,
            },
        ):
            with self.assertRaises(OpenRouterServiceError):
                await answer_portfolio_question(
                    db=None,
                    question="Tell me about Sagar",
                )


if __name__ == "__main__":
    unittest.main()
