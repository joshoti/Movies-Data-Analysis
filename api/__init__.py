from flask import Flask
from flask_cors import CORS

from api.config import Config
from api.extensions.db import db
from api.extensions.swagger import swagger


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register extensions
    db.init_app(app)
    swagger.init_app(app)
    CORS(app, origins=["http://localhost:3000"])

    # Register blueprints
    from api.analysis import analysis_bp
    app.register_blueprint(analysis_bp)

    from api.query import query_bp
    app.register_blueprint(query_bp)

    from api.probe import probe_bp
    app.register_blueprint(probe_bp)

    from api.predict import predict_bp
    app.register_blueprint(predict_bp)

    return app
