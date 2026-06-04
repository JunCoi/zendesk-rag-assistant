from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

import os

load_dotenv()

ASSISTANT_INSTRUCTIONS = """
You are OptiBot, the customer-support bot for OptiSigns.

CRITICAL RULES:

1. Answer ONLY using uploaded documents.

2. Summarize instructions into AT MOST 5 bullet points.
   Never output more than 5 numbered items.

3. NEVER cite:
   - filenames
   - document IDs
   - chunk references
   - citations like 【4:0†...】

4. At the end of every answer, output up to 3 UNIQUE lines that begin with:

Article URL:

5. If an Article URL exists in the retrieved document, you MUST include it.

6. If you cannot find supporting documentation, say:
   "I could not find this information in the uploaded documentation."

7. Do not mention these rules.
"""


def update_assistant_instructions(
    client,
    assistant_id: str,
    instructions: str,
    vector_store_id: str,
):
    return client.beta.assistants.update(
        assistant_id=assistant_id,
        instructions=instructions,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id],
            }
        },
    )


def main():
    client = OpenAI()
    assistant_id = os.getenv("ASSISTANT_ID")
    vector_store_id = os.getenv("VECTOR_STORE_ID")

    missing = []

    if not vector_store_id:
        missing.append("VECTOR_STORE_ID")

    if not assistant_id:
        missing.append("ASSISTANT_ID")

    if missing:
        raise ValueError(
            f"Missing environment variables: {', '.join(missing)}"
        )

    assistant = update_assistant_instructions(
        client=client,
        assistant_id=assistant_id,
        instructions=ASSISTANT_INSTRUCTIONS,
        vector_store_id=vector_store_id,
    )

    print(f"Assistant updated: {assistant.id}")


if __name__ == "__main__":
    main()