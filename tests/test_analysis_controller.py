import unittest
from unittest.mock import patch

from flask import Flask

from api.analysis.analysisController import analysis_bp


class TestAnalysisEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(analysis_bp)
        self.client = self.app.test_client()

    @patch("api.services.analysis.analysis_service.get_sample_data")
    def test_analysis(self, mock_get_sample_data):
        mock_get_sample_data.return_value = {"mock_key": "mock_value"}
        response = self.client.get("/analysis/sample-1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"mock_key": "mock_value"})


if __name__ == "__main__":
    unittest.main()
