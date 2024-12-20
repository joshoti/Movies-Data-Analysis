import unittest

from api import create_app
from api.extensions.db import db_client
from api.query import query_service
from app import csv_path
from tests import TestConfig


class TestQueryService(unittest.TestCase):
    def setUp(self):
        self.test_app = create_app(TestConfig)

        with self.test_app.app_context():
            db_client.init_db(csv_path)
            db_client.load_dataframe()

    def test_query(self):
        with self.test_app.app_context():
            query = {}
            response: list[dict] = query_service.get_data(query)

        # Many results, each result has complete columns
        self.assertGreater(len(response), 0)
        self.assertEqual(len(response[0].keys()), len(db_client.columns))

    def test_query_with_select(self):
        with self.test_app.app_context():
            query = {"select": "title"}
            response: list[dict] = query_service.get_data(query)

        # Many results, each result has one column
        self.assertGreater(len(response), 0)
        self.assertEqual(len(response[0].keys()), 1)

    def test_query_with_where(self):
        with self.test_app.app_context():
            query = {"where": "AND-title-=-The Shawshank Redemption"}
            response: list[dict] = query_service.get_data(query)

        # One result, that result has complete columns
        self.assertEqual(len(response), 1)
        self.assertEqual(len(response[0].keys()), len(db_client.columns))

    def test_query_with_select_and_where(self):
        with self.test_app.app_context():
            query = {"select": "title", "where": "AND-title-=-The Shawshank Redemption"}
            response: list[dict] = query_service.get_data(query)

        # One result, that result has one column
        self.assertEqual(len(response), 1)
        self.assertEqual(len(response[0].keys()), 1)


if __name__ == "__main__":
    unittest.main()
