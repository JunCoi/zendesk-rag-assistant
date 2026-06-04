from unittest.mock import Mock

from src.vector_store.create_store import (
    VECTOR_STORE_NAME,
    create_vector_store,
    save_vector_store_id,
)


def test_create_vector_store_calls_openai_client():
    mock_client = Mock()
    mock_client.vector_stores.create.return_value.id = "vs_test123"

    vector_store = create_vector_store(mock_client)

    mock_client.vector_stores.create.assert_called_once_with(
        name=VECTOR_STORE_NAME
    )
    assert vector_store.id == "vs_test123"


def test_save_vector_store_id_writes_file(tmp_path):
    output_file = tmp_path / "vector_store_id.txt"

    save_vector_store_id("vs_test123", output_file=output_file)

    assert output_file.read_text(encoding="utf-8") == "vs_test123"