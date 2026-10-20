
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from fastapi import HTTPException

from app.api.v1 import experience, profile, projects, technologies


class ChatbotCacheInvalidationTests(unittest.TestCase):
    def setUp(self):
        self.db = object()
        self.admin = object()
        self.payload = SimpleNamespace(
            model_dump=lambda **kwargs: {"name": "Test record"}
        )

    def assert_mutation_clears_cache(
        self,
        module,
        handler_name,
        service_name,
        args,
    ):
        with (
            patch.object(module, service_name, return_value=object()),
            patch.object(module, "clear_chatbot_cache") as clear_cache,
        ):
            handler = getattr(module, handler_name)
            handler(*args, admin=self.admin)

        clear_cache.assert_called_once_with()

    def assert_missing_record_does_not_clear_cache(
        self,
        module,
        handler_name,
        service_name,
        args,
    ):
        with (
            patch.object(module, service_name, return_value=None),
            patch.object(module, "clear_chatbot_cache") as clear_cache,
        ):
            handler = getattr(module, handler_name)

            with self.assertRaises(HTTPException) as context:
                handler(*args, admin=self.admin)

        self.assertEqual(context.exception.status_code, 404)
        clear_cache.assert_not_called()

    def test_successful_mutations_clear_cache(self):
        mutation_cases = [
            (
                profile,
                "edit_profile",
                "update_profile",
                (self.payload, self.db),
            ),
            (
                projects,
                "add_project",
                "create_project",
                (self.payload, self.db),
            ),
            (
                projects,
                "edit_project",
                "update_project",
                (uuid4(), self.payload, self.db),
            ),
            (
                projects,
                "remove_project",
                "delete_project",
                (uuid4(), self.db),
            ),
            (
                experience,
                "add_experience",
                "create_experience",
                (self.payload, self.db),
            ),
            (
                experience,
                "edit_experience",
                "update_experience",
                (uuid4(), self.payload, self.db),
            ),
            (
                experience,
                "remove_experience",
                "delete_experience",
                (uuid4(), self.db),
            ),
            (
                technologies,
                "add_technology",
                "create_technology",
                (self.payload, self.db),
            ),
            (
                technologies,
                "edit_technology",
                "update_technology",
                (uuid4(), self.payload, self.db),
            ),
            (
                technologies,
                "remove_technology",
                "delete_technology",
                (uuid4(), self.db),
            ),
        ]

        for module, handler, service, args in mutation_cases:
            with self.subTest(
                module=module.__name__,
                handler=handler,
            ):
                self.assert_mutation_clears_cache(
                    module,
                    handler,
                    service,
                    args,
                )

    def test_missing_records_do_not_clear_cache(self):
        missing_record_cases = [
            (
                profile,
                "edit_profile",
                "update_profile",
                (self.payload, self.db),
            ),
            (
                projects,
                "edit_project",
                "update_project",
                (uuid4(), self.payload, self.db),
            ),
            (
                experience,
                "edit_experience",
                "update_experience",
                (uuid4(), self.payload, self.db),
            ),
            (
                technologies,
                "edit_technology",
                "update_technology",
                (uuid4(), self.payload, self.db),
            ),
        ]

        for module, handler, service, args in missing_record_cases:
            with self.subTest(
                module=module.__name__,
                handler=handler,
            ):
                self.assert_missing_record_does_not_clear_cache(
                    module,
                    handler,
                    service,
                    args,
                )


if __name__ == "__main__":
    unittest.main()
