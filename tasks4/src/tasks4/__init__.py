from openai import OpenAI

client = OpenAI()

def summarize(paragraph: str) -> str:
    """Use ChatGPT-4o-mini to summarize a long task description."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize tasks as short phrases."},
            {"role": "user", "content": paragraph},
        ]
    )

    return response.choices[0].message.content

def main():
    # At least two sample paragraph-length task descriptions
    paragraphs = [
        """I need to completely reorganize my bedroom closet. 
        Right now it’s full of mixed clothes, boxes, and random items. 
        I want to sort everything into seasons, donate items I don’t wear, 
        and create specific storage spaces for shoes and accessories.""",

        """For my software engineering class project, I need to review 
        all previous tasks, refactor old code, create proper documentation, 
        and prepare a demonstration video that explains how the system works."""
    ]

    for i, text in enumerate(paragraphs, start=1):
        summary = summarize(text)
        print(f"Task {i} Summary: {summary}\n")


if __name__ == "__main__":
    main()
