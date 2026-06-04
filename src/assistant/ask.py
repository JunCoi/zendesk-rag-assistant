from pathlib import Path
import time

import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

ASSISTANT_ID_FILE = Path("assistant_id.txt")


def wait_for_run(thread_id: str, run_id: str):
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id,
        )

        if run.status == "completed":
            return

        if run.status in ["failed", "cancelled", "expired"]:
            print(run)

            if hasattr(run, "last_error"):
                print("Last Error:", run.last_error)

            raise Exception(f"Run failed with status: {run.status}")

        time.sleep(1)


def get_latest_answer(thread_id: str):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    for message in messages.data:
        if message.role == "assistant":
            return message.content[0].text.value

    return "No answer found"


def remove_file_citations(text: str) -> str:
    return re.sub(r"【[^】]*†[^】]*】", "", text).strip()


def main():
    assistant_id = ASSISTANT_ID_FILE.read_text().strip()

    thread = client.beta.threads.create()

    print("Assistant ready. Type 'exit' to quit.\n")

    while True:
        question = input("> ")

        if question.lower() == "exit":
            break

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question,
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )

        wait_for_run(thread.id, run.id)

        answer = get_latest_answer(thread.id)
        clean_answer = remove_file_citations(answer)

        print("\nAnswer:")
        print(clean_answer)
        print()


if __name__ == "__main__":
    main()