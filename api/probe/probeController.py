from flask import Blueprint, request

from .probeService import probing_service

probe_bp = Blueprint("probe", __name__, url_prefix="/probe")


@probe_bp.route("", methods=["POST"])
def probe():
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    tags: [Probe]
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
    return probing_service.answer_question(request.json["prompt"])
