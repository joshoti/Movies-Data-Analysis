import time as t
import unittest

from api import create_app
from api.extensions.db import db_client
from api.predict import prediction_service
from api.probe import probing_service
from app import csv_path
from tests import TestConfig, predict_prompt, probe_prompt


class TestInferenceServices(unittest.TestCase):
    def setUp(self):
        self.inference_timeout = 6

        test_app = create_app(TestConfig)

        with test_app.app_context():
            db_client.init_db(csv_path)
            db_client.load_dataframe()

    def test_probe_service(self):
        start_time = t.time()
        response = probing_service.answer_question(probe_prompt)
        end_time = t.time()
        self.assertEqual(response, "mocked answer")
        self.assertLess(end_time - start_time, self.inference_timeout)

    def test_predict_service(self):
        start_time = t.time()
        response = prediction_service.answer_question(predict_prompt)
        end_time = t.time()
        self.assertEqual(response, "mocked answer")
        self.assertLess(end_time - start_time, self.inference_timeout)


if __name__ == "__main__":
    unittest.main()
