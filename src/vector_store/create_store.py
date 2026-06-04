from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

VECTOR_STORE_ID_FILE = Path("vector_store_id.txt")
VECTOR_STORE_NAME = "Zendesk Support Knowledge Base"


def get_or_create_vector_store(client):
    stores = client.vector_stores.list()

    for store in stores.data:
        if store.name == VECTOR_STORE_NAME:
            return store

    return client.vector_stores.create(
        name=VECTOR_STORE_NAME
    )


def save_vector_store_id(vector_store_id: str, output_file=VECTOR_STORE_ID_FILE):
    output_file.write_text(vector_store_id, encoding="utf-8")


def main():
    client = OpenAI()

    vector_store = get_or_create_vector_store(client)
    save_vector_store_id(vector_store.id)

    print("Vector store created")
    print(f"Vector store ID: {vector_store.id}")


if __name__ == "__main__":
    main()