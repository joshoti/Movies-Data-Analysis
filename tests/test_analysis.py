import unittest
from unittest.mock import patch

from api.analysis.analysisService import analysis_service


class TestAnalysisService(unittest.TestCase):
    @patch("api.services.dbclient.db_client.query_db")
    def test_get_data(self, mock_query_db):
        mock_query_db.return_value = [{"mock_key": "mock_value"}]
        query_params = {"query": "mock_query"}
        response = analysis_service.get_data(query_params)
        self.assertEqual(response, [{"mock_key": "mock_value"}])

    @patch("api.services.dbclient.db_client.dataframe")
    def test_get_sample_data(self, mock_dataframe):
        mock_dataframe.iloc.__getitem__.return_value = {
            "main_genre": "Action",
            "Rating": "7.0",
            "Runtime": "120",
            "Total_Gross": "$100M",
            "Year": "2020",
            "Censor": "PG",
        }
        response = analysis_service.get_sample_data("sample-1")
        self.assertIn("data", response)


if __name__ == "__main__":
    unittest.main()
