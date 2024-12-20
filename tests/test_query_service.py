import unittest
from unittest.mock import patch

from flask import Flask

from api.query import query_bp


class TestQueryService(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(query_bp)
        self.client = self.app.test_client()

    @patch("api.services.query.query_service.get_data")
    def test_query(self, mock_get_data):
        mock_get_data.return_value = {"mock_key": "mock_value"}
        response = self.client.get("/query")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"mock_key": "mock_value"})


if __name__ == "__main__":
    unittest.main()
