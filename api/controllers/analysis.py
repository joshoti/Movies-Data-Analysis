from flask import Blueprint

from api.services.analysis import analysis_service

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")


@analysis_bp.route("/<sample_id>", methods=["GET"])
def analysis(sample_id: str):
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    tags: [Analysis]
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
    return analysis_service.get_sample_data(sample_id)
