from src.markdown.convert_articles import (
    slugify,
    convert_html_to_markdown,
    convert_article,
)


def test_slugify():
    assert slugify("Accepted Payment Methods") == "accepted-payment-methods"
    assert slugify("How to Use YouTube App!") == "how-to-use-youtube-app"


def test_convert_html_to_markdown_preserves_heading_and_link():
    html = """
    <h2>Steps</h2>
    <p>Visit <a href="https://example.com">Example</a></p>
    """

    result = convert_html_to_markdown(html)

    assert "## Steps" in result
    assert "[Example](https://example.com)" in result


def test_convert_html_to_markdown_preserves_list():
    html = """
    <ul>
        <li>Open Assets</li>
        <li>Click Apps</li>
    </ul>
    """

    result = convert_html_to_markdown(html)

    assert "- Open Assets" in result
    assert "- Click Apps" in result


def test_convert_article_adds_title_source_and_body():
    article = {
        "title": "Accepted Payment Methods",
        "html_url": "https://support.optisigns.com/example",
        "body": "<p>Credit cards are accepted.</p>",
    }

    result = convert_article(article)

    assert "# Accepted Payment Methods" in result
    assert "Article URL: https://support.optisigns.com/example" in result
    assert "Credit cards are accepted." in result