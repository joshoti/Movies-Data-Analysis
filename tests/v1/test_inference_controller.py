import unittest

from api.v1.app import create_app
from api.v1.extensions.db import csv_path, db_client
from notebooks.google_tapas import google_tapas_client
from notebooks.inference import inference_service
from tests.v1 import TestConfig, chat_prompt_1


class TestInferenceEndpoints(unittest.TestCase):
    def setUp(self):
        test_app = create_app(TestConfig)

        with test_app.app_context():
            db_client.init_db(csv_path)
            db_client.load_dataframe()

        inference_service.client = google_tapas_client
        inference_service.client.get_pipeline()

        self.test_client = test_app.test_client()

    def test_chat(self):
        response = self.test_client.post(
            "/chat",
            json={"prompt": chat_prompt_1},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)


if __name__ == "__main__":
    unittest.main()
