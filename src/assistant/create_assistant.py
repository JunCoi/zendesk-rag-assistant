from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

VECTOR_STORE_ID_FILE = Path("vector_store_id.txt")
ASSISTANT_ID_FILE = Path("assistant_id.txt")

ASSISTANT_NAME = "Support Knowledge Assistant"
ASSISTANT_MODEL = "gpt-4.1-mini"

ASSISTANT_INSTRUCTIONS = """
You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply.
"""


def create_assistant(client, vector_store_id: str):
    return client.beta.assistants.create(
        name=ASSISTANT_NAME,
        instructions=ASSISTANT_INSTRUCTIONS,
        model=ASSISTANT_MODEL,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id],
            }
        },
    )


def save_assistant_id(assistant_id: str, output_file=ASSISTANT_ID_FILE):
    output_file.write_text(assistant_id, encoding="utf-8")


def main():
    client = OpenAI()
    vector_store_id = VECTOR_STORE_ID_FILE.read_text().strip()

    assistant = create_assistant(
        client=client,
        vector_store_id=vector_store_id,
    )

    save_assistant_id(assistant.id)

    print(f"Assistant created: {assistant.id}")


if __name__ == "__main__":
    main()