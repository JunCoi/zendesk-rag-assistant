from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

MARKDOWN_DIR = Path("data/markdown")
VECTOR_STORE_ID_FILE = Path("vector_store_id.txt")


def main():
    vector_store_id = VECTOR_STORE_ID_FILE.read_text().strip()

    markdown_files = list(MARKDOWN_DIR.glob("*.md"))

    file_ids = []

    for file_path in markdown_files:
        print(f"Uploading {file_path.name}")

        with open(file_path, "rb") as file:
            uploaded_file = client.files.create(
                file=file,
                purpose="assistants"
            )

        file_ids.append(uploaded_file.id)

    print(f"Uploaded {len(file_ids)} files")

    client.vector_stores.file_batches.create(
        vector_store_id=vector_store_id,
        file_ids=file_ids,
    )

    print("Files attached to vector store")


if __name__ == "__main__":
    main()