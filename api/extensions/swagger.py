from flasgger import Swagger
from flask import Blueprint, redirect

swagger_config = {
    "title": "Movies Dataset OpenAPI Specification",
    "description": "OpenAPI Documentation for Dataset Visualization app",
    "version": "1.0",
    "openapi": "3.0.2",
    "termsOfService": "",
    "servers": [
        {
            "url": "http://localhost:5000",
            "description": "Local server",
        },
        {
            "url": "https://movies-data-analysis.onrender.com",
            "description": "Development server",
        },
        {
            "url": "TBA",
            "description": "Production server",
        },
    ],
    "components": {
        "schemas": {
            "ChartDataObject": {
                "type": "object",
                "properties": {
                    "min": {"type": "number", "format": "float", "example": 0},
                    "max": {"type": "number", "format": "float", "example": 100.5},
                    "data": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ChartDataPoints"},
                    },
                },
            },
            "ChartDataPoints": {
                "type": "object",
                "properties": {
                    "key1": {"type": "string", "example": "value1"},
                    "key2": {"type": "string", "example": "value2"},
                },
            },
            "Prompt": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "example": "What is the capital of Nigeria?",
                    },
                },
            },
            "Query": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "example": "Avengers: Endgame"},
                    "year": {"type": "string"},
                    "director": {
                        "type": "string",
                        "example": "Anthony Russo, Joe Russo",
                    },
                    "actor": {
                        "type": "string",
                        "example": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth",
                    },
                    "rating": {"type": "number", "format": "float", "example": 8.4},
                    "runtime": {"type": "integer", "example": 181},
                    "censor": {"type": "string", "example": "UA"},
                    "gross": {"type": "string", "example": "$858.37M"},
                    "main_genre": {"type": "string", "example": "Action"},
                },
            },
        },
    },
}

swagger = Swagger()


swagger_bp = Blueprint("swagger", __name__, url_prefix="/")


@swagger_bp.route("", methods=["GET"])
def default_redirect():
    return redirect("/apidocs")
