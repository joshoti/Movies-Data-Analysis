import time as t
import unittest

from api.v1.app import create_app
from api.v1.extensions.db import csv_path, db_client
from api.v1.chat import chat_service
from notebooks.google_tapas import google_tapas_client
from notebooks.inference import inference_service
from tests.v1 import TestConfig, chat_prompt_1, chat_prompt_2


class TestInferenceServices(unittest.TestCase):
    def setUp(self):
        self.inference_timeout = 6

        test_app = create_app(TestConfig)

        with test_app.app_context():
            db_client.init_db(csv_path)
            db_client.load_dataframe()

        inference_service.client = google_tapas_client
        inference_service.client.get_pipeline()

    def test_chat_service(self):
        start_time = t.time()
        response = chat_service.answer_question(chat_prompt_1)
        end_time = t.time()
        self.assertIsNotNone(response)
        self.assertGreater(
            len(response.split(",")), 3
        )  # result lists more than 3 items
        self.assertLess(end_time - start_time, self.inference_timeout)

    def test_chat_service_2(self):
        start_time = t.time()
        response = chat_service.answer_question(chat_prompt_2)
        end_time = t.time()
        self.assertIsNotNone(response)
        self.assertGreater(len(response.split(",")), 1)
        self.assertLess(end_time - start_time, self.inference_timeout)


if __name__ == "__main__":
    unittest.main()
