from flask import Flask
from flask_cors import CORS

from api.extensions.db import db
from api.extensions.swagger import swagger
from api.utils.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register extensions
    db.init_app(app)
    swagger.init_app(app)
    CORS(app, origins=["http://localhost:3000"])

    # Register blueprints
    from api.analysis.analysisController import analysis_bp
    app.register_blueprint(analysis_bp)

    from api.controllers.query import query_bp
    app.register_blueprint(query_bp)

    from api.controllers.probe import probe_bp
    app.register_blueprint(probe_bp)

    from api.controllers.predict import predict_bp
    app.register_blueprint(predict_bp)

    return app
