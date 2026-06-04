from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

import os

load_dotenv()

client = OpenAI()

VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")


def main():
    vector_store_id = os.getenv("VECTOR_STORE_ID")

    if not vector_store_id:
        raise ValueError("VECTOR_STORE_ID is not configured")
    
    vector_store = client.vector_stores.retrieve(
        vector_store_id
    )

    print(f"Status: {vector_store.status}")
    print(f"File count: {vector_store.file_counts}")


if __name__ == "__main__":
    main()