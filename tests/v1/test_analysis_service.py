import unittest

from api.v1.app import create_app
from api.v1.analysis import analysis_service
from api.v1.extensions.db import csv_path, db_client
from tests.v1 import TestConfig


class TestAnalysisService(unittest.TestCase):
    def setUp(self):
        test_app = create_app(TestConfig)

        with test_app.app_context():
            db_client.init_db(csv_path)
            db_client.load_dataframe()

    def test_complete_sample_data_functions(self):
        number_of_samples = 5
        for i in range(1, number_of_samples + 1):
            response = analysis_service.get_sample_data(f"sample-{i}")
            self.assertIsNotNone(response)

    def test_get_sample_data(self):
        response = analysis_service.get_sample_data("sample-1")
        self.assertIn("data", response)
        self.assertIn("min_rating", response)
        self.assertIn("max_rating", response)
        self.assertGreater(len(response["data"]), 0)


if __name__ == "__main__":
    unittest.main()
