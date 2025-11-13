import os

import dotenv
from flask import Flask
from flask_cors import CORS

from api.v1.config import Config
from api.v1.extensions.db import db
from api.v1.extensions.swagger import swagger, swagger_bp

dotenv.load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register extensions
    db.init_app(app)
    swagger.init_app(app)
    CORS(app, origins=os.environ.get("TRUSTED_ORIGINS", "").split(","))

    # Register blueprints
    from api.v1.analysis import analysis_bp

    app.register_blueprint(analysis_bp)

    from api.v1.query import query_bp

    app.register_blueprint(query_bp)

    from api.v1.chat import chat_bp

    app.register_blueprint(chat_bp)

    app.register_blueprint(swagger_bp)

    return app
