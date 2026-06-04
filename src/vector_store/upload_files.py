from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

import os

load_dotenv()

MARKDOWN_DIR = Path("data/markdown")


def get_markdown_files(markdown_dir=MARKDOWN_DIR):
    return list(markdown_dir.glob("*.md"))


def upload_markdown_files(client, markdown_files):
    file_ids = []

    for file_path in markdown_files:
        print(f"Uploading {file_path.name}")

        with file_path.open("rb") as file:
            uploaded_file = client.files.create(
                file=file,
                purpose="assistants",
            )

        file_ids.append(uploaded_file.id)

    return file_ids


def attach_files_to_vector_store(client, vector_store_id, file_ids):
    return client.vector_stores.file_batches.create(
        vector_store_id=vector_store_id,
        file_ids=file_ids,
    )


def main():
    client = OpenAI()

    vector_store_id = os.getenv("VECTOR_STORE_ID")

    if not vector_store_id:
        raise ValueError("VECTOR_STORE_ID is not configured")
    
    markdown_files = get_markdown_files()

    file_ids = upload_markdown_files(client, markdown_files)

    print(f"Uploaded {len(file_ids)} files")

    attach_files_to_vector_store(
        client=client,
        vector_store_id=vector_store_id,
        file_ids=file_ids,
    )

    print("Files attached to vector store")


if __name__ == "__main__":
    main()