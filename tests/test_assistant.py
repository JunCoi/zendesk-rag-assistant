from unittest.mock import Mock

from src.assistant.create_assistant import (
    ASSISTANT_INSTRUCTIONS,
    ASSISTANT_MODEL,
    ASSISTANT_NAME,
    create_assistant,
    save_assistant_id,
)
from src.assistant.update_assistant import update_assistant_instructions


def test_create_assistant_calls_openai_client():
    mock_client = Mock()
    mock_client.beta.assistants.create.return_value.id = "asst_test123"

    assistant = create_assistant(
        client=mock_client,
        vector_store_id="vs_test123",
    )

    mock_client.beta.assistants.create.assert_called_once_with(
        name=ASSISTANT_NAME,
        instructions=ASSISTANT_INSTRUCTIONS,
        model=ASSISTANT_MODEL,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": ["vs_test123"],
            }
        },
    )

    assert assistant.id == "asst_test123"


def test_save_assistant_id_writes_file(tmp_path):
    output_file = tmp_path / "assistant_id.txt"

    save_assistant_id("asst_test123", output_file=output_file)

    assert output_file.read_text(encoding="utf-8") == "asst_test123"


def test_update_assistant_instructions_calls_openai_client():
    mock_client = Mock()
    mock_client.beta.assistants.update.return_value.id = "asst_test123"

    assistant = update_assistant_instructions(
        client=mock_client,
        assistant_id="asst_test123",
        instructions="New instructions",
        vector_store_id="vs_test123",
    )

    mock_client.beta.assistants.update.assert_called_once_with(
        assistant_id="asst_test123",
        instructions="New instructions",
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": ["vs_test123"],
            }
        },
    )

    assert assistant.id == "asst_test123"