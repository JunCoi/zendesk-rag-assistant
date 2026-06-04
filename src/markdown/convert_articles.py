import json
import re
from pathlib import Path

from markdownify import markdownify as md

RAW_DIR = Path("data/raw")
MARKDOWN_DIR = Path("data/markdown")
MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def convert_html_to_markdown(html: str) -> str:
    markdown = md(
        html,
        heading_style="ATX",
        bullets="-",
    )

    # Clean excessive blank lines
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    return markdown.strip()


def convert_article(article: dict) -> str:
    title = article.get("title", "Untitled")
    url = article.get("html_url", "")
    body_html = article.get("body", "")

    body_markdown = convert_html_to_markdown(body_html)

    return f"""# {title}

Source: {url}

{body_markdown}
"""


def main():
    files = list(RAW_DIR.glob("*.json"))

    for file_path in files:
        with file_path.open("r", encoding="utf-8") as file:
            article = json.load(file)

        title = article.get("title", file_path.stem)
        slug = article.get("slug") or slugify(title)

        markdown = convert_article(article)

        output_path = MARKDOWN_DIR / f"{slug}.md"
        output_path.write_text(markdown, encoding="utf-8")

    print(f"Converted {len(files)} articles to Markdown in {MARKDOWN_DIR}")


if __name__ == "__main__":
    main()