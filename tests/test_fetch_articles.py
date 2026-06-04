import json

from unittest.mock import Mock, patch

from src.zendesk.fetch_articles import (fetch_articles, save_articles)


@patch("src.zendesk.fetch_articles.requests.get")
def test_fetch_articles_returns_articles(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "articles": [
            {"id": 1, "title": "Article 1"},
            {"id": 2, "title": "Article 2"},
        ],
        "next_page": None,
    }
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    articles = fetch_articles()

    assert len(articles) == 2
    assert articles[0]["title"] == "Article 1"
    assert articles[1]["title"] == "Article 2"


@patch("src.zendesk.fetch_articles.requests.get")
def test_fetch_articles_limits_to_30(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "articles": [{"id": i} for i in range(50)],
        "next_page": None,
    }
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    articles = fetch_articles()

    assert len(articles) == 30


def test_save_articles_writes_json_files(tmp_path):
    articles = [
        {"id": 1, "title": "Article 1"},
        {"id": 2, "title": "Article 2"},
    ]

    save_articles(articles, output_dir=tmp_path)

    first_file = tmp_path / "1.json"
    second_file = tmp_path / "2.json"

    assert first_file.exists()
    assert second_file.exists()

    assert json.loads(first_file.read_text(encoding="utf-8")) == articles[0]
    assert json.loads(second_file.read_text(encoding="utf-8")) == articles[1]