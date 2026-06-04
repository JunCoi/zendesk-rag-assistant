from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

VECTOR_STORE_ID_FILE = Path("vector_store_id.txt")
ASSISTANT_ID_FILE = Path("assistant_id.txt")


def main():
    vector_store_id = VECTOR_STORE_ID_FILE.read_text().strip()

    assistant = client.beta.assistants.create(
        name="Support Knowledge Assistant",
        instructions="""
            You are a helpful support assistant.
            Answer questions using the uploaded knowledge base.
            If the answer cannot be found in the knowledge base,
            say so clearly.
            Always cite sources when possible.
        """,
        model="gpt-4.1-mini",
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
            }
        }
    )

    ASSISTANT_ID_FILE.write_text(
        assistant.id,
        encoding="utf-8"
    )

    print(f"Assistant created: {assistant.id}")


if __name__ == "__main__":
    main()