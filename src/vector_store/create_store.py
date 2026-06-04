from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

VECTOR_STORE_ID_FILE = Path("vector_store_id.txt")

client = OpenAI()


def main():
    vector_store = client.vector_stores.create(
        name="Zendesk Support Knowledge Base"
    )

    VECTOR_STORE_ID_FILE.write_text(vector_store.id, encoding="utf-8")

    print("Vector store created")
    print(f"Vector store ID: {vector_store.id}")


if __name__ == "__main__":
    main()