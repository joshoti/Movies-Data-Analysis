from threading import Thread

from api import create_app
from api.extensions.db import csv_path, db_client
from notebooks.inference import inference_service

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db_client.init_db(csv_path)
        Thread(target=db_client.load_dataframe).run()

    Thread(target=inference_service.load_default_qa_client).run()

    app.run()
