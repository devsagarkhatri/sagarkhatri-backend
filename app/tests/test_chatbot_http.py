
import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.services.chatbot.chatbot_cache import (
    cache_answer,
    clear_chatbot_cache,
)
from app.services.chatbot.openrouter_service import OpenRouterServiceError
from app.services.chatbot.rate_limit import enforce_chat_rate_limit


class ChatbotHttpTests(unittest.TestCase):
    def setUp(self):
        clear_chatbot_cache()
        self.original_overrides = app.dependency_overrides.copy()

        app.dependency_overrides[get_db] = lambda: None
        app.dependency_overrides[enforce_chat_rate_limit] = lambda: None

        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self.original_overrides)
        clear_chatbot_cache()

    def test_successful_request_returns_expected_json(self):
        with patch(
            "app.api.v1.chatbot.answer_portfolio_question",
            new_callable=AsyncMock,
            return_value="Sagar is a software engineer.",
        ) as mock_answer:
            response = self.client.post(
                "/api/v1/chatbot",
                json={"message": "Tell me about Sagar"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"answer": "Sagar is a software engineer."},
        )
        mock_answer.assert_awaited_once()

    def test_cached_answer_is_returned_over_http(self):
        cache_answer("Tell me about Sagar", "Cached answer")

        with patch(
            "app.api.v1.chatbot.answer_portfolio_question",
            new_callable=AsyncMock,
        ) as mock_answer:
            response = self.client.post(
                "/api/v1/chatbot",
                json={"message": "Tell me about Sagar"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"answer": "Cached answer"})
        mock_answer.assert_not_awaited()

    def test_provider_failure_returns_safe_503(self):
        with patch(
            "app.api.v1.chatbot.answer_portfolio_question",
            new_callable=AsyncMock,
            side_effect=OpenRouterServiceError(
                "Sensitive internal provider details"
            ),
        ):
            response = self.client.post(
                "/api/v1/chatbot",
                json={"message": "Tell me about Sagar"},
            )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json()["detail"],
            "The portfolio assistant is temporarily unavailable. "
            "Please try again later.",
        )
        self.assertNotIn(
            "Sensitive internal provider details",
            response.text,
        )

    def test_whitespace_only_message_returns_422(self):
        response = self.client.post(
            "/api/v1/chatbot",
            json={"message": "   "},
        )

        self.assertEqual(response.status_code, 422)

    def test_oversized_message_returns_422(self):
        response = self.client.post(
            "/api/v1/chatbot",
            json={"message": "x" * 2001},
        )

        self.assertEqual(response.status_code, 422)

    def test_missing_message_returns_422(self):
        response = self.client.post(
            "/api/v1/chatbot",
            json={},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
