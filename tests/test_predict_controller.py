import unittest
from unittest.mock import patch

from flask import Flask

from api.predict import predict_bp


class TestPredictEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(predict_bp)
        self.client = self.app.test_client()

    @patch("api.services.predict.prediction_service.answer_question")
    def test_predict(self, mock_answer_question):
        mock_answer_question.return_value = "mocked answer"
        response = self.client.post("/predict", json={"prompt": "test prompt"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "mocked answer")


if __name__ == "__main__":
    unittest.main()
