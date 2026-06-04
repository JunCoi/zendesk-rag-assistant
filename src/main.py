from dotenv import load_dotenv
from openai import OpenAI

from src.zendesk.fetch_articles import fetch_articles, save_articles
from src.markdown.convert_articles import main as convert_saved_articles_to_markdown
from src.vector_store.create_store import get_or_create_vector_store
from src.vector_store.upload_files import (
    get_markdown_files,
    upload_markdown_files,
    attach_files_to_vector_store,
)
from src.sync import detect_changed_files


def main():
    try:
        load_dotenv()

        client = OpenAI()

        print("Fetching Zendesk articles...")
        articles = fetch_articles()
        save_articles(articles)

        print("Converting articles to Markdown...")
        convert_saved_articles_to_markdown()

        markdown_files = get_markdown_files()
        changed_files, counts = detect_changed_files(markdown_files)

        print(
            f"Sync summary: "
            f"added={counts['added']}, "
            f"updated={counts['updated']}, "
            f"skipped={counts['skipped']}"
        )

        if not changed_files:
            print("No new or updated files. Nothing to upload.")
            print("Daily sync completed successfully.")
            return

        vector_store = get_or_create_vector_store(client)

        file_ids = upload_markdown_files(client, changed_files)

        attach_files_to_vector_store(
            client=client,
            vector_store_id=vector_store.id,
            file_ids=file_ids,
        )

        print(f"Uploaded {len(file_ids)} changed files.")
        print("Daily sync completed successfully.")
        
    except Exception as error:
        print(f"Daily sync failed: {type(error).__name__}: {error}")
        raise


if __name__ == "__main__":
    main()