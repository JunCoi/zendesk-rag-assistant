from unittest.mock import Mock

from src.vector_store.upload_files import (
    get_markdown_files,
    upload_markdown_files,
    attach_files_to_vector_store,
)


def test_get_markdown_files_returns_only_markdown_files(tmp_path):
    markdown_file = tmp_path / "article.md"
    text_file = tmp_path / "notes.txt"

    markdown_file.write_text("# Article", encoding="utf-8")
    text_file.write_text("Not markdown", encoding="utf-8")

    result = get_markdown_files(tmp_path)

    assert result == [markdown_file]


def test_upload_markdown_files_uploads_files_and_returns_file_ids(tmp_path):
    file_one = tmp_path / "article-one.md"
    file_two = tmp_path / "article-two.md"

    file_one.write_text("# Article One", encoding="utf-8")
    file_two.write_text("# Article Two", encoding="utf-8")

    mock_client = Mock()
    mock_client.files.create.side_effect = [
        Mock(id="file_1"),
        Mock(id="file_2"),
    ]

    file_ids = upload_markdown_files(
        mock_client,
        [file_one, file_two],
    )

    assert file_ids == ["file_1", "file_2"]
    assert mock_client.files.create.call_count == 2

    first_call = mock_client.files.create.call_args_list[0]
    assert first_call.kwargs["purpose"] == "assistants"


def test_attach_files_to_vector_store_creates_file_batch():
    mock_client = Mock()

    attach_files_to_vector_store(
        client=mock_client,
        vector_store_id="vs_test123",
        file_ids=["file_1", "file_2"],
    )

    mock_client.vector_stores.file_batches.create.assert_called_once_with(
        vector_store_id="vs_test123",
        file_ids=["file_1", "file_2"],
    )