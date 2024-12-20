from flask import Blueprint, request

from .queryService import query_service

query_bp = Blueprint("query", __name__, url_prefix="/query")


@query_bp.route("", methods=["GET"])
def query():
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    tags: [Query]
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    return query_service.get_data(request.args)
