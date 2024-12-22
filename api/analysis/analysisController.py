from flask import Blueprint

from .analysisService import analysis_service

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")


@analysis_bp.route("/<sample_id>", methods=["GET"])
def analysis(sample_id: str):
    """Gets data for analysis charts
    Gets data for analysis charts
    ---
    tags:
      - Analysis

    parameters:
      - name: sample_id
        in: path
        description: ID's 1-5 are available
        required: true
        schema:
          type: string
        example:
          sample-1

    responses:
      200:
        description: OK
        content:
          application/json:
            examples:
              chartObjects:
                summary: Chart data object
                value:
                  { min: 0, max: 100.5, data: [{key1: value1, key2: value2 }] }

              chartPoints:
                summary: List of chart data points
                value:
                  [{ key1: value1, key2: value2 }]
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/ChartDataPoints'
            # schema:
            #   type: array
            #   items:
            #     $ref: '#/components/schemas/ChartDataPoints'
            # schema:
            #   $ref: '#/components/schemas/ChartDataObject'
    """
    return analysis_service.get_sample_data(sample_id)
