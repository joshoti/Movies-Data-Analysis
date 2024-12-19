import asyncio
import time

from api.controllers.analysis import analysis_bp
from api.controllers.predict import predict_bp
from api.controllers.probe import probe_bp
from api.controllers.query import query_bp
from api.services.dbclient import db_client
from api.utils.config import create_flask_app
from notebooks.inference import inference_service

app = create_flask_app(__name__)


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
