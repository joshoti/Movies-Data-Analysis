from unittest.mock import patch

from api.v2.services.chat_service import chat_service


@patch(
    "api.v2.services.chat_service.inference_service.use_hugging_face_pipeline",
    return_value="mocked-answer",
)
def test_chat_service_uses_inference(mock_pipeline):
    answer = chat_service.answer_question("Hello?")
    assert answer == "mocked-answer"
    mock_pipeline.assert_called_once()
