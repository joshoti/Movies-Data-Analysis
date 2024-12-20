import unittest
from unittest.mock import patch

from api.probe.probeService import probing_service


class TestProbingService(unittest.TestCase):
    @patch("api.services.probe.inference_service.use_hugging_face_pipeline")
    def test_answer_question(self, mock_use_hugging_face_pipeline):
        mock_use_hugging_face_pipeline.return_value = "mocked answer"
        response = probing_service.answer_question("test prompt")
        self.assertEqual(response, "mocked answer")


if __name__ == "__main__":
    unittest.main()
