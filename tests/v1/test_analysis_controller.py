import unittest

from api.v1.app import create_app
from api.v1.extensions.db import csv_path, db_client
from tests.v1 import TestConfig


class TestAnalysisEndpoint(unittest.TestCase):
    def setUp(self):
        test_app = create_app(TestConfig)

        with test_app.app_context():
            db_client.init_db(csv_path)
            db_client.load_dataframe()

        self.test_client = test_app.test_client()

    def test_analysis(self):
        number_of_samples = 5
        for i in range(1, number_of_samples + 1):
            response = self.test_client.get(f"/analysis/sample-{i}")
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.json)


if __name__ == "__main__":
    unittest.main()
