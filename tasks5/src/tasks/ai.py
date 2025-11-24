"""AI-powered task intelligence using OpenAI."""

from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

MODEL_NAME = "gpt-4o-mini"

# Lazy client initialization to avoid requiring API key at import time
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    """Get or create OpenAI client instance."""
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


def is_api_key_available() -> bool:
    """Check if OpenAI API key is configured."""
    return bool(os.getenv("OPENAI_API_KEY"))


def summarize_task(description: str) -> str:
    """Summarize a long task description into a short, actionable phrase.

    Args:
        description: Long task description

    Returns:
        Short summarized phrase or error message
    """
    if not description or not description.strip():
        return "Empty description"

    if not is_api_key_available():
        return "API key not set"

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "Summarize tasks as short, action-oriented phrases (5-10 words max).",
                },
                {"role": "user", "content": description.strip()},
            ],
            temperature=0.3,
            max_tokens=40,
        )
        content = response.choices[0].message.content
        return content.strip() if content else "No summary produced"
    except Exception as e:
        return f"Summary unavailable: {str(e)}"[:120]


def suggest_priority(description: str, due_date: str | None = None) -> dict[str, Any]:
    """Analyze task and suggest priority level with reasoning.

    Args:
        description: Task description
        due_date: Optional due date

    Returns:
        Dictionary with priority, estimate_hours, and reason
    """
    if not description or not description.strip():
        return {
            "priority": "medium",
            "estimate_hours": 1.0,
            "reason": "No description provided",
        }

    if not is_api_key_available():
        return {
            "priority": "medium",
            "estimate_hours": 1.0,
            "reason": "API key not configured",
        }

    context = description
    if due_date:
        context += f"\nDue date: {due_date}"

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyze the task and return JSON with: "
                        '{"priority": "low"|"medium"|"high", "estimate_hours": float, "reason": str}. '
                        "Consider urgency, complexity, and impact."
                    ),
                },
                {"role": "user", "content": context},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        content = response.choices[0].message.content
        if content:
            result = json.loads(content)
            # Validate and normalize
            if "priority" not in result:
                result["priority"] = "medium"
            if "estimate_hours" not in result:
                result["estimate_hours"] = 1.0
            if "reason" not in result:
                result["reason"] = "Analysis completed"
            return result
        return {
            "priority": "medium",
            "estimate_hours": 1.0,
            "reason": "No response from AI",
        }
    except Exception as e:
        return {
            "priority": "medium",
            "estimate_hours": 1.0,
            "reason": f"Error: {str(e)}"[:100],
        }


def get_task_advice(
    description: str,
    status: str,
    due_date: str | None = None,
    note: str | None = None,
) -> str:
    """Get AI-powered advice for completing a specific task.

    Args:
        description: Task description
        status: Current task status
        due_date: Optional due date
        note: Optional note

    Returns:
        Advice string or error message
    """
    if not description or not description.strip():
        return "No task description available for advice"

    if not is_api_key_available():
        return (
            "⚠️  OPENAI_API_KEY not set. Set it as an environment variable to get AI-powered advice."
        )

    # Build context
    context_parts = [f"Task: {description}", f"Current status: {status}"]
    if due_date:
        context_parts.append(f"Due date: {due_date}")
    if note:
        context_parts.append(f"Note: {note}")

    context = "\n".join(context_parts)

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a productivity coach. Provide practical, actionable advice "
                        "for completing the task. Include 2-3 specific tips or steps. "
                        "Keep it concise (3-5 sentences)."
                    ),
                },
                {"role": "user", "content": context},
            ],
            temperature=0.7,
            max_tokens=200,
        )
        content = response.choices[0].message.content
        return content.strip() if content else "No advice generated"
    except Exception as e:
        return f"⚠️  Could not get advice: {str(e)}"[:150]


def suggest_tags(description: str, max_tags: int = 3) -> list[str]:
    """Suggest relevant tags for a task.

    Args:
        description: Task description
        max_tags: Maximum number of tags to suggest

    Returns:
        List of suggested tags
    """
    if not description or not description.strip():
        return []

    if not is_api_key_available():
        return []

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Suggest {max_tags} relevant, lowercase tags for the task. "
                        'Return JSON: {"tags": ["tag1", "tag2", "tag3"]}'
                    ),
                },
                {"role": "user", "content": description.strip()},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=50,
        )
        content = response.choices[0].message.content
        if content:
            result = json.loads(content)
            return result.get("tags", [])
        return []
    except Exception:
        return []
