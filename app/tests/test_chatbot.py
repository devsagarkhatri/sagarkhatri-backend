
import json
import unittest
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
from starlette.requests import Request

from app.services.chatbot.agent_service import answer_portfolio_question
from app.services.chatbot.chatbot_cache import (
    cache_answer,
    clear_chatbot_cache,
    get_cached_answer,
)
from app.services.chatbot.rate_limit import enforce_chat_rate_limit
from app.services.chatbot.tools import execute_chatbot_tool


def make_request(client_ip: str) -> Request:
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "POST",
            "scheme": "http",
            "path": "/api/v1/chatbot",
            "raw_path": b"/api/v1/chatbot",
            "query_string": b"",
            "headers": [],
            "client": (client_ip, 12345),
            "server": ("testserver", 80),
        }
    )


class ChatbotCacheTests(unittest.TestCase):
    def setUp(self):
        clear_chatbot_cache()

    def tearDown(self):
        clear_chatbot_cache()

    def test_cache_miss_and_hit(self):
        self.assertIsNone(get_cached_answer("What projects has Sagar built?"))

        cache_answer(
            "What projects has Sagar built?",
            "Sagar has built several projects.",
        )

        self.assertEqual(
            get_cached_answer("What projects has Sagar built?"),
            "Sagar has built several projects.",
        )

    def test_cache_normalizes_case_and_whitespace(self):
        cache_answer("What projects has Sagar built?", "Cached answer")

        self.assertEqual(
            get_cached_answer("  WHAT projects has Sagar built?  "),
            "Cached answer",
        )

    def test_expired_answer_is_not_returned(self):
        with patch(
            "app.services.chatbot.chatbot_cache.monotonic",
            return_value=100,
        ):
            cache_answer("Test question", "Old answer")

        with patch(
            "app.services.chatbot.chatbot_cache.monotonic",
            return_value=401,
        ):
            self.assertIsNone(get_cached_answer("Test question"))

    def test_cache_can_be_cleared(self):
        cache_answer("Test question", "Cached answer")
        clear_chatbot_cache()

        self.assertIsNone(get_cached_answer("Test question"))


class ChatbotRateLimitTests(unittest.TestCase):
    def test_excess_requests_are_rejected(self):
        # Use a unique synthetic client address for an isolated test.
        request = make_request(f"test-client-{id(self)}")

        for _ in range(10):
            enforce_chat_rate_limit(request)

        with self.assertRaises(HTTPException) as context:
            enforce_chat_rate_limit(request)

        self.assertEqual(context.exception.status_code, 429)

    def test_hourly_limit_is_enforced(self):
        from unittest.mock import patch
        from app.services.chatbot import rate_limit

        client_ip = f"hourly-test-{id(self)}"
        request = make_request(client_ip)

        # Use a controlled clock so all requests are within one hour,
        # but spaced far enough apart to avoid the per-minute limit.
        with patch.object(rate_limit, "monotonic") as mock_clock:
            mock_clock.return_value = 0

            for index in range(50):
                mock_clock.return_value = index * 61
                rate_limit.enforce_chat_rate_limit(request)

            mock_clock.return_value = 49 * 61 + 1

            with self.assertRaises(HTTPException) as context:
                rate_limit.enforce_chat_rate_limit(request)

        self.assertEqual(context.exception.status_code, 429)
        self.assertIn("Retry-After", context.exception.headers)


class ChatbotToolTests(unittest.TestCase):
    def test_unapproved_tool_is_rejected(self):
        result = execute_chatbot_tool(
            db=None,
            tool_name="delete_database",
            arguments="{}",
        )

        self.assertEqual(
            json.loads(result),
            {"error": "This tool is not available."},
        )

    def test_unexpected_tool_arguments_are_rejected(self):
        result = execute_chatbot_tool(
            db=None,
            tool_name="get_profile",
            arguments='{"unexpected": true}',
        )

        self.assertEqual(
            json.loads(result),
            {"error": "Invalid arguments for this tool."},
        )


class ChatbotAgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_final_answer_from_model(self):
        with patch(
            "app.services.chatbot.agent_service.create_chat_completion",
            new_callable=AsyncMock,
        ) as mock_completion:
            mock_completion.return_value = {
                "role": "assistant",
                "content": "Sagar has built several projects.",
            }

            answer = await answer_portfolio_question(
                db=None,
                question="What projects has Sagar built?",
            )

        self.assertEqual(answer, "Sagar has built several projects.")
        mock_completion.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
