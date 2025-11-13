from flask import Blueprint, request

from .query_service import query_service

query_bp = Blueprint("query", __name__, url_prefix="/v1/query")


@query_bp.route("", methods=["GET"])
def query():
    """Queries the database
    Queries the database
    ---
    tags:
      - Query

    parameters:
      - name: select
        in: query
        description: Available values - title, year, director, actor, rating, runtime, censor, gross, main_genre
        schema:
          type: string
        examples:
          noColumn:
            value: " "
            summary: Implicitly selects all columns
          fewColumns:
            value: select=title,year,director
            summary: Selects only title, year and director columns
          allColumns:
            value: select=title,year,director,actor,rating,runtime,censor,gross,main_genre
            summary: Explicitly selects all columns

      - name: where
        in: query
        description: Four hyphen-separated components. 1. Logical operators - AND, OR. 2. Columns - title, year, (more examples above). 3. Comparison operators - LIKE, =, <, >, <=, >=, != 4. Values - (depends on column)
        schema:
          type: string
        examples:
          noClause:
            value: " "
            summary: No where clause
          oneClause:
            value: where=AND-title-LIKE-Avengers
            summary: One where clause
          multipleClauses:
            value: where=AND-title-LIKE-Avengers,AND-actor-LIKE-Robert,OR-rating-<-2
            summary: Multiple where clauses

    responses:
      200:
        description: OK
        content:
          application/json:
            examples:
              selectQuery:
                summary: Movies with a select and where (title LIKE avengers) query
                value: [
                  {
                    "Actors": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth",
                    "Movie_Title": "Avengers: Endgame",
                    "Rating": 8.4
                  },
                  {
                    "Actors": "Robert Downey Jr., Chris Hemsworth, Mark Ruffalo, Chris Evans",
                    "Movie_Title": "Avengers: Infinity War",
                    "Rating": 8.4
                  },
                ]
              noSelectQuery:
                summary: Movies with no select query
                value:
                  [
                    {
                      "Actors": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth",
                      "Censor": "UA",
                      "Director": "Joss Whedon",
                      "Movie_Title": "Avengers: Age of Ultron",
                      "Rating": 7.3,
                      "Runtime(Mins)": 141,
                      "Total_Gross": "$459.01M",
                      "Year": 2015,
                      "main_genre": "Action",
                      "side_genre": " Adventure,  Sci-Fi"
                    },
                  ]
    """
    return query_service.get_data(request.args)
