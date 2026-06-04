from unittest.mock import Mock

from src.vector_store.create_store import (
    VECTOR_STORE_NAME,
    get_or_create_vector_store,
    save_vector_store_id,
)


def test_get_or_create_vector_store_calls_openai_client():
    mock_client = Mock()
    existing_store = Mock()
    existing_store.id = "vs_test123"
    existing_store.name = VECTOR_STORE_NAME

    stores_response = Mock()
    stores_response.data = [existing_store]

    mock_client.vector_stores.list.return_value = stores_response

    vector_store = get_or_create_vector_store(mock_client)

    assert vector_store.id == "vs_test123"
    assert vector_store.name == VECTOR_STORE_NAME


def test_save_vector_store_id_writes_file(tmp_path):
    output_file = tmp_path / "vector_store_id.txt"

    save_vector_store_id("vs_test123", output_file=output_file)

    assert output_file.read_text(encoding="utf-8") == "vs_test123"