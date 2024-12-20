import unittest
from unittest.mock import patch

from flask import Flask

from api.probe import probe_bp


class TestProbeEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(probe_bp)
        self.client = self.app.test_client()

    @patch("api.services.probe.probing_service.answer_question")
    def test_probe(self, mock_answer_question):
        mock_answer_question.return_value = "mocked answer"
        response = self.client.post("/probe", json={"prompt": "test prompt"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "mocked answer")


if __name__ == "__main__":
    unittest.main()
