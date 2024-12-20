import asyncio
import time

from api import create_app
from api.extensions.db import db_client
from notebooks.inference import inference_service

csv_path = "./data/external/MoviesDataset.csv"


async def main():
    app = create_app()



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
