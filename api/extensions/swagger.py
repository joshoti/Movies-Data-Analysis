from flasgger import Swagger

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
            "url": "TBA",
            "description": "Production server",
        },
    ],
}

swagger = Swagger()
