import asyncio
import time

from api import create_app
from api.extensions.db import db_client
from notebooks.inference import inference_service

app = create_app()


async def main():
    csv_path = "./data/external/MoviesDataset.csv"

    app.register_blueprint(analysis_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(probe_bp)
    app.register_blueprint(predict_bp)

    with app.app_context():
        db_client.init_db(csv_path)
        db_client.load_dataframe()
        # await asyncio.create_task(db_client.init_db(csv_path))
        # await asyncio.create_task(db_client.load_dataframe())

    # inference_service.load_default_qa_client()
    await asyncio.create_task(inference_service.load_default_qa_client())
    app.run()


if __name__ == "__main__":
    asyncio.run(main())
