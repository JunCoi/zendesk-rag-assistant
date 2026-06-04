from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

VECTOR_STORE_ID_FILE = Path("vector_store_id.txt")


def main():
    vector_store_id = VECTOR_STORE_ID_FILE.read_text().strip()

    vector_store = client.vector_stores.retrieve(
        vector_store_id
    )

    print(f"Status: {vector_store.status}")
    print(f"File count: {vector_store.file_counts}")


if __name__ == "__main__":
    main()