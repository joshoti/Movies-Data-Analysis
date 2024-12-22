import unittest

from api import create_app
from api.extensions.db import csv_path, db_client
from tests import TestConfig


class TestQueryEndpoint(unittest.TestCase):
    def setUp(self):
        test_app = create_app(TestConfig)

        with test_app.app_context():
            db_client.init_db(csv_path)
            db_client.load_dataframe()

        self.test_client = test_app.test_client()

    def test_query(self):
        response = self.test_client.get("/query")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)

    def test_query_select_one_column(self):
        response = self.test_client.get("/query?select=title")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertEqual(len(response.json[0]), 1)


if __name__ == "__main__":
    unittest.main()
