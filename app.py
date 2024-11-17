from threading import Thread

from flask import Flask

from api.controller.analysis import analysis_bp
from api.controller.predict import predict_bp
from api.controller.probe import probe_bp
from api.extensions.db import db
from api.services.dbclient import db_client
from api.utils.config import Config
from notebooks.inference import inference_service

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


if __name__ == "__main__":
    csv_path = "./data/external/MoviesDataset.csv"

    app.register_blueprint(analysis_bp)
    app.register_blueprint(probe_bp)
    app.register_blueprint(predict_bp)

    with app.app_context():
        db_client.init_db(csv_path)
        Thread(target=db_client.load_dataframe()).run()

    Thread(target=inference_service.load_default_pipeline).run()

    app.run(debug=True)
