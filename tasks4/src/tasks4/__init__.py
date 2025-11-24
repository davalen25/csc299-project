"""Task summarization script using OpenAI's chat completion API.

Run with: `uv run tasks4`

This module summarizes multiple paragraph-length task descriptions into short phrases.
Includes basic error handling for missing API key or API failures.
"""

from openai import OpenAI
import os

# Instantiate client (relies on OPENAI_API_KEY environment variable)
client = OpenAI()

MODEL_NAME = "gpt-4o-mini"

def summarize(paragraph: str) -> str:
    """Use ChatGPT to summarize a long task description into a short phrase.

    Returns a fallback message on error instead of raising.
    """
    if not paragraph or not paragraph.strip():
        return "Empty description"
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Summarize tasks as short, action-oriented phrases."},
                {"role": "user", "content": paragraph.strip()},
            ],
            temperature=0.3,
            max_tokens=40,
        )
        content = response.choices[0].message.content
        return content.strip() if content else "No summary produced"
    except Exception as e:  # Catch any SDK/network/API errors
        return f"Summary unavailable: {e}"[:120]

def main() -> None:
    # Sample paragraph-length task descriptions
    paragraphs = [
        (
            "I need to completely reorganize my bedroom closet. Right now it's full of mixed clothes, boxes, and random "
            "items. I want to sort everything into seasons, donate items I don't wear, and create specific storage "
            "spaces for shoes and accessories."
        ),
        (
            "For my software engineering class project, I need to review all previous tasks, refactor old code, create "
            "proper documentation, and prepare a demonstration video that explains how the system works."
        ),
    ]

    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. Set it to get real summaries.")

    for i, text in enumerate(paragraphs, start=1):
        summary = summarize(text)
        print(f"Task {i} Summary: {summary}\n")

if __name__ == "__main__":  # pragma: no cover
    main()
