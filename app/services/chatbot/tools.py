
import json

from sqlalchemy.orm import Session

from app.services.chatbot.chatbot_service import (
    get_chatbot_experience,
    get_chatbot_profile,
    get_chatbot_projects,
    get_chatbot_technologies,
)


CHATBOT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_profile",
            "description": (
                "Get Sagar's public profile, professional headline, "
                "about information, location, and public contact links."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_projects",
            "description": (
                "Get the list of visible portfolio projects, including "
                "descriptions, technologies, and project links."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_experience",
            "description": (
                "Get Sagar's visible work experience, employers, roles, "
                "dates, and experience highlights."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_technologies",
            "description": (
                "Get the technologies and skill categories listed "
                "publicly on Sagar's portfolio."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
]


def execute_chatbot_tool(
    db: Session,
    tool_name: str,
    arguments: str | dict,
) -> str:
    """Execute only explicitly approved, read-only chatbot tools."""

    allowed_tools = {
        "get_profile": get_chatbot_profile,
        "get_projects": get_chatbot_projects,
        "get_experience": get_chatbot_experience,
        "get_technologies": get_chatbot_technologies,
    }

    if tool_name not in allowed_tools:
        return json.dumps({
            "error": "This tool is not available."
        })

    try:
        if isinstance(arguments, str):
            parsed_arguments = json.loads(arguments)
        else:
            parsed_arguments = arguments

        if not isinstance(parsed_arguments, dict):
            raise ValueError("Tool arguments must be an object.")

        if parsed_arguments:
            raise ValueError("This tool does not accept arguments.")

        result = allowed_tools[tool_name](db)

        return json.dumps(
            result,
            ensure_ascii=False,
            default=str,
        )

    except (ValueError, TypeError):
        return json.dumps({
            "error": "Invalid arguments for this tool."
        })
